# Outcome Tracker for Neurodiverse Interventions

A web-based application designed to capture and analyze psychosocial outcomes for neurodiverse children. The application provides data collection, analysis, visualization, and predictive modeling capabilities.

## Features

- Data Collection Form: Web interface for inputting psychosocial data
- Database Integration: SQLite database for data storage and management
- Data Analytics: Analysis using Pandas and NumPy with visualizations
- Interactive Dashboard: Outcome visualization and KPI tracking
- Predictive Modeling: Basic ML model for outcome prediction

## Project Structure

```
.
├── src/                  # Source code files
│   ├── app/             # Streamlit web application
│   ├── database/        # Database scripts and models
│   ├── analysis/        # Data analysis and ML scripts
│   └── utils/           # Helper functions
├── data/                # Data storage (excluding sensitive data)
│   ├── raw/            # Raw data files
│   └── processed/      # Processed datasets
├── dashboard/          # Dashboard files
├── tests/             # Unit tests
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run src/app/main.py
   ```

## Technologies Used

- Python 3.8+
- Streamlit for web interface
- SQLite for database
- Pandas & NumPy for data analysis
- Matplotlib & Seaborn for visualization
- Scikit-learn for machine learning
- Power BI/Tableau for dashboard

## Development

Currently under active development. Features will be implemented in phases:

1. Basic data collection form 
2. Database integration 
3. Data analysis scripts
4. Dashboard development
5. Predictive modeling
6. Testing and documentation

## Results on Sreamlit Web Application

Assessment Data Entry Dashboard of Outcome Tracker for Neurodiverse Interventions
![Data entry](https://github.com/user-attachments/assets/d536c1ac-ccdb-47f1-a239-8ee04f320c0e)

### Analytics
Trends
![Trends](https://github.com/user-attachments/assets/465aaa0e-9377-499a-8f21-1b2277b278b0)

Age Analysis
![Age Analysis ](https://github.com/user-attachments/assets/c263a77d-2530-4e98-b343-576e2f283705)

Database
![image](https://github.com/user-attachments/assets/bb52aaf9-9d35-450c-9c99-f3a347700385)

#### Umesh Mehtre
