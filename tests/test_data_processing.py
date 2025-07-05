"""
Test suite for SmartPay Analytics data processing module.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the python directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from data_processing import SmartPayDataProcessor

class TestSmartPayDataProcessor:
    """Test cases for SmartPayDataProcessor class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        # Sample users data
        users_data = {
            'user_id': [1, 2, 3, 4, 5],
            'age': [25, 30, 35, 28, 42],
            'gender': ['M', 'F', 'M', 'F', 'M'],
            'location': ['NYC', 'LA', 'CHI', 'MIA', 'SEA'],
            'registration_date': [
                '2024-01-15', '2024-02-01', '2024-01-20', 
                '2024-02-10', '2024-01-05'
            ]
        }
        
        # Sample transactions data
        transactions_data = {
            'transaction_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'user_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            'amount': [100.0, 150.0, 200.0, 75.0, 300.0, 125.0, 80.0, 250.0, 180.0, 90.0],
            'status': ['Success', 'Success', 'Success', 'Failed', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success'],
            'feature': ['Payment', 'Transfer', 'Payment', 'Bill Pay', 'Transfer', 'Payment', 'Bill Pay', 'Transfer', 'Payment', 'Transfer'],
            'timestamp': [
                '2024-12-01 10:00:00', '2024-12-02 14:30:00', '2024-12-01 16:45:00',
                '2024-12-03 09:15:00', '2024-12-02 11:20:00', '2024-12-03 13:40:00',
                '2024-12-01 08:30:00', '2024-12-02 17:15:00', '2024-12-03 12:00:00',
                '2024-12-01 15:30:00'
            ]
        }
        
        # Sample activity data
        activity_data = {
            'user_id': [1, 2, 3, 4, 5],
            'session_duration': [45, 30, 60, 25, 40],
            'page_views': [8, 5, 12, 4, 7],
            'last_activity_date': [
                '2024-12-03', '2024-12-02', '2024-12-03', '2024-12-01', '2024-12-03'
            ],
            'login_count': [15, 8, 22, 6, 12]
        }
        
        return {
            'users': pd.DataFrame(users_data),
            'transactions': pd.DataFrame(transactions_data),
            'activity': pd.DataFrame(activity_data)
        }
    
    @pytest.fixture
    def processor(self, sample_data, tmp_path):
        """Create a processor instance with sample data."""
        # Create temporary CSV files
        users_file = tmp_path / "test_users.csv"
        transactions_file = tmp_path / "test_transactions.csv"
        activity_file = tmp_path / "test_activity.csv"
        
        sample_data['users'].to_csv(users_file, index=False)
        sample_data['transactions'].to_csv(transactions_file, index=False)
        sample_data['activity'].to_csv(activity_file, index=False)
        
        return SmartPayDataProcessor(
            users_file=str(users_file),
            transactions_file=str(transactions_file),
            activity_file=str(activity_file)
        )
    
    def test_initialization(self, processor):
        """Test processor initialization."""
        assert processor is not None
        assert processor.users_df is not None
        assert processor.transactions_df is not None
        assert processor.activity_df is not None
    
    def test_data_loading(self, processor, sample_data):
        """Test data loading from CSV files."""
        # Check users data
        assert len(processor.users_df) == len(sample_data['users'])
        assert list(processor.users_df.columns) == list(sample_data['users'].columns)
        
        # Check transactions data
        assert len(processor.transactions_df) == len(sample_data['transactions'])
        assert list(processor.transactions_df.columns) == list(sample_data['transactions'].columns)
        
        # Check activity data
        assert len(processor.activity_df) == len(sample_data['activity'])
        assert list(processor.activity_df.columns) == list(sample_data['activity'].columns)
    
    def test_data_cleaning(self, processor):
        """Test data cleaning functionality."""
        # Test that timestamps are converted to datetime
        assert pd.api.types.is_datetime64_any_dtype(processor.transactions_df['timestamp'])
        assert pd.api.types.is_datetime64_any_dtype(processor.users_df['registration_date'])
        assert pd.api.types.is_datetime64_any_dtype(processor.activity_df['last_activity_date'])
        
        # Test that numeric columns are properly typed
        assert pd.api.types.is_numeric_dtype(processor.transactions_df['amount'])
        assert pd.api.types.is_numeric_dtype(processor.users_df['age'])
        assert pd.api.types.is_numeric_dtype(processor.activity_df['session_duration'])
    
    def test_user_metrics(self, processor):
        """Test user metrics calculation."""
        metrics = processor.get_user_metrics()
        
        # Check that all required metrics are present
        required_metrics = [
            'total_users', 'mau_last_3_months', 'dau_last_7_days',
            'user_growth_rate', 'churn_rate', 'avg_session_duration',
            'avg_page_views', 'avg_login_count'
        ]
        
        for metric in required_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))
            assert metrics[metric] >= 0
    
    def test_transaction_metrics(self, processor):
        """Test transaction metrics calculation."""
        metrics = processor.get_transaction_metrics()
        
        # Check that all required metrics are present
        required_metrics = [
            'total_transactions', 'successful_transactions', 'failed_transactions',
            'success_rate', 'total_revenue', 'avg_transaction_value',
            'revenue_per_user', 'transactions_per_user'
        ]
        
        for metric in required_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))
            assert metrics[metric] >= 0
    
    def test_feature_metrics(self, processor):
        """Test feature metrics calculation."""
        metrics = processor.get_feature_metrics()
        
        # Check that metrics are calculated for each feature
        assert 'Payment' in metrics
        assert 'Transfer' in metrics
        assert 'Bill Pay' in metrics
        
        # Check that each feature has required metrics
        for feature in metrics:
            feature_metrics = metrics[feature]
            required_metrics = [
                'usage_count', 'success_rate', 'total_revenue',
                'avg_amount', 'user_count'
            ]
            
            for metric in required_metrics:
                assert metric in feature_metrics
                assert isinstance(feature_metrics[metric], (int, float))
                assert feature_metrics[metric] >= 0
    
    def test_user_segmentation(self, processor):
        """Test user segmentation functionality."""
        segments = processor.get_user_segments()
        
        # Check that segments are created
        assert 'segments' in segments
        assert 'segment_metrics' in segments
        
        # Check that segments have reasonable values
        assert len(segments['segments']) > 0
        assert len(segments['segment_metrics']) > 0
    
    def test_behavioral_analysis(self, processor):
        """Test behavioral analysis functionality."""
        behavior = processor.get_behavioral_analysis()
        
        # Check that behavioral metrics are calculated
        required_metrics = [
            'peak_hours', 'peak_days', 'avg_session_duration',
            'page_views_distribution', 'login_frequency'
        ]
        
        for metric in required_metrics:
            assert metric in behavior
    
    def test_data_validation(self, processor):
        """Test data validation functionality."""
        validation = processor.validate_data()
        
        # Check validation results
        assert 'is_valid' in validation
        assert 'issues' in validation
        assert 'completeness' in validation
        assert 'accuracy' in validation
        
        # Check that validation returns boolean
        assert isinstance(validation['is_valid'], bool)
        assert isinstance(validation['completeness'], float)
        assert isinstance(validation['accuracy'], float)
    
    def test_error_handling(self, tmp_path):
        """Test error handling for missing files."""
        # Test with non-existent files
        with pytest.raises(FileNotFoundError):
            SmartPayDataProcessor(
                users_file='nonexistent_users.csv',
                transactions_file='nonexistent_transactions.csv',
                activity_file='nonexistent_activity.csv'
            )
    
    def test_empty_data_handling(self, tmp_path):
        """Test handling of empty data files."""
        # Create empty CSV files
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("user_id,age\n")
        
        with pytest.raises(ValueError):
            SmartPayDataProcessor(
                users_file=str(empty_file),
                transactions_file=str(empty_file),
                activity_file=str(empty_file)
            )
    
    def test_data_export(self, processor, tmp_path):
        """Test data export functionality."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        # Test export functionality
        processor.export_processed_data(str(output_dir))
        
        # Check that files are created
        expected_files = [
            'user_summary.csv',
            'transaction_summary.csv',
            'feature_metrics.csv',
            'user_segments.csv'
        ]
        
        for file_name in expected_files:
            file_path = output_dir / file_name
            assert file_path.exists()
            assert file_path.stat().st_size > 0
    
    def test_performance_benchmark(self, processor):
        """Test performance benchmarking."""
        benchmark = processor.benchmark_performance()
        
        # Check benchmark results
        assert 'data_loading_time' in benchmark
        assert 'processing_time' in benchmark
        assert 'analytics_time' in benchmark
        assert 'total_time' in benchmark
        
        # Check that times are positive
        for time_key in benchmark:
            assert benchmark[time_key] >= 0
    
    def test_memory_usage(self, processor):
        """Test memory usage monitoring."""
        memory_usage = processor.get_memory_usage()
        
        # Check memory usage metrics
        assert 'users_memory' in memory_usage
        assert 'transactions_memory' in memory_usage
        assert 'activity_memory' in memory_usage
        assert 'total_memory' in memory_usage
        
        # Check that memory usage is positive
        for memory_key in memory_usage:
            assert memory_usage[memory_key] >= 0

class TestDataQuality:
    """Test cases for data quality checks."""
    
    def test_data_completeness(self, sample_data):
        """Test data completeness validation."""
        # Add some missing values
        sample_data['users'].loc[0, 'age'] = np.nan
        sample_data['transactions'].loc[0, 'amount'] = np.nan
        
        # Test completeness calculation
        users_completeness = 1 - (sample_data['users'].isnull().sum().sum() / sample_data['users'].size)
        transactions_completeness = 1 - (sample_data['transactions'].isnull().sum().sum() / sample_data['transactions'].size)
        
        assert users_completeness < 1.0
        assert transactions_completeness < 1.0
    
    def test_data_consistency(self, sample_data):
        """Test data consistency validation."""
        # Test that user IDs in transactions exist in users table
        user_ids_in_transactions = set(sample_data['transactions']['user_id'])
        user_ids_in_users = set(sample_data['users']['user_id'])
        
        # All transaction user IDs should exist in users table
        assert user_ids_in_transactions.issubset(user_ids_in_users)
    
    def test_data_accuracy(self, sample_data):
        """Test data accuracy validation."""
        # Test that amounts are positive
        assert all(sample_data['transactions']['amount'] > 0)
        
        # Test that ages are reasonable
        assert all(sample_data['users']['age'] >= 0)
        assert all(sample_data['users']['age'] <= 120)
        
        # Test that session durations are positive
        assert all(sample_data['activity']['session_duration'] > 0)

class TestIntegration:
    """Integration tests for the complete data processing pipeline."""
    
    def test_end_to_end_processing(self, processor):
        """Test complete end-to-end data processing."""
        # Run complete processing
        processor.process_all_data()
        
        # Verify that all metrics are calculated
        user_metrics = processor.get_user_metrics()
        transaction_metrics = processor.get_transaction_metrics()
        feature_metrics = processor.get_feature_metrics()
        
        # Check that metrics are reasonable
        assert user_metrics['total_users'] > 0
        assert transaction_metrics['total_transactions'] > 0
        assert len(feature_metrics) > 0
    
    def test_data_pipeline_consistency(self, processor):
        """Test consistency across the data pipeline."""
        # Process data
        processor.process_all_data()
        
        # Get metrics from different methods
        user_metrics = processor.get_user_metrics()
        transaction_metrics = processor.get_transaction_metrics()
        
        # Check consistency between user and transaction metrics
        # Total users should be consistent
        assert user_metrics['total_users'] == len(processor.users_df)
        
        # Transaction counts should be consistent
        assert transaction_metrics['total_transactions'] == len(processor.transactions_df)
    
    def test_performance_scalability(self, processor):
        """Test performance with larger datasets."""
        # Create larger dataset by duplicating existing data
        large_users = pd.concat([processor.users_df] * 10, ignore_index=True)
        large_transactions = pd.concat([processor.transactions_df] * 10, ignore_index=True)
        
        # Update processor with larger data
        processor.users_df = large_users
        processor.transactions_df = large_transactions
        
        # Test that processing still works
        start_time = datetime.now()
        processor.process_all_data()
        end_time = datetime.now()
        
        # Processing should complete within reasonable time (5 seconds)
        processing_time = (end_time - start_time).total_seconds()
        assert processing_time < 5.0

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 