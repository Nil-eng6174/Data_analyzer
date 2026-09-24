import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def prepare_forecast_data(df, freq='M'):
    """Prepares data for forecasting total sales."""
    # Group by date
    daily_sales = df.groupby('order_date')['sales'].sum().reset_index()
    monthly_sales = daily_sales.set_index('order_date').resample(freq).sum().reset_index()
    
    # Feature engineering
    monthly_sales['year'] = monthly_sales['order_date'].dt.year
    monthly_sales['month'] = monthly_sales['order_date'].dt.month
    monthly_sales['time_idx'] = np.arange(len(monthly_sales))
    
    return monthly_sales

def train_forecast_model(df):
    """Trains a simple linear regression model for forecasting."""
    monthly_sales = prepare_forecast_data(df)
    
    # Features and Target
    X = monthly_sales[['time_idx', 'month']]
    y = monthly_sales['sales']
    
    # Train/Test Split (last 6 months for testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2
    }
    
    return model, metrics, monthly_sales

def generate_future_forecast(model, last_time_idx, last_date, months=6):
    """Generates future sales predictions."""
    future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, months+1)]
    future_data = pd.DataFrame({
        'order_date': future_dates,
        'year': [d.year for d in future_dates],
        'month': [d.month for d in future_dates],
        'time_idx': [last_time_idx + i for i in range(1, months+1)]
    })
    
    future_data['predicted_sales'] = model.predict(future_data[['time_idx', 'month']])
    return future_data

if __name__ == '__main__':
    from src.analysis import load_data
    df = load_data('data/cleaned_dataset.csv')
    model, metrics, data = train_forecast_model(df)
    print("Metrics:", metrics)
    print("Forecast:", generate_future_forecast(model, data['time_idx'].max(), data['order_date'].max()))
