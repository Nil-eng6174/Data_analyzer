# AI-Powered Business Intelligence & Data Analytics Project

## Problem Statement
Businesses generate vast amounts of data daily. Without proper analysis, they fail to identify key trends, risks, and opportunities, leading to suboptimal decision-making. 

## Objectives
- Perform comprehensive data cleaning and exploratory data analysis (EDA).
- Build a KPI engine to track revenue, profit, and margins.
- Analyze trends and drivers behind business performance.
- Identify risks (e.g., unprofitable segments) and opportunities.
- Implement time-series forecasting for future sales.
- Generate automated, AI-style insights based on calculated data.
- Build an interactive Streamlit dashboard to present these findings.

## Dataset and Source
- **Name:** Superstore Sales Dataset (2011-2015)
- **Source:** [Public Github Repository (pplonski/datasets-for-start)](https://raw.githubusercontent.com/pplonski/datasets-for-start/refs/heads/master/superstore-sales/superstore_dataset2011-2015.csv)

## Features
- **Data Pipeline:** End-to-end data ingestion, cleaning, and transformation.
- **KPI Engine:** Calculates total revenue, profit, profit margin, and orders dynamically.
- **Trend & Driver Analysis:** Visualizes performance over time and identifies key drivers (Categories/Regions).
- **Forecasting:** Linear regression model built with scikit-learn for predicting future sales.
- **AI Insights:** Rule-based engine that converts calculated metrics into natural language actionable insights.

## Technology Stack
- Python, Pandas, NumPy
- Scikit-learn
- Plotly, Matplotlib, Seaborn
- Streamlit
- Jupyter Notebook

## Architecture & Methodology
1. **Data Ingestion (`data_cleaning.py`)**: Reads raw CSV, handles missing values, standardized names, and date formats.
2. **Analysis Engine (`src/analysis.py`)**: Computes aggregations, trends, and business logic.
3. **Forecasting (`src/forecasting.py`)**: Trains an ML model on historical data.
4. **Insight Engine (`src/insights.py`)**: Evaluates results and generates text insights.
5. **Dashboard (`app.py`)**: Serves the user interface using Streamlit.

## Installation & How to Run

1. Clone or download the repository.
2. Navigate to the project directory:
   ```bash
   cd Superstore_BI_Project
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the data cleaning pipeline:
   ```bash
   python src/data_cleaning.py
   ```
5. Launch the Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```

## Project Structure
```text
Project/
├── app.py                  # Main Streamlit Dashboard
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── Project_Report.md       # Detailed project report
├── data/                   
│   ├── raw_dataset.csv     # Original data
│   └── cleaned_dataset.csv # Processed data
├── src/                    
│   ├── data_cleaning.py    # Data preparation pipeline
│   ├── analysis.py         # KPI & Driver analysis logic
│   ├── forecasting.py      # ML forecasting module
│   └── insights.py         # AI-insight generator
├── notebooks/              
│   └── analysis.ipynb      # EDA notebook
└── assets/                 
    └── screenshots/        # Application screenshots
```

## Results & Findings
- The KPI engine correctly computed overall profitability, showing specific segments operating at a loss.
- The trend analysis highlighted clear seasonal peaks.
- Driver analysis revealed that certain categories, while driving high volume, suffer from negative margins due to excessive discounts.
- The predictive model provided a 6-month sales forecast.

## Limitations & Future Scope
- **Limitations:** The forecasting model uses simple linear regression. It lacks advanced seasonality modeling (like ARIMA or Prophet). The dataset is historical and static.
- **Future Scope:** Implement real-time data streaming, add advanced deep-learning models for forecasting, and integrate an LLM API to generate natural language explanations dynamically.

## Team Members
- Pratiksha Ingale (Lead Developer / AI Agent Bob)

## References
- Pandas Documentation
- Streamlit Documentation
- Scikit-learn Documentation
