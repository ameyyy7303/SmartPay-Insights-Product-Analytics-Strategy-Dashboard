"""
SmartPay Analytics - Business Insights Generator
===============================================

This module generates business insights and strategic recommendations based on data analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_processing import SmartPayDataProcessor

class SmartPayInsightsGenerator:
    """Generate business insights and strategic recommendations."""
    
    def __init__(self, data_processor):
        self.processor = data_processor
        self.insights = {}
        self.recommendations = []
    
    def analyze_user_behavior_patterns(self):
        """Analyze user behavior patterns and generate insights."""
        insights = []
        
        # Analyze peak transaction times
        self.processor.transactions_df['hour'] = self.processor.transactions_df['timestamp'].dt.hour
        hourly_transactions = self.processor.transactions_df.groupby('hour').size()
        peak_hour = hourly_transactions.idxmax()
        peak_count = hourly_transactions.max()
        
        insights.append({
            'type': 'Peak Usage Time',
            'insight': f'Peak transaction activity occurs at {peak_hour}:00 with {peak_count} transactions',
            'impact': 'High',
            'action': 'Optimize server capacity and support during peak hours'
        })
        
        # Analyze day-of-week patterns
        self.processor.transactions_df['day_of_week'] = self.processor.transactions_df['timestamp'].dt.day_name()
        daily_transactions = self.processor.transactions_df.groupby('day_of_week').size()
        busiest_day = daily_transactions.idxmax()
        slowest_day = daily_transactions.idxmin()
        
        insights.append({
            'type': 'Weekly Pattern',
            'insight': f'{busiest_day} is the busiest day, {slowest_day} is the slowest',
            'impact': 'Medium',
            'action': 'Schedule promotions and maintenance accordingly'
        })
        
        return insights
    
    def analyze_revenue_optimization(self):
        """Analyze revenue optimization opportunities."""
        insights = []
        
        # High-value user analysis
        user_revenue = self.processor.transactions_df[
            self.processor.transactions_df['status'] == 'Success'
        ].groupby('user_id')['amount'].sum()
        
        top_10_percent = user_revenue.quantile(0.9)
        high_value_users = user_revenue[user_revenue >= top_10_percent]
        
        insights.append({
            'type': 'High-Value Users',
            'insight': f'{len(high_value_users)} users (top 10%) generate {high_value_users.sum():,.2f} in revenue',
            'impact': 'High',
            'action': 'Implement VIP program and personalized offers for high-value users'
        })
        
        # Feature revenue analysis
        feature_revenue = self.processor.transactions_df[
            self.processor.transactions_df['status'] == 'Success'
        ].groupby('feature')['amount'].sum()
        
        highest_revenue_feature = feature_revenue.idxmax()
        highest_revenue = feature_revenue.max()
        
        insights.append({
            'type': 'Revenue by Feature',
            'insight': f'{highest_revenue_feature} generates the highest revenue: ${highest_revenue:,.2f}',
            'impact': 'High',
            'action': f'Invest in {highest_revenue_feature} feature development and marketing'
        })
        
        return insights
    
    def analyze_churn_risk(self):
        """Analyze churn risk and retention opportunities."""
        insights = []
        
        # Churn analysis by user segment
        user_activity = self.processor.activity_df.merge(
            self.processor.users_df[['user_id', 'age', 'location']], on='user_id'
        )
        
        # Days since last transaction
        user_activity['days_since_last'] = (
            datetime.now() - user_activity['last_transaction_date']
        ).dt.days
        
        # Identify at-risk users (7-30 days inactive)
        at_risk_users = user_activity[
            (user_activity['days_since_last'] >= 7) & 
            (user_activity['days_since_last'] <= 30)
        ]
        
        insights.append({
            'type': 'Churn Risk',
            'insight': f'{len(at_risk_users)} users are at risk of churning (7-30 days inactive)',
            'impact': 'High',
            'action': 'Implement re-engagement campaigns for at-risk users'
        })
        
        return insights
    
    def analyze_feature_performance(self):
        """Analyze feature performance and optimization opportunities."""
        insights = []
        
        # Feature success rates
        feature_success = self.processor.transactions_df.groupby('feature').agg({
            'status': lambda x: (x == 'Success').sum() / len(x) * 100
        }).rename(columns={'status': 'success_rate'})
        
        lowest_success_feature = feature_success['success_rate'].idxmin()
        lowest_success_rate = feature_success['success_rate'].min()
        
        insights.append({
            'type': 'Feature Success Rate',
            'insight': f'{lowest_success_feature} has the lowest success rate: {lowest_success_rate:.1f}%',
            'impact': 'High',
            'action': f'Investigate and optimize {lowest_success_feature} user experience'
        })
        
        return insights
    
    def generate_strategic_recommendations(self):
        """Generate strategic business recommendations."""
        recommendations = []
        
        # Collect all insights
        user_insights = self.analyze_user_behavior_patterns()
        revenue_insights = self.analyze_revenue_optimization()
        churn_insights = self.analyze_churn_risk()
        feature_insights = self.analyze_feature_performance()
        
        all_insights = user_insights + revenue_insights + churn_insights + feature_insights
        
        # Prioritize by impact
        high_impact_insights = [insight for insight in all_insights if insight['impact'] == 'High']
        medium_impact_insights = [insight for insight in all_insights if insight['impact'] == 'Medium']
        
        # Generate strategic recommendations
        recommendations.append({
            'category': 'Immediate Actions (High Impact)',
            'recommendations': [
                insight['action'] for insight in high_impact_insights[:5]
            ]
        })
        
        recommendations.append({
            'category': 'Strategic Initiatives (Medium Impact)',
            'recommendations': [
                insight['action'] for insight in medium_impact_insights[:5]
            ]
        })
        
        # Add general strategic recommendations
        general_recommendations = [
            'Implement A/B testing framework for feature optimization',
            'Develop customer lifetime value (CLV) prediction model',
            'Create personalized onboarding experience based on user segments',
            'Establish real-time monitoring dashboard for key metrics',
            'Launch referral program to increase user acquisition'
        ]
        
        recommendations.append({
            'category': 'Long-term Strategic Initiatives',
            'recommendations': general_recommendations
        })
        
        return recommendations
    
    def generate_executive_summary(self):
        """Generate executive summary report."""
        print("🎯 SmartPay Executive Summary Report")
        print("=" * 50)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Key Metrics Summary
        user_metrics = self.processor.get_user_metrics()
        transaction_metrics = self.processor.get_transaction_metrics()
        
        print("📊 KEY METRICS")
        print(f"• Total Users: {user_metrics['total_users']:,}")
        print(f"• Monthly Active Users: {user_metrics['mau_last_3_months']:,}")
        print(f"• Transaction Success Rate: {transaction_metrics['success_rate']:.1f}%")
        print(f"• Average Transaction Value: ${transaction_metrics['avg_transaction_value']:.2f}")
        print(f"• Total Revenue: ${transaction_metrics['total_revenue']:,.2f}")
        print(f"• Churn Rate: {user_metrics['churn_rate']:.1f}%")
        print()
        
        # Top Insights
        print("🔍 TOP INSIGHTS")
        user_insights = self.analyze_user_behavior_patterns()
        revenue_insights = self.analyze_revenue_optimization()
        
        top_insights = user_insights[:2] + revenue_insights[:2]
        for i, insight in enumerate(top_insights, 1):
            print(f"{i}. {insight['insight']}")
        print()
        
        # Strategic Recommendations
        print("🎯 STRATEGIC RECOMMENDATIONS")
        recommendations = self.generate_strategic_recommendations()
        
        for category in recommendations:
            print(f"\n{category['category']}:")
            for i, rec in enumerate(category['recommendations'][:3], 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "=" * 50)
        print("📈 NEXT STEPS")
        print("1. Review and prioritize recommendations")
        print("2. Assign ownership and timelines")
        print("3. Implement monitoring for key metrics")
        print("4. Schedule follow-up review in 30 days")
    
    def export_insights_report(self, filename='smartpay_insights_report.txt'):
        """Export insights report to file."""
        import sys
        from io import StringIO
        
        # Capture print output
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        
        # Generate report
        self.generate_executive_summary()
        
        # Restore stdout and save to file
        sys.stdout = old_stdout
        report_content = result.getvalue()
        
        with open(filename, 'w') as f:
            f.write(report_content)
        
        print(f"✅ Insights report exported to {filename}")
        return report_content

def main():
    """Main function to generate insights."""
    # Initialize data processor
    processor = SmartPayDataProcessor(
        users_file='../smartpay_users.csv',
        transactions_file='../smartpay_transactions.csv',
        activity_file='../smartpay_app_activity.csv'
    )
    
    # Initialize insights generator
    insights_generator = SmartPayInsightsGenerator(processor)
    
    # Generate and display insights
    insights_generator.generate_executive_summary()
    
    # Export report
    insights_generator.export_insights_report()
    
    print("\n🎉 Insights generation completed successfully!")

if __name__ == "__main__":
    main() 