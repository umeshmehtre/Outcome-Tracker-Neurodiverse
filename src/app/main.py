import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.models import init_db, Session
from database.crud import add_assessment, get_assessments, get_assessment
from utils.data_processing import (
    process_assessment_data,
    calculate_summary_stats,
    calculate_progress,
    generate_trend_data,
    identify_areas_of_concern
)

def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Outcome Tracker",
        page_icon="📊",
        layout="wide"
    )
    st.title("Outcome Tracker for Neurodiverse Interventions")

def render_data_entry():
    """Render the data entry form."""
    st.header("Assessment Data Entry")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            child_id = st.text_input("Child ID", key="child_id")
            age = st.number_input("Age", min_value=0, max_value=18, key="age")
        
        with col2:
            assessment_date = st.date_input(
                "Assessment Date",
                value=datetime.now(),
                key="assessment_date"
            )
        
        st.subheader("Assessment Scores")
        score_col1, score_col2, score_col3 = st.columns(3)
        
        with score_col1:
            social_score = st.slider(
                "Social Interaction Score",
                min_value=1,
                max_value=10,
                value=5,
                help="Rate social interaction skills"
            )
        
        with score_col2:
            communication_score = st.slider(
                "Communication Score",
                min_value=1,
                max_value=10,
                value=5,
                help="Rate communication abilities"
            )
        
        with score_col3:
            behavior_score = st.slider(
                "Behavioral Score",
                min_value=1,
                max_value=10,
                value=5,
                help="Rate behavioral regulation"
            )
        
        notes = st.text_area("Additional Notes", key="notes")
        
        submitted = st.form_submit_button("Submit Assessment")
        
        if submitted:
            try:
                assessment_data = {
                    "child_id": child_id,
                    "age": age,
                    "assessment_date": assessment_date,
                    "social_score": social_score,
                    "communication_score": communication_score,
                    "behavior_score": behavior_score,
                    "notes": notes
                }
                
                add_assessment(assessment_data)
                st.success("Assessment data saved successfully!")
                
            except Exception as e:
                st.error(f"Error saving assessment: {str(e)}")

def render_analytics():
    """Render the analytics dashboard."""
    st.header("Analytics Dashboard")
    
    # Get all assessments
    assessments = get_assessments()
    if not assessments:
        st.warning("No assessment data available.")
        return
    
    # Process data
    df = process_assessment_data([{
        'child_id': a.child_id,
        'age': a.age,
        'assessment_date': a.assessment_date,
        'social_score': a.social_score,
        'communication_score': a.communication_score,
        'behavior_score': a.behavior_score,
        'notes': a.notes
    } for a in assessments])
    
    # Summary statistics
    st.subheader("Summary Statistics")
    stats = calculate_summary_stats(df)
    
    col1, col2, col3 = st.columns(3)
    
    metrics = {
        'social_score': 'Social Interaction',
        'communication_score': 'Communication',
        'behavior_score': 'Behavior'
    }
    
    for (col, (metric, label)) in zip(
        [col1, col2, col3],
        metrics.items()
    ):
        with col:
            if metric in stats:
                st.metric(
                    label=f"{label} Score",
                    value=f"{stats[metric]['mean']:.2f}",
                    delta=f"{stats[metric]['std']:.2f} σ"
                )
    
    # Trends over time
    st.subheader("Score Trends Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for metric, label in metrics.items():
        sns.lineplot(
            data=df,
            x='assessment_date',
            y=metric,
            label=label,
            marker='o'
        )
    
    plt.title("Score Trends Over Time")
    plt.xlabel("Assessment Date")
    plt.ylabel("Score")
    plt.legend()
    st.pyplot(fig)
    
    # Areas of concern
    st.subheader("Areas of Concern")
    concerns = identify_areas_of_concern(df)
    if concerns:
        for concern in concerns:
            st.warning(
                f"{concern['area'].title()}: {concern['count']} low scores "
                f"affecting {concern['affected_children']} children "
                f"(avg: {concern['average_score']:.2f})"
            )
    else:
        st.success("No major areas of concern identified.")

def main():
    """Main application entry point."""
    setup_page()
    
    # Initialize database
    init_db()
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select Page",
        ["Data Entry", "Analytics"]
    )
    
    if page == "Data Entry":
        render_data_entry()
    else:
        render_analytics()

if __name__ == "__main__":
    main()