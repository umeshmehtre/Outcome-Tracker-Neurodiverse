import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.utils.data_processing import (
    process_assessment_data,
    calculate_summary_stats,
    calculate_progress,
    identify_areas_of_concern
)

@pytest.fixture
def sample_assessments():
    """Fixture providing sample assessment data."""
    return [
        {
            'child_id': 'C001',
            'age': 8,
            'assessment_date': datetime(2024, 1, 1),
            'social_score': 7.0,
            'communication_score': 6.0,
            'behavior_score': 8.0,
            'notes': 'Initial assessment'
        },
        {
            'child_id': 'C001',
            'age': 8,
            'assessment_date': datetime(2024, 2, 1),
            'social_score': 8.0,
            'communication_score': 7.0,
            'behavior_score': 8.5,
            'notes': 'Follow-up'
        },
        {
            'child_id': 'C002',
            'age': 10,
            'assessment_date': datetime(2024, 1, 15),
            'social_score': 4.0,
            'communication_score': 3.0,
            'behavior_score': 5.0,
            'notes': 'Initial assessment'
        }
    ]

def test_process_assessment_data(sample_assessments):
    """Test assessment data processing."""
    df = process_assessment_data(sample_assessments)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert 'assessment_date' in df.columns
    assert df['assessment_date'].dtype == 'datetime64[ns]'

def test_process_empty_assessment_data():
    """Test processing empty assessment data."""
    df = process_assessment_data([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_calculate_summary_stats(sample_assessments):
    """Test summary statistics calculation."""
    df = process_assessment_data(sample_assessments)
    stats = calculate_summary_stats(df)
    
    assert 'social_score' in stats
    assert 'communication_score' in stats
    assert 'behavior_score' in stats
    
    # Test social score statistics
    social_stats = stats['social_score']
    assert isinstance(social_stats['mean'], float)
    assert isinstance(social_stats['median'], float)
    assert isinstance(social_stats['std'], float)
    assert social_stats['min'] == 4.0
    assert social_stats['max'] == 8.0

def test_calculate_progress(sample_assessments):
    """Test progress calculation for a specific child."""
    df = process_assessment_data(sample_assessments)
    progress = calculate_progress(df, 'C001')
    
    assert 'social_score' in progress
    assert 'communication_score' in progress
    assert 'behavior_score' in progress
    
    social_progress = progress['social_score']
    assert social_progress['initial_score'] == 7.0
    assert social_progress['current_score'] == 8.0
    assert social_progress['absolute_change'] == 1.0
    assert abs(social_progress['percent_change'] - 14.285714) < 0.0001

def test_identify_areas_of_concern(sample_assessments):
    """Test identification of areas of concern."""
    df = process_assessment_data(sample_assessments)
    concerns = identify_areas_of_concern(df, threshold=5.0)
    
    assert len(concerns) > 0
    concern = next((c for c in concerns if c['area'] == 'communication'), None)
    assert concern is not None
    assert concern['count'] == 1
    assert concern['affected_children'] == 1
    assert concern['average_score'] == 3.0

def test_identify_areas_of_concern_no_concerns(sample_assessments):
    """Test identification of areas of concern with high threshold."""
    df = process_assessment_data(sample_assessments)
    concerns = identify_areas_of_concern(df, threshold=2.0)
    assert len(concerns) == 0