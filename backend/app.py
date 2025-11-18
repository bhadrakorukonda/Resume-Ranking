from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, DEFAULT_WEIGHTS
from db import get_db, init_db, get_default_weights
from models import Candidate, Weights
from nlp import extract_text_from_pdf, extract_features, normalize_features
from mcdm import rank_candidates, validate_weights, normalize_weights

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Initialize database
init_db()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/weights', methods=['GET'])
def get_weights():
    """Get all weight configurations"""
    db = next(get_db())
    try:
        weights_list = db.query(Weights).order_by(desc(Weights.is_default), Weights.name).all()
        return jsonify({
            'weights': [weight.to_dict() for weight in weights_list],
            'default_weights': DEFAULT_WEIGHTS
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/weights', methods=['POST'])
def create_weights():
    """Create new weight configuration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract weights from data
        weights = {k: v for k, v in data.items() if k != 'name'}
        
        # Validate weights
        is_valid, error_msg = validate_weights(weights)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Normalize weights
        normalized_weights = normalize_weights(weights)
        
        db = next(get_db())
        try:
            # Check if name already exists
            existing = db.query(Weights).filter(Weights.name == data['name']).first()
            if existing:
                return jsonify({'error': 'Weight configuration with this name already exists'}), 400
            
            # Create new weights
            weights = Weights(
                name=data['name'],
                skill_match=normalized_weights['skill_match'],
                jd_alignment=normalized_weights['jd_alignment'],
                exp_years=normalized_weights['exp_years'],
                projects=normalized_weights['projects'],
                education=normalized_weights['education']
            )
            
            db.add(weights)
            db.commit()
            
            return jsonify({
                'message': 'Weight configuration created successfully',
                'weights': weights.to_dict()
            }), 201
            
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Upload resume PDF and job description"""
    try:
        # Check if files are present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'File type not allowed. Only PDF files are accepted.'}), 400
        
        # Save file
        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(filepath)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)
        if not resume_text:
            os.remove(filepath)  # Clean up file
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Extract features
        features = extract_features(resume_text, job_description)
        normalized_features = normalize_features(features)
        
        # Save candidate to database
        db = next(get_db())
        try:
            candidate = Candidate(
                name=request.form.get('name', 'Unknown'),
                email=request.form.get('email', ''),
                phone=request.form.get('phone', ''),
                resume_text=resume_text,
                resume_filename=filename,
                skill_match=normalized_features['skill_match'],
                jd_alignment=normalized_features['jd_alignment'],
                exp_years=normalized_features['exp_years'],
                projects=normalized_features['projects'],
                education=normalized_features['education']
            )
            
            db.add(candidate)
            db.commit()
            
            return jsonify({
                'message': 'Resume uploaded and processed successfully',
                'candidate_id': candidate.id,
                'features': normalized_features,
                'filename': filename
            }), 201
            
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rank', methods=['POST'])
def rank_candidates_endpoint():
    """Rank candidates using TOPSIS"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Get weights (use provided weights or default)
        weights_data = data.get('weights', DEFAULT_WEIGHTS)
        weights_id = data.get('weights_id')
        
        db = next(get_db())
        try:
            # Get weights from database if weights_id provided
            if weights_id:
                weights_obj = db.query(Weights).filter(Weights.id == weights_id).first()
                if not weights_obj:
                    return jsonify({'error': 'Weight configuration not found'}), 404
                weights_dict = {
                    'skill_match': weights_obj.skill_match,
                    'jd_alignment': weights_obj.jd_alignment,
                    'exp_years': weights_obj.exp_years,
                    'projects': weights_obj.projects,
                    'education': weights_obj.education
                }
            else:
                # Validate provided weights
                is_valid, error_msg = validate_weights(weights_data)
                if not is_valid:
                    return jsonify({'error': error_msg}), 400
                weights_dict = normalize_weights(weights_data)
            
            # Get all candidates
            candidates = db.query(Candidate).all()
            if not candidates:
                return jsonify({'error': 'No candidates found'}), 404
            
            # Convert to list of dictionaries
            candidates_data = [candidate.to_dict() for candidate in candidates]
            
            # Rank candidates
            ranked_candidates = rank_candidates(candidates_data, weights_dict)
            
            return jsonify({
                'message': 'Candidates ranked successfully',
                'ranked_candidates': ranked_candidates,
                'weights_used': weights_dict,
                'total_candidates': len(ranked_candidates)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/candidates', methods=['GET'])
def get_candidates():
    """Get all candidates"""
    db = next(get_db())
    try:
        candidates = db.query(Candidate).order_by(desc(Candidate.created_at)).all()
        return jsonify({
            'candidates': [candidate.to_dict() for candidate in candidates],
            'total': len(candidates)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get specific candidate by ID"""
    db = next(get_db())
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        return jsonify({'candidate': candidate.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete candidate by ID"""
    db = next(get_db())
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Delete associated file
        if candidate.resume_filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], candidate.resume_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.delete(candidate)
        db.commit()
        
        return jsonify({'message': 'Candidate deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
