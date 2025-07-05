"""
SmartPay Analytics - Data Processing Script
==========================================

This script loads, processes, and analyzes SmartPay mock data for use in dashboards and reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class SmartPayDataProcessor:
    def __init__(self, users_file, transactions_file, activity_file):
        self.users_file = users_file
        self.transactions_file = transactions_file
        self.activity_file = activity_file
        self.users_df = None
        self.transactions_df = None
        self.activity_df = None
        self.load_data()

    def load_data(self):
        self.users_df = pd.read_csv(self.users_file)
        self.transactions_df = pd.read_csv(self.transactions_file)
        self.activity_df = pd.read_csv(self.activity_file)
        self.users_df['signup_date'] = pd.to_datetime(self.users_df['signup_date'])
        self.transactions_df['timestamp'] = pd.to_datetime(self.transactions_df['timestamp'])
        self.activity_df['last_transaction_date'] = pd.to_datetime(self.activity_df['last_transaction_date'])
        print("✅ Data loaded successfully!")

    def get_user_metrics(self):
        metrics = {}
        metrics['total_users'] = len(self.users_df)
        three_months_ago = datetime.now() - timedelta(days=90)
        recent_tx = self.transactions_df[self.transactions_df['timestamp'] >= three_months_ago]
        metrics['mau_last_3_months'] = recent_tx['user_id'].nunique()
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_tx_30d = self.transactions_df[self.transactions_df['timestamp'] >= thirty_days_ago]
        metrics['dau_last_30_days'] = recent_tx_30d['user_id'].nunique()
        churned = self.activity_df[self.activity_df['last_transaction_date'] < thirty_days_ago]
        metrics['churn_rate'] = (len(churned) / len(self.activity_df)) * 100
        self.users_df['signup_month'] = self.users_df['signup_date'].dt.to_period('M')
        monthly_signups = self.users_df.groupby('signup_month').size()
        if len(monthly_signups) > 1:
            current_month = monthly_signups.iloc[-1]
            previous_month = monthly_signups.iloc[-2]
            metrics['growth_rate'] = ((current_month - previous_month) / previous_month) * 100
        else:
            metrics['growth_rate'] = 0
        return metrics

    def get_transaction_metrics(self):
        metrics = {}
        total_tx = len(self.transactions_df)
        successful_tx = len(self.transactions_df[self.transactions_df['status'] == 'Success'])
        metrics['success_rate'] = (successful_tx / total_tx) * 100
        successful_df = self.transactions_df[self.transactions_df['status'] == 'Success']
        metrics['avg_transaction_value'] = successful_df['amount'].mean()
        metrics['total_revenue'] = successful_df['amount'].sum()
        unique_users = self.transactions_df['user_id'].nunique()
        metrics['arpu'] = metrics['total_revenue'] / unique_users
        feature_metrics = self.transactions_df.groupby('feature').agg({
            'transaction_id': 'count',
            'amount': lambda x: x[self.transactions_df.loc[x.index, 'status'] == 'Success'].sum(),
            'status': lambda x: (x == 'Success').sum() / len(x) * 100
        }).rename(columns={
            'transaction_id': 'transaction_count',
            'amount': 'total_revenue',
            'status': 'success_rate'
        })
        metrics['feature_metrics'] = feature_metrics
        return metrics

    def get_funnel_metrics(self):
        funnel = {}
        app_opens = len(self.activity_df[self.activity_df['app_open_count'] > 0])
        funnel['app_opens'] = app_opens
        feature_used = self.transactions_df['user_id'].nunique()
        funnel['feature_used'] = feature_used
        funnel['app_to_feature_rate'] = (feature_used / app_opens) * 100 if app_opens else 0
        transaction_started = self.transactions_df['user_id'].nunique()
        funnel['transaction_started'] = transaction_started
        funnel['feature_to_transaction_rate'] = (transaction_started / feature_used) * 100 if feature_used else 0
        transaction_completed = self.transactions_df[self.transactions_df['status'] == 'Success']['user_id'].nunique()
        funnel['transaction_completed'] = transaction_completed
        funnel['transaction_success_rate'] = (transaction_completed / transaction_started) * 100 if transaction_started else 0
        funnel['overall_conversion_rate'] = (transaction_completed / app_opens) * 100 if app_opens else 0
        return funnel

    def get_feature_engagement(self):
        engagement = {}
        self.transactions_df['hour'] = self.transactions_df['timestamp'].dt.hour
        hourly_usage = self.transactions_df.groupby(['feature', 'hour']).size().unstack(fill_value=0)
        engagement['hourly_usage'] = hourly_usage
        self.transactions_df['day_of_week'] = self.transactions_df['timestamp'].dt.day_name()
        daily_usage = self.transactions_df.groupby(['feature', 'day_of_week']).size().unstack(fill_value=0)
        engagement['daily_usage'] = daily_usage
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_tx = self.transactions_df[self.transactions_df['timestamp'] >= thirty_days_ago]
        feature_retention = {}
        for feature in self.transactions_df['feature'].unique():
            total_users = self.transactions_df[self.transactions_df['feature'] == feature]['user_id'].nunique()
            retained_users = recent_tx[recent_tx['feature'] == feature]['user_id'].nunique()
            retention_rate = (retained_users / total_users) * 100 if total_users > 0 else 0
            feature_retention[feature] = retention_rate
        engagement['feature_retention'] = feature_retention
        return engagement

    def get_user_segmentation(self):
        segmentation = {}
        self.activity_df['activity_level'] = pd.cut(
            self.activity_df['days_active_per_month'],
            bins=[0, 10, 20, float('inf')],
            labels=['Low Activity', 'Medium Activity', 'High Activity']
        )
        activity_segments = self.activity_df['activity_level'].value_counts()
        segmentation['activity_segments'] = activity_segments
        user_revenue = self.transactions_df[self.transactions_df['status'] == 'Success'].groupby('user_id')['amount'].sum()
        user_revenue_percentiles = user_revenue.quantile([0.5, 0.8, 0.95])
        def categorize_user_value(revenue):
            if revenue >= user_revenue_percentiles[0.95]:
                return 'High Value'
            elif revenue >= user_revenue_percentiles[0.8]:
                return 'Medium Value'
            elif revenue >= user_revenue_percentiles[0.5]:
                return 'Low Value'
            else:
                return 'Minimal Value'
        user_revenue_df = user_revenue.reset_index()
        user_revenue_df['value_segment'] = user_revenue_df['amount'].apply(categorize_user_value)
        value_segments = user_revenue_df['value_segment'].value_counts()
        segmentation['value_segments'] = value_segments
        return segmentation

    def export_processed_data(self, output_dir='processed_data'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        user_summary = self.users_df.merge(self.activity_df, on='user_id', how='left')
        user_summary.to_csv(f'{output_dir}/user_summary.csv', index=False)
        transaction_summary = self.transactions_df.copy()
        transaction_summary.to_csv(f'{output_dir}/transaction_summary.csv', index=False)
        feature_metrics = self.get_transaction_metrics()['feature_metrics'].reset_index()
        feature_metrics.to_csv(f'{output_dir}/feature_metrics.csv', index=False)
        funnel = self.get_funnel_metrics()
        funnel_data = pd.DataFrame([
            {'stage': 'App Opens', 'count': funnel['app_opens']},
            {'stage': 'Feature Used', 'count': funnel['feature_used']},
            {'stage': 'Transaction Started', 'count': funnel['transaction_started']},
            {'stage': 'Transaction Completed', 'count': funnel['transaction_completed']}
        ])
        funnel_data.to_csv(f'{output_dir}/funnel_data.csv', index=False)
        print(f"✅ Processed data exported to {output_dir}/")

    def generate_insights_report(self):
        print("📊 SmartPay Analytics Insights Report")
        print("=" * 50)
        user_metrics = self.get_user_metrics()
        print("\n👥 USER OVERVIEW")
        print(f"Total Users: {user_metrics['total_users']:,}")
        print(f"Monthly Active Users (3 months): {user_metrics['mau_last_3_months']:,}")
        print(f"Daily Active Users (30 days): {user_metrics['dau_last_30_days']:,}")
        print(f"Churn Rate: {user_metrics['churn_rate']:.2f}%")
        print(f"Growth Rate: {user_metrics['growth_rate']:.2f}%")
        transaction_metrics = self.get_transaction_metrics()
        print("\n💰 TRANSACTION METRICS")
        print(f"Success Rate: {transaction_metrics['success_rate']:.2f}%")
        print(f"Average Transaction Value: ${transaction_metrics['avg_transaction_value']:.2f}")
        print(f"Total Revenue: ${transaction_metrics['total_revenue']:,.2f}")
        print(f"ARPU: ${transaction_metrics['arpu']:.2f}")
        print("\n🔧 FEATURE PERFORMANCE")
        feature_metrics = transaction_metrics['feature_metrics']
        for feature in feature_metrics.index:
            print(f"{feature}:")
            print(f"  - Transactions: {feature_metrics.loc[feature, 'transaction_count']:,}")
            print(f"  - Revenue: ${feature_metrics.loc[feature, 'total_revenue']:,.2f}")
            print(f"  - Success Rate: {feature_metrics.loc[feature, 'success_rate']:.2f}%")
        funnel = self.get_funnel_metrics()
        print("\n🔄 FUNNEL ANALYSIS")
        print(f"App Opens: {funnel['app_opens']:,}")
        print(f"Feature Used: {funnel['feature_used']:,} ({funnel['app_to_feature_rate']:.2f}%)")
        print(f"Transaction Started: {funnel['transaction_started']:,} ({funnel['feature_to_transaction_rate']:.2f}%)")
        print(f"Transaction Completed: {funnel['transaction_completed']:,} ({funnel['transaction_success_rate']:.2f}%)")
        print(f"Overall Conversion: {funnel['overall_conversion_rate']:.2f}%")
        segmentation = self.get_user_segmentation()
        print("\n👤 USER SEGMENTATION")
        print("Activity-based:")
        for segment, count in segmentation['activity_segments'].items():
            percentage = (count / len(self.activity_df)) * 100
            print(f"  {segment}: {count:,} ({percentage:.1f}%)")
        print("\nValue-based:")
        for segment, count in segmentation['value_segments'].items():
            percentage = (count / len(segmentation['value_segments'])) * 100
            print(f"  {segment}: {count:,} ({percentage:.1f}%)")


def main():
    processor = SmartPayDataProcessor(
        users_file='../smartpay_users.csv',
        transactions_file='../smartpay_transactions.csv',
        activity_file='../smartpay_app_activity.csv'
    )
    processor.generate_insights_report()
    processor.export_processed_data()
    print("\n🎉 Data processing completed successfully!")

if __name__ == "__main__":
    main() 