import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

def create_score_trend_plot(df):
    """Create a line plot showing score trends over time."""
    fig = go.Figure()
    
    metrics = {
        'social_score': 'Social Interaction',
        'communication_score': 'Communication',
        'behavior_score': 'Behavior'
    }
    
    for metric, label in metrics.items():
        fig.add_trace(
                go.Scatter(
                    x=df['assessment_date'],
                    y=df[metric],
                    name=label,
                    mode='lines+markers',
                    hovertemplate=f"{label}: %{{y:.1f}}<br>Date: %{{x|%Y-%m-%d}}<extra></extra>"
            )
        )
    
    fig.update_layout(
        title="Score Trends Over Time",
        xaxis_title="Assessment Date",
        yaxis_title="Score",
        hovermode='x unified',
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def create_radar_chart(latest_scores):
    """Create a radar chart showing the latest scores."""
    categories = ['Social Interaction', 'Communication', 'Behavior']
    values = [
        latest_scores['social_score'],
        latest_scores['communication_score'],
        latest_scores['behavior_score']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],  # Repeat first value to close the polygon
        theta=categories + [categories[0]],  # Repeat first category to close the polygon
        fill='toself',
        name='Latest Assessment'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        title="Latest Assessment Scores"
    )
    
    return fig

def create_age_distribution_plot(df):
    """Create a box plot showing score distributions by age group."""
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 5, 10, 15, 18],
        labels=['0-5', '6-10', '11-15', '16-18']
    )
    
    fig = go.Figure()
    
    metrics = {
        'social_score': 'Social Interaction',
        'communication_score': 'Communication',
        'behavior_score': 'Behavior'
    }
    
    for metric, label in metrics.items():
        fig.add_trace(
            go.Box(
                x=df['age_group'],
                y=df[metric],
                name=label
            )
        )
    
    fig.update_layout(
        title="Score Distribution by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Score",
        boxmode='group'
    )
    
    return fig

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
    
    # Interactive visualizations
    tab1, tab2, tab3 = st.tabs(["Trends", "Current Status", "Age Analysis"])
    
    with tab1:
        st.plotly_chart(
            create_score_trend_plot(df),
            use_container_width=True
        )
    
    with tab2:
        # Get latest assessment for radar chart
        latest_df = df.sort_values('assessment_date').iloc[-1]
        st.plotly_chart(
            create_radar_chart(latest_df),
            use_container_width=True
        )
    
    with tab3:
        st.plotly_chart(
            create_age_distribution_plot(df),
            use_container_width=True
        )
    
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