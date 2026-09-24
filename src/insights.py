import pandas as pd
from src.analysis import calculate_kpis, identify_risks_opportunities

def generate_insights(df):
    kpis = calculate_kpis(df)
    risks, opportunities = identify_risks_opportunities(df)
    
    insights = []
    
    # Overall Performance Insight
    margin = kpis['Profit Margin']
    if margin > 10:
        perf_rec = "Maintain pricing strategy and focus on customer retention."
    elif margin > 0:
        perf_rec = "Optimize shipping and operational costs to improve tight margins."
    else:
        perf_rec = "Immediate review of pricing and discount strategies required. Operating at a loss."
        
    insights.append({
        "OBSERVATION": f"Total revenue stands at ${kpis['Total Revenue']:,.2f} with a profit margin of {margin:.2f}%.",
        "DRIVER": "Overall sales volume vs. applied discounts and shipping costs.",
        "RISK/OPPORTUNITY": "Opportunity" if margin > 10 else "Risk",
        "RECOMMENDATION": perf_rec
    })
    
    # Add top risk and top opportunity from the analysis engine
    if risks:
        insights.append({
            "OBSERVATION": risks[0].split(':')[1].strip() if ':' in risks[0] else risks[0],
            "DRIVER": "High discount rates or low product demand in this segment.",
            "RISK/OPPORTUNITY": "Risk",
            "RECOMMENDATION": "Investigate root cause of losses. Consider reducing discounts or discontinuing highly unprofitable product lines."
        })
        
    if opportunities:
        insights.append({
            "OBSERVATION": opportunities[0].split(':')[1].strip() if ':' in opportunities[0] else opportunities[0],
            "DRIVER": "Strong customer demand and healthy margins.",
            "RISK/OPPORTUNITY": "Opportunity",
            "RECOMMENDATION": "Increase marketing spend in this specific area to capitalize on high profitability."
        })
        
    return insights

if __name__ == '__main__':
    from src.analysis import load_data
    df = load_data('data/cleaned_dataset.csv')
    for i in generate_insights(df):
        print(i)
