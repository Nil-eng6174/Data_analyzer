import pandas as pd
import numpy as np

def load_data(filepath='data/cleaned_dataset.csv'):
    df = pd.read_csv(filepath)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

# --- PHASE 5: KPI ENGINE ---
def calculate_kpis(df):
    kpis = {
        'Total Revenue': df['sales'].sum(),
        'Total Profit': df['profit'].sum(),
        'Total Orders': df['order_id'].nunique(),
        'Total Customers': df['customer_id'].nunique(),
        'Average Order Value': df['sales'].sum() / df['order_id'].nunique() if df['order_id'].nunique() > 0 else 0,
        'Profit Margin': (df['profit'].sum() / df['sales'].sum() * 100) if df['sales'].sum() > 0 else 0,
        'Units Sold': df['quantity'].sum()
    }
    return kpis

# --- PHASE 6: TREND ANALYSIS ---
def get_revenue_profit_trend(df, freq='M'):
    # freq can be 'D', 'W', 'M', 'Q', 'Y'
    trend = df.set_index('order_date').resample(freq)[['sales', 'profit']].sum().reset_index()
    return trend

def get_category_trend(df, freq='M'):
    trend = df.groupby([pd.Grouper(key='order_date', freq=freq), 'category'])['sales'].sum().reset_index()
    return trend

# --- PHASE 7: DRIVER ANALYSIS ---
def get_drivers(df):
    # Drivers for profit
    category_profit = df.groupby('category')['profit'].sum().sort_values(ascending=False).to_dict()
    region_profit = df.groupby('region')['profit'].sum().sort_values(ascending=False).to_dict()
    
    return {
        'Category Profit': category_profit,
        'Region Profit': region_profit
    }

# --- PHASE 8: RISKS AND OPPORTUNITIES ---
def identify_risks_opportunities(df):
    risks = []
    opportunities = []
    
    # Analyze by Sub-Category
    sub_cat = df.groupby('sub_category').agg({
        'sales': 'sum',
        'profit': 'sum',
        'discount': 'mean'
    }).reset_index()
    
    for _, row in sub_cat.iterrows():
        if row['profit'] < 0:
            risks.append(f"Risk: Sub-Category '{row['sub_category']}' is operating at a loss (Profit: ${row['profit']:.2f}, Avg Discount: {row['discount']*100:.2f}%).")
        elif row['profit'] > 50000 and row['sales'] > 200000:
            opportunities.append(f"Opportunity: Sub-Category '{row['sub_category']}' is highly profitable. Consider scaling marketing here.")
            
    # Analyze by Region
    region_prof = df.groupby('region')['profit'].sum().reset_index()
    worst_region = region_prof.loc[region_prof['profit'].idxmin()]
    best_region = region_prof.loc[region_prof['profit'].idxmax()]
    
    if worst_region['profit'] < 0:
        risks.append(f"Risk: Region '{worst_region['region']}' is making a net loss.")
    else:
        risks.append(f"Risk: Region '{worst_region['region']}' has the lowest profit (${worst_region['profit']:.2f}). Investigate drivers.")
        
    opportunities.append(f"Opportunity: Region '{best_region['region']}' is performing best. Replicate its strategy.")
    
    return risks, opportunities

if __name__ == '__main__':
    df = load_data()
    print("KPIs:", calculate_kpis(df))
    print("Risks:", identify_risks_opportunities(df)[0])
    print("Opportunities:", identify_risks_opportunities(df)[1])
