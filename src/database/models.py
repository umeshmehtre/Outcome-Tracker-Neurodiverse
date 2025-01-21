from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create SQLite database engine
DATABASE_URL = "sqlite:///data/outcomes.db"
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

class Assessment(Base):
    """Model for storing assessment data."""
    __tablename__ = 'assessments'

    id = Column(Integer, primary_key=True)
    child_id = Column(String(50), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    age = Column(Integer, nullable=False)
    
    # Assessment scores
    social_score = Column(Float)
    communication_score = Column(Float)
    behavior_score = Column(Float)
    
    # Additional fields
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create Session class
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database, creating all tables."""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()