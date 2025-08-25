"""
Module containing the questions for the project initialization questionnaire.
Each question is a dictionary with a key, question text, and input type.
"""

PROJECT_QUESTIONS = [
    {
        "key": "project_name",
        "question": "Enter the project name (e.g., client-name-demand-forecasting): ",
        "type": "text"
    },
    {
        "key": "client_name",
        "question": "Enter the client's name or organization: ",
        "type": "text"
    },
    {
        "key": "project_goal",
        "question": "Describe the primary goal of the project (1-2 sentences): ",
        "type": "text"
    },
    {
        "key": "success_metric",
        "question": "Define the primary success metric (e.g., MAE < 100 units, 99% accuracy): ",
        "type": "text"
    },
    {
        "key": "data_sources",
        "question": "Describe the data sources (e.g., BigQuery, S3 buckets, API endpoints): ",
        "type": "text"
    },
    {
        "key": "model_type",
        "question": "What type of modeling is anticipated? (e.g., time-series forecasting, classification, regression): ",
        "type": "text"
    },
    {
        "key": "budget_range",
        "question": "What is the project's budget range? (e.g., 10k-15k): ",
        "type": "text"
    },
    # Add more questions relevant to ML projects here.
    # Example: timeline, key stakeholders, known risks, etc.
]