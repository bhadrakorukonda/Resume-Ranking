from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    resume_text = Column(Text)
    resume_filename = Column(String(255))
    
    # Feature scores
    skill_match = Column(Float, default=0.0)
    jd_alignment = Column(Float, default=0.0)
    exp_years = Column(Float, default=0.0)
    projects = Column(Float, default=0.0)
    education = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'resume_filename': self.resume_filename,
            'skill_match': self.skill_match,
            'jd_alignment': self.jd_alignment,
            'exp_years': self.exp_years,
            'projects': self.projects,
            'education': self.education,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_feature_vector(self):
        """Return feature vector in the order specified by FEATURE_ORDER"""
        return [
            self.skill_match,
            self.jd_alignment,
            self.exp_years,
            self.projects,
            self.education
        ]

class Weights(Base):
    __tablename__ = 'weights'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    
    # Weight values
    skill_match = Column(Float, nullable=False)
    jd_alignment = Column(Float, nullable=False)
    exp_years = Column(Float, nullable=False)
    projects = Column(Float, nullable=False)
    education = Column(Float, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_default = Column(Integer, default=0)  # 1 for default, 0 for custom
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'skill_match': self.skill_match,
            'jd_alignment': self.jd_alignment,
            'exp_years': self.exp_years,
            'projects': self.projects,
            'education': self.education,
            'is_default': bool(self.is_default),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_weight_vector(self):
        """Return weight vector in the order specified by FEATURE_ORDER"""
        return [
            self.skill_match,
            self.jd_alignment,
            self.exp_years,
            self.projects,
            self.education
        ]
