from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Candidate, Weights
from config import DATABASE_URL, DEFAULT_WEIGHTS

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    
    # Create default weights if they don't exist
    session = SessionLocal()
    try:
        default_weights = session.query(Weights).filter(Weights.is_default == 1).first()
        if not default_weights:
            default_weights = Weights(
                name="Default Weights",
                skill_match=DEFAULT_WEIGHTS['skill_match'],
                jd_alignment=DEFAULT_WEIGHTS['jd_alignment'],
                exp_years=DEFAULT_WEIGHTS['exp_years'],
                projects=DEFAULT_WEIGHTS['projects'],
                education=DEFAULT_WEIGHTS['education'],
                is_default=1
            )
            session.add(default_weights)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_default_weights():
    """Get default weights from database"""
    session = SessionLocal()
    try:
        weights = session.query(Weights).filter(Weights.is_default == 1).first()
        if weights:
            return weights
        else:
            # Fallback to config defaults
            return Weights(
                name="Config Default",
                skill_match=DEFAULT_WEIGHTS['skill_match'],
                jd_alignment=DEFAULT_WEIGHTS['jd_alignment'],
                exp_years=DEFAULT_WEIGHTS['exp_years'],
                projects=DEFAULT_WEIGHTS['projects'],
                education=DEFAULT_WEIGHTS['education'],
                is_default=1
            )
    finally:
        session.close()
