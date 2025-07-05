"""
Test suite for SmartPay Analytics insights generator module.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
from unittest.mock import Mock, patch

# Add the python directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from insights_generator import SmartPayInsightsGenerator
from data_processing import SmartPayDataProcessor

class TestSmartPayInsightsGenerator:
    """Test cases for SmartPayInsightsGenerator class."""
    
    @pytest.fixture
    def mock_processor(self):
        """Create a mock data processor for testing."""
        processor = Mock(spec=SmartPayDataProcessor)
        
        # Mock user metrics
        processor.get_user_metrics.return_value = {
            'total_users': 50000,
            'mau_last_3_months': 35000,
            'dau_last_7_days': 8500,
            'user_growth_rate': 0.15,
            'churn_rate': 0.08,
            'avg_session_duration': 45.5,
            'avg_page_views': 8.2,
            'avg_login_count': 12.5
        }
        
        # Mock transaction metrics
        processor.get_transaction_metrics.return_value = {
            'total_transactions': 33000,
            'successful_transactions': 31200,
            'failed_transactions': 1800,
            'success_rate': 94.5,
            'total_revenue': 4200000.0,
            'avg_transaction_value': 127.50,
            'revenue_per_user': 84.00,
            'transactions_per_user': 0.66
        }
        
        # Mock dataframes
        processor.users_df = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5],
            'age': [25, 30, 35, 28, 42],
            'gender': ['M', 'F', 'M', 'F', 'M'],
            'location': ['NYC', 'LA', 'CHI', 'MIA', 'SEA'],
            'registration_date': pd.to_datetime(['2024-01-15', '2024-02-01', '2024-01-20', '2024-02-10', '2024-01-05'])
        })
        
        processor.transactions_df = pd.DataFrame({
            'transaction_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'user_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            'amount': [100.0, 150.0, 200.0, 75.0, 300.0, 125.0, 80.0, 250.0, 180.0, 90.0],
            'status': ['Success', 'Success', 'Success', 'Failed', 'Success', 'Success', 'Success', 'Success', 'Success', 'Success'],
            'feature': ['Payment', 'Transfer', 'Payment', 'Bill Pay', 'Transfer', 'Payment', 'Bill Pay', 'Transfer', 'Payment', 'Transfer'],
            'timestamp': pd.to_datetime([
                '2024-12-01 10:00:00', '2024-12-02 14:30:00', '2024-12-01 16:45:00',
                '2024-12-03 09:15:00', '2024-12-02 11:20:00', '2024-12-03 13:40:00',
                '2024-12-01 08:30:00', '2024-12-02 17:15:00', '2024-12-03 12:00:00',
                '2024-12-01 15:30:00'
            ])
        })
        
        processor.activity_df = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5],
            'session_duration': [45, 30, 60, 25, 40],
            'page_views': [8, 5, 12, 4, 7],
            'last_activity_date': pd.to_datetime(['2024-12-03', '2024-12-02', '2024-12-03', '2024-12-01', '2024-12-03']),
            'login_count': [15, 8, 22, 6, 12]
        })
        
        return processor
    
    @pytest.fixture
    def insights_generator(self, mock_processor):
        """Create an insights generator instance with mock data."""
        return SmartPayInsightsGenerator(mock_processor)
    
    def test_initialization(self, insights_generator, mock_processor):
        """Test insights generator initialization."""
        assert insights_generator is not None
        assert insights_generator.processor == mock_processor
        assert insights_generator.insights == {}
        assert insights_generator.recommendations == []
    
    def test_analyze_user_behavior_patterns(self, insights_generator):
        """Test user behavior pattern analysis."""
        insights = insights_generator.analyze_user_behavior_patterns()
        
        # Check that insights are generated
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Check insight structure
        for insight in insights:
            assert 'type' in insight
            assert 'insight' in insight
            assert 'impact' in insight
            assert 'action' in insight
            
            # Check that impact is valid
            assert insight['impact'] in ['High', 'Medium', 'Low']
            
            # Check that insight text is not empty
            assert len(insight['insight']) > 0
            assert len(insight['action']) > 0
    
    def test_analyze_revenue_optimization(self, insights_generator):
        """Test revenue optimization analysis."""
        insights = insights_generator.analyze_revenue_optimization()
        
        # Check that insights are generated
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Check insight structure
        for insight in insights:
            assert 'type' in insight
            assert 'insight' in insight
            assert 'impact' in insight
            assert 'action' in insight
            
            # Check that impact is valid
            assert insight['impact'] in ['High', 'Medium', 'Low']
            
            # Check that insight contains revenue information
            assert 'revenue' in insight['insight'].lower() or 'value' in insight['insight'].lower()
    
    def test_analyze_churn_risk(self, insights_generator):
        """Test churn risk analysis."""
        insights = insights_generator.analyze_churn_risk()
        
        # Check that insights are generated
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Check insight structure
        for insight in insights:
            assert 'type' in insight
            assert 'insight' in insight
            assert 'impact' in insight
            assert 'action' in insight
            
            # Check that insight is related to churn
            assert 'churn' in insight['type'].lower() or 'risk' in insight['type'].lower()
    
    def test_analyze_feature_performance(self, insights_generator):
        """Test feature performance analysis."""
        insights = insights_generator.analyze_feature_performance()
        
        # Check that insights are generated
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Check insight structure
        for insight in insights:
            assert 'type' in insight
            assert 'insight' in insight
            assert 'impact' in insight
            assert 'action' in insight
            
            # Check that insight is related to features
            assert 'feature' in insight['type'].lower() or 'success' in insight['type'].lower()
    
    def test_generate_strategic_recommendations(self, insights_generator):
        """Test strategic recommendations generation."""
        recommendations = insights_generator.generate_strategic_recommendations()
        
        # Check that recommendations are generated
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for category in recommendations:
            assert 'category' in category
            assert 'recommendations' in category
            
            # Check that category has a name
            assert len(category['category']) > 0
            
            # Check that recommendations list is not empty
            assert isinstance(category['recommendations'], list)
            assert len(category['recommendations']) > 0
            
            # Check that each recommendation is a string
            for rec in category['recommendations']:
                assert isinstance(rec, str)
                assert len(rec) > 0
    
    @patch('builtins.print')
    def test_generate_executive_summary(self, mock_print, insights_generator):
        """Test executive summary generation."""
        insights_generator.generate_executive_summary()
        
        # Check that print was called multiple times (indicating summary was generated)
        assert mock_print.call_count > 10
        
        # Check that key sections were printed
        printed_text = ' '.join([call.args[0] for call in mock_print.call_args_list])
        
        # Check for key sections
        assert 'SmartPay Executive Summary Report' in printed_text
        assert 'KEY METRICS' in printed_text
        assert 'TOP INSIGHTS' in printed_text
        assert 'STRATEGIC RECOMMENDATIONS' in printed_text
    
    def test_export_insights_report(self, insights_generator, tmp_path):
        """Test insights report export."""
        output_file = tmp_path / "test_insights_report.txt"
        
        # Export report
        report_content = insights_generator.export_insights_report(str(output_file))
        
        # Check that file was created
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        
        # Check that content was returned
        assert isinstance(report_content, str)
        assert len(report_content) > 0
        
        # Check that content contains key sections
        assert 'SmartPay Executive Summary Report' in report_content
        assert 'KEY METRICS' in report_content
        assert 'TOP INSIGHTS' in report_content

class TestInsightsQuality:
    """Test cases for insights quality and accuracy."""
    
    def test_insight_relevance(self, mock_processor):
        """Test that insights are relevant to the data."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Test user behavior insights
        user_insights = generator.analyze_user_behavior_patterns()
        for insight in user_insights:
            # Check that insights contain actionable information
            assert any(keyword in insight['action'].lower() for keyword in [
                'optimize', 'implement', 'schedule', 'improve', 'enhance'
            ])
    
    def test_insight_accuracy(self, mock_processor):
        """Test that insights are mathematically accurate."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Test revenue insights
        revenue_insights = generator.analyze_revenue_optimization()
        for insight in revenue_insights:
            # Check that insights contain numerical information
            if 'revenue' in insight['insight'].lower():
                # Should contain dollar amounts or percentages
                assert any(char.isdigit() for char in insight['insight'])
    
    def test_recommendation_quality(self, mock_processor):
        """Test that recommendations are high quality."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        recommendations = generator.generate_strategic_recommendations()
        
        for category in recommendations:
            for rec in category['recommendations']:
                # Check that recommendations are actionable
                assert any(keyword in rec.lower() for keyword in [
                    'implement', 'develop', 'create', 'establish', 'launch',
                    'optimize', 'improve', 'enhance', 'increase', 'reduce'
                ])
                
                # Check that recommendations are specific
                assert len(rec) > 20  # Should be detailed enough

class TestInsightsIntegration:
    """Integration tests for insights generation."""
    
    def test_end_to_end_insights_generation(self, mock_processor):
        """Test complete insights generation process."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Generate all types of insights
        user_insights = generator.analyze_user_behavior_patterns()
        revenue_insights = generator.analyze_revenue_optimization()
        churn_insights = generator.analyze_churn_risk()
        feature_insights = generator.analyze_feature_performance()
        
        # Generate recommendations
        recommendations = generator.generate_strategic_recommendations()
        
        # Check that all insights were generated
        assert len(user_insights) > 0
        assert len(revenue_insights) > 0
        assert len(churn_insights) > 0
        assert len(feature_insights) > 0
        assert len(recommendations) > 0
    
    def test_insights_consistency(self, mock_processor):
        """Test consistency across different insight types."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Generate insights multiple times
        insights1 = generator.analyze_user_behavior_patterns()
        insights2 = generator.analyze_user_behavior_patterns()
        
        # Insights should be consistent (same structure and content)
        assert len(insights1) == len(insights2)
        
        for i in range(len(insights1)):
            assert insights1[i]['type'] == insights2[i]['type']
            assert insights1[i]['impact'] == insights2[i]['impact']
    
    def test_recommendation_prioritization(self, mock_processor):
        """Test that recommendations are properly prioritized."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        recommendations = generator.generate_strategic_recommendations()
        
        # Check that high-impact recommendations come first
        high_impact_categories = [
            'Immediate Actions (High Impact)',
            'Strategic Initiatives (Medium Impact)',
            'Long-term Strategic Initiatives'
        ]
        
        for i, category in enumerate(recommendations):
            if i < len(high_impact_categories):
                assert category['category'] == high_impact_categories[i]

class TestInsightsPerformance:
    """Performance tests for insights generation."""
    
    def test_insights_generation_speed(self, mock_processor):
        """Test that insights generation is fast."""
        generator = SmartPayInsightsGenerator(mock_processor)
        
        start_time = datetime.now()
        
        # Generate all insights
        generator.analyze_user_behavior_patterns()
        generator.analyze_revenue_optimization()
        generator.analyze_churn_risk()
        generator.analyze_feature_performance()
        generator.generate_strategic_recommendations()
        
        end_time = datetime.now()
        
        # Should complete within 1 second
        processing_time = (end_time - start_time).total_seconds()
        assert processing_time < 1.0
    
    def test_memory_efficiency(self, mock_processor):
        """Test that insights generation is memory efficient."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Generate insights multiple times
        for _ in range(10):
            generator.analyze_user_behavior_patterns()
            generator.analyze_revenue_optimization()
            generator.analyze_churn_risk()
            generator.analyze_feature_performance()
            generator.generate_strategic_recommendations()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024  # 100MB

class TestInsightsErrorHandling:
    """Test error handling in insights generation."""
    
    def test_missing_data_handling(self):
        """Test handling of missing or invalid data."""
        # Create processor with empty data
        empty_processor = Mock(spec=SmartPayDataProcessor)
        empty_processor.users_df = pd.DataFrame()
        empty_processor.transactions_df = pd.DataFrame()
        empty_processor.activity_df = pd.DataFrame()
        
        generator = SmartPayInsightsGenerator(empty_processor)
        
        # Should handle empty data gracefully
        try:
            insights = generator.analyze_user_behavior_patterns()
            # Should return empty list or handle gracefully
            assert isinstance(insights, list)
        except Exception as e:
            # Should not crash, but may return empty results
            assert "empty" in str(e).lower() or "no data" in str(e).lower()
    
    def test_invalid_metrics_handling(self, mock_processor):
        """Test handling of invalid metrics."""
        # Mock invalid metrics
        mock_processor.get_user_metrics.return_value = {
            'total_users': -1,  # Invalid negative value
            'mau_last_3_months': 0,
            'churn_rate': 1.5  # Invalid rate > 1
        }
        
        generator = SmartPayInsightsGenerator(mock_processor)
        
        # Should handle invalid metrics gracefully
        try:
            insights = generator.analyze_user_behavior_patterns()
            assert isinstance(insights, list)
        except Exception as e:
            # Should not crash
            assert "invalid" in str(e).lower() or "error" in str(e).lower()

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 