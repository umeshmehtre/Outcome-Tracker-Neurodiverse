import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime

def process_assessment_data(assessments: List[Dict]) -> pd.DataFrame:
    """
    Convert assessment data to a pandas DataFrame and perform basic processing.
    
    Args:
        assessments (List[Dict]): List of assessment dictionaries
        
    Returns:
        pd.DataFrame: Processed assessment data
    """
    if not assessments:
        return pd.DataFrame()
        
    df = pd.DataFrame(assessments)
    
    # Convert dates to datetime
    if 'assessment_date' in df.columns:
        df['assessment_date'] = pd.to_datetime(df['assessment_date'])
        
    return df

def calculate_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Calculate summary statistics for assessment scores.
    
    Args:
        df (pd.DataFrame): Assessment data DataFrame
        
    Returns:
        Dict: Dictionary containing summary statistics
    """
    score_columns = ['social_score', 'communication_score', 'behavior_score']
    
    summary = {}
    for col in score_columns:
        if col in df.columns:
            summary[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max()
            }
            
    return summary

def calculate_progress(df: pd.DataFrame, child_id: str) -> Dict:
    """
    Calculate progress over time for a specific child.
    
    Args:
        df (pd.DataFrame): Assessment data DataFrame
        child_id (str): Child ID to analyze
        
    Returns:
        Dict: Dictionary containing progress metrics
    """
    if df.empty:
        return {}
        
    child_data = df[df['child_id'] == child_id].sort_values('assessment_date')
    
    if child_data.empty:
        return {}
        
    progress = {}
    score_columns = ['social_score', 'communication_score', 'behavior_score']
    
    for col in score_columns:
        if col in child_data.columns and len(child_data) >= 2:
            initial = child_data[col].iloc[0]
            current = child_data[col].iloc[-1]
            change = current - initial
            percent_change = (change / initial * 100) if initial != 0 else 0
            
            progress[col] = {
                'initial_score': initial,
                'current_score': current,
                'absolute_change': change,
                'percent_change': percent_change
            }
            
    return progress

def generate_trend_data(df: pd.DataFrame, metric: str) -> Dict:
    """
    Generate trend data for visualization.
    
    Args:
        df (pd.DataFrame): Assessment data DataFrame
        metric (str): Metric to analyze (e.g., 'social_score')
        
    Returns:
        Dict: Dictionary containing trend data
    """
    if df.empty or metric not in df.columns:
        return {}
        
    trends = {}
    
    # Overall trend
    trends['overall'] = df.groupby('assessment_date')[metric].mean().to_dict()
    
    # Trend by age group
    df['age_group'] = pd.cut(df['age'], 
                            bins=[0, 5, 10, 15, 20],
                            labels=['0-5', '6-10', '11-15', '16+'])
    
    trends['by_age_group'] = {
        str(group): group_data[metric].mean()
        for group, group_data in df.groupby('age_group')
    }
    
    return trends

def identify_areas_of_concern(df: pd.DataFrame, threshold: float = 4.0) -> List[Dict]:
    """
    Identify areas that may need attention based on low scores.
    
    Args:
        df (pd.DataFrame): Assessment data DataFrame
        threshold (float): Score threshold for concern
        
    Returns:
        List[Dict]: List of identified concerns
    """
    concerns = []
    score_columns = ['social_score', 'communication_score', 'behavior_score']
    
    for col in score_columns:
        if col in df.columns:
            low_scores = df[df[col] < threshold]
            if not low_scores.empty:
                concerns.append({
                    'area': col.replace('_score', ''),
                    'count': len(low_scores),
                    'affected_children': low_scores['child_id'].nunique(),
                    'average_score': low_scores[col].mean()
                })
                
    return concerns