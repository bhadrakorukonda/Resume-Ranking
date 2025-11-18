# Resume Ranking System

A comprehensive AI-powered resume ranking system that uses Multi-Criteria Decision Making (MCDM) techniques to evaluate and rank job candidates based on their resumes and job descriptions.

## 🚀 Features

- **Intelligent Resume Parsing**: Extract text from PDF resumes using PyPDF2
- **NLP-Powered Feature Extraction**: Utilize spaCy for natural language processing to analyze skills, experience, and job alignment
- **TOPSIS Ranking Algorithm**: Implement Technique for Order of Preference by Similarity to Ideal Solution for objective candidate ranking
- **Customizable Weight Configurations**: Allow users to define custom weighting schemes for different evaluation criteria
- **RESTful API**: Clean Flask-based API for seamless integration
- **Modern Web Interface**: React-based frontend with Tailwind CSS for intuitive user experience
- **Database Storage**: SQLite database for persistent candidate and configuration data
- **Docker Support**: Containerized deployment with Docker Compose

## 🛠 Tech Stack

### Backend
- **Python 3.10**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **spaCy** - Natural Language Processing
- **PyPDF2** - PDF text extraction
- **NumPy** - Numerical computations
- **RapidFuzz** - Fuzzy string matching

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **SQLite** - Database
- **Git** - Version control

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- Docker (optional, for containerized deployment)

## 🔧 Installation

### Option 1: Local Development

#### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhadrakorukonda/Resume-Ranking.git
   cd Resume-Ranking
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

#### Frontend Setup

1. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

2. **Start the development servers**

   **Backend:**
   ```bash
   cd backend
   python run.py
   ```
   Server will be available at `http://localhost:5000`

   **Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:5000`

## 📖 Usage

### Web Interface

1. **Upload Resumes**: Use the web interface to upload PDF resumes along with candidate information
2. **Configure Weights**: Create custom weight configurations for different job types
3. **Rank Candidates**: Automatically rank candidates using the TOPSIS algorithm
4. **View Results**: See detailed rankings with scores and feature analysis

### API Usage

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Upload Resume
```bash
curl -X POST http://localhost:5000/upload \
  -F "resume=@resume.pdf" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "job_description=Software Engineer position requiring Python and React"
```

#### Get Candidates
```bash
curl http://localhost:5000/candidates
```

#### Rank Candidates
```bash
curl -X POST http://localhost:5000/rank \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {
      "skill_match": 0.3,
      "jd_alignment": 0.3,
      "exp_years": 0.2,
      "projects": 0.1,
      "education": 0.1
    }
  }'
```

#### Manage Weights
```bash
# Get all weights
curl http://localhost:5000/weights

# Create new weights
curl -X POST http://localhost:5000/weights \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Senior Developer",
    "skill_match": 0.25,
    "jd_alignment": 0.35,
    "exp_years": 0.25,
    "projects": 0.10,
    "education": 0.05
  }'
```

## 🏗 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/weights` | Get all weight configurations |
| POST | `/weights` | Create new weight configuration |
| POST | `/upload` | Upload resume and extract features |
| POST | `/rank` | Rank candidates using TOPSIS |
| GET | `/candidates` | Get all candidates |
| GET | `/candidates/<id>` | Get specific candidate |
| DELETE | `/candidates/<id>` | Delete candidate |

### Request/Response Formats

#### Weight Configuration
```json
{
  "name": "Default Weights",
  "skill_match": 0.25,
  "jd_alignment": 0.30,
  "exp_years": 0.20,
  "projects": 0.15,
  "education": 0.10
}
```

#### Candidate Data
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "",
  "skill_match": 0.85,
  "jd_alignment": 0.72,
  "exp_years": 5.0,
  "projects": 8.0,
  "education": 4.5,
  "rank": 1,
  "topsis_score": 0.823
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m unittest discover tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔍 How It Works

1. **Resume Upload**: PDFs are uploaded and text is extracted using PyPDF2
2. **Feature Extraction**: spaCy analyzes the text to extract:
   - Skill match percentage
   - Job description alignment
   - Years of experience
   - Number of projects
   - Education level
3. **Normalization**: Features are normalized to comparable scales
4. **TOPSIS Ranking**: Multi-criteria decision making algorithm ranks candidates objectively
5. **Results**: Ranked list with scores and detailed feature analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [spaCy](https://spacy.io/) for NLP capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [TOPSIS](https://en.wikipedia.org/wiki/TOPSIS) algorithm for MCDM
- [React](https://reactjs.org/) for the frontend framework

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ for efficient and fair candidate evaluation**</content>
<parameter name="filePath">h:\Resume ranker\Resume-Ranking-1\README.md