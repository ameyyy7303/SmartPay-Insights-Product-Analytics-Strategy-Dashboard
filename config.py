"""
SmartPay Analytics - Configuration Settings
==========================================

This module contains all configuration settings for the SmartPay Analytics project.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration class for SmartPay Analytics."""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    LOG_DIR = PROJECT_ROOT / "logs"
    REPORTS_DIR = PROJECT_ROOT / "reports"
    
    # File paths
    USERS_FILE = DATA_DIR / "smartpay_users.csv"
    TRANSACTIONS_FILE = DATA_DIR / "smartpay_transactions.csv"
    ACTIVITY_FILE = DATA_DIR / "smartpay_app_activity.csv"
    
    # Database configuration
    DATABASE_CONFIG = {
        'server': os.getenv('DB_SERVER', 'localhost'),
        'database': os.getenv('DB_NAME', 'smartpay_analytics'),
        'username': os.getenv('DB_USER', ''),
        'password': os.getenv('DB_PASSWORD', ''),
        'driver': os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
        'port': os.getenv('DB_PORT', '1433'),
        'timeout': int(os.getenv('DB_TIMEOUT', '30'))
    }
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Data processing settings
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '10000'))
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    CACHE_RESULTS = os.getenv('CACHE_RESULTS', 'True').lower() == 'true'
    
    # Analytics settings
    INSIGHT_THRESHOLDS = {
        'high_value_user_percentile': float(os.getenv('HIGH_VALUE_USER_PERCENTILE', '0.9')),
        'churn_risk_days': int(os.getenv('CHURN_RISK_DAYS', '30')),
        'success_rate_minimum': float(os.getenv('SUCCESS_RATE_MINIMUM', '0.8')),
        'session_duration_threshold': int(os.getenv('SESSION_DURATION_THRESHOLD', '300')),
        'page_views_threshold': int(os.getenv('PAGE_VIEWS_THRESHOLD', '5'))
    }
    
    # User segmentation settings
    SEGMENTATION_CONFIG = {
        'age_groups': {
            'young': (18, 25),
            'adult': (26, 35),
            'middle': (36, 45),
            'senior': (46, 65),
            'elderly': (66, 100)
        },
        'activity_levels': {
            'high': {'min_sessions': 20, 'min_duration': 60},
            'medium': {'min_sessions': 10, 'min_duration': 30},
            'low': {'min_sessions': 1, 'min_duration': 10}
        },
        'value_tiers': {
            'premium': {'min_revenue': 1000, 'min_transactions': 10},
            'regular': {'min_revenue': 100, 'min_transactions': 3},
            'casual': {'min_revenue': 0, 'min_transactions': 1}
        }
    }
    
    # Feature configuration
    FEATURES = {
        'Payment': {
            'category': 'Core',
            'launch_date': '2024-01-01',
            'success_threshold': 0.95
        },
        'Transfer': {
            'category': 'Core',
            'launch_date': '2024-01-01',
            'success_threshold': 0.90
        },
        'Bill Pay': {
            'category': 'Premium',
            'launch_date': '2024-02-01',
            'success_threshold': 0.85
        }
    }
    
    # Dashboard settings
    DASHBOARD_CONFIG = {
        'refresh_interval': int(os.getenv('DASHBOARD_REFRESH_INTERVAL', '900')),  # 15 minutes
        'max_data_points': int(os.getenv('MAX_DATA_POINTS', '10000')),
        'compression_level': os.getenv('COMPRESSION_LEVEL', 'High'),
        'retention_period': int(os.getenv('RETENTION_PERIOD', '90'))  # days
    }
    
    # Performance settings
    PERFORMANCE_CONFIG = {
        'max_memory_usage': int(os.getenv('MAX_MEMORY_USAGE', '2048')),  # MB
        'processing_timeout': int(os.getenv('PROCESSING_TIMEOUT', '300')),  # seconds
        'batch_size': int(os.getenv('BATCH_SIZE', '1000')),
        'enable_parallel_processing': os.getenv('ENABLE_PARALLEL_PROCESSING', 'True').lower() == 'true'
    }
    
    # Security settings
    SECURITY_CONFIG = {
        'encrypt_sensitive_data': os.getenv('ENCRYPT_SENSITIVE_DATA', 'True').lower() == 'true',
        'mask_pii': os.getenv('MASK_PII', 'True').lower() == 'true',
        'audit_logging': os.getenv('AUDIT_LOGGING', 'True').lower() == 'true',
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600'))  # seconds
    }
    
    # Email notification settings
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', ''),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'smtp_username': os.getenv('SMTP_USERNAME', ''),
        'smtp_password': os.getenv('SMTP_PASSWORD', ''),
        'from_email': os.getenv('FROM_EMAIL', 'analytics@smartpay.com'),
        'to_emails': os.getenv('TO_EMAILS', '').split(',') if os.getenv('TO_EMAILS') else []
    }
    
    # Alert settings
    ALERT_CONFIG = {
        'enable_alerts': os.getenv('ENABLE_ALERTS', 'True').lower() == 'true',
        'alert_thresholds': {
            'churn_rate': float(os.getenv('CHURN_RATE_THRESHOLD', '0.1')),
            'success_rate': float(os.getenv('SUCCESS_RATE_THRESHOLD', '0.9')),
            'revenue_drop': float(os.getenv('REVENUE_DROP_THRESHOLD', '0.2')),
            'user_growth': float(os.getenv('USER_GROWTH_THRESHOLD', '0.05'))
        },
        'notification_channels': os.getenv('NOTIFICATION_CHANNELS', 'email').split(',')
    }
    
    # Export settings
    EXPORT_CONFIG = {
        'formats': ['csv', 'json', 'excel'],
        'compression': os.getenv('EXPORT_COMPRESSION', 'gzip'),
        'include_metadata': os.getenv('INCLUDE_METADATA', 'True').lower() == 'true',
        'max_file_size': int(os.getenv('MAX_FILE_SIZE', '100'))  # MB
    }
    
    @classmethod
    def get_database_connection_string(cls) -> str:
        """Generate database connection string."""
        config = cls.DATABASE_CONFIG
        return (
            f"DRIVER={{{config['driver']}}};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"UID={config['username']};"
            f"PWD={config['password']};"
            f"TIMEOUT={config['timeout']};"
        )
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration settings."""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required directories
        required_dirs = [cls.DATA_DIR, cls.OUTPUT_DIR, cls.LOG_DIR]
        for directory in required_dirs:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                    validation_results['warnings'].append(f"Created directory: {directory}")
                except Exception as e:
                    validation_results['errors'].append(f"Cannot create directory {directory}: {e}")
                    validation_results['valid'] = False
        
        # Check required files
        required_files = [cls.USERS_FILE, cls.TRANSACTIONS_FILE, cls.ACTIVITY_FILE]
        for file_path in required_files:
            if not file_path.exists():
                validation_results['warnings'].append(f"Data file not found: {file_path}")
        
        # Validate database configuration
        if not cls.DATABASE_CONFIG['username'] or not cls.DATABASE_CONFIG['password']:
            validation_results['warnings'].append("Database credentials not configured")
        
        # Validate email configuration
        if cls.EMAIL_CONFIG['smtp_server'] and not cls.EMAIL_CONFIG['to_emails']:
            validation_results['warnings'].append("SMTP configured but no recipient emails specified")
        
        # Validate thresholds
        for threshold_name, threshold_value in cls.INSIGHT_THRESHOLDS.items():
            if threshold_value < 0:
                validation_results['errors'].append(f"Invalid threshold {threshold_name}: {threshold_value}")
                validation_results['valid'] = False
        
        return validation_results
    
    @classmethod
    def get_feature_config(cls, feature_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific feature."""
        return cls.FEATURES.get(feature_name)
    
    @classmethod
    def get_segmentation_config(cls, segment_type: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific segmentation type."""
        return cls.SEGMENTATION_CONFIG.get(segment_type)
    
    @classmethod
    def update_config(cls, **kwargs) -> None:
        """Update configuration settings."""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CACHE_RESULTS = False

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    CACHE_RESULTS = True
    SECURITY_CONFIG = {
        **Config.SECURITY_CONFIG,
        'encrypt_sensitive_data': True,
        'mask_pii': True,
        'audit_logging': True
    }

class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CACHE_RESULTS = False
    DATABASE_CONFIG = {
        **Config.DATABASE_CONFIG,
        'database': 'smartpay_analytics_test'
    }

# Configuration factory
def get_config(environment: str = None) -> Config:
    """Get configuration for the specified environment."""
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(environment.lower(), DevelopmentConfig)

# Global configuration instance
config = get_config()

if __name__ == "__main__":
    # Validate configuration
    validation = config.validate_config()
    
    print("Configuration Validation Results:")
    print(f"Valid: {validation['valid']}")
    
    if validation['errors']:
        print("\nErrors:")
        for error in validation['errors']:
            print(f"  - {error}")
    
    if validation['warnings']:
        print("\nWarnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if validation['valid']:
        print("\n✅ Configuration is valid!")
    else:
        print("\n❌ Configuration has errors!")
        exit(1) 