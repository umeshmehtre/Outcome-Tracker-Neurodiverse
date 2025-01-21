from datetime import datetime
from typing import Dict, List, Optional

from .models import Session, Assessment

def add_assessment(data: Dict) -> Assessment:
    """
    Add a new assessment to the database.
    
    Args:
        data (Dict): Dictionary containing assessment data
        
    Returns:
        Assessment: Created assessment object
    """
    with Session() as session:
        assessment = Assessment(
            child_id=data['child_id'],
            age=data['age'],
            social_score=data['social_score'],
            communication_score=data['communication_score'],
            behavior_score=data['behavior_score'],
            notes=data.get('notes', '')
        )
        session.add(assessment)
        session.commit()
        session.refresh(assessment)
        return assessment

def get_assessment(assessment_id: int) -> Optional[Assessment]:
    """
    Retrieve a specific assessment by ID.
    
    Args:
        assessment_id (int): ID of the assessment to retrieve
        
    Returns:
        Optional[Assessment]: Assessment object if found, None otherwise
    """
    with Session() as session:
        return session.query(Assessment).filter(Assessment.id == assessment_id).first()

def get_assessments(child_id: Optional[str] = None) -> List[Assessment]:
    """
    Retrieve all assessments, optionally filtered by child_id.
    
    Args:
        child_id (Optional[str]): Child ID to filter by
        
    Returns:
        List[Assessment]: List of assessment objects
    """
    with Session() as session:
        query = session.query(Assessment)
        if child_id:
            query = query.filter(Assessment.child_id == child_id)
        return query.order_by(Assessment.assessment_date.desc()).all()

def update_assessment(assessment_id: int, data: Dict) -> Optional[Assessment]:
    """
    Update an existing assessment.
    
    Args:
        assessment_id (int): ID of the assessment to update
        data (Dict): Dictionary containing updated assessment data
        
    Returns:
        Optional[Assessment]: Updated assessment object if found, None otherwise
    """
    with Session() as session:
        assessment = session.query(Assessment).filter(Assessment.id == assessment_id).first()
        if assessment:
            for key, value in data.items():
                if hasattr(assessment, key):
                    setattr(assessment, key, value)
            assessment.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(assessment)
        return assessment

def delete_assessment(assessment_id: int) -> bool:
    """
    Delete an assessment from the database.
    
    Args:
        assessment_id (int): ID of the assessment to delete
        
    Returns:
        bool: True if assessment was deleted, False otherwise
    """
    with Session() as session:
        assessment = session.query(Assessment).filter(Assessment.id == assessment_id).first()
        if assessment:
            session.delete(assessment)
            session.commit()
            return True
        return False