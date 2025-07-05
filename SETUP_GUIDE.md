# SmartPay Analytics - Setup Guide

## Overview
This guide provides step-by-step instructions for setting up and running the SmartPay Analytics project on your local machine or server environment.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: At least 5GB free space
- **Network**: Internet connection for package installation

### Required Software
1. **Python 3.8+**: [Download from python.org](https://www.python.org/downloads/)
2. **Git**: [Download from git-scm.com](https://git-scm.com/downloads)
3. **Power BI Desktop**: [Download from Microsoft](https://powerbi.microsoft.com/desktop/)
4. **SQL Server Management Studio** (Optional): For database management
5. **Visual Studio Code** (Recommended): [Download from code.visualstudio.com](https://code.visualstudio.com/)

## Installation Steps

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/your-username/smartpay-analytics.git
cd smartpay-analytics

# Verify the project structure
ls -la
```

### Step 2: Set Up Python Environment
```bash
# Create a virtual environment
python -m venv smartpay_env

# Activate the virtual environment
# On Windows:
smartpay_env\Scripts\activate

# On macOS/Linux:
source smartpay_env/bin/activate

# Verify Python version
python --version
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import pandas, numpy, matplotlib; print('Dependencies installed successfully!')"
```

### Step 4: Configure Environment Variables
```bash
# Create environment file
cp .env.example .env

# Edit the environment file with your settings
# Windows:
notepad .env

# macOS/Linux:
nano .env
```

**Environment Variables to Configure**:
```env
# Database Configuration
DB_SERVER=localhost
DB_NAME=smartpay_analytics
DB_USER=your_username
DB_PASSWORD=your_password

# File Paths
DATA_DIR=./data
OUTPUT_DIR=./output
LOG_DIR=./logs

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Step 5: Prepare Data Files
```bash
# Create data directory
mkdir -p data

# Copy your CSV files to the data directory
# Ensure you have:
# - smartpay_users.csv
# - smartpay_transactions.csv
# - smartpay_app_activity.csv

# Verify data files
ls -la data/
```

## Running the Application

### Step 1: Data Processing
```bash
# Navigate to the python directory
cd python

# Run the data processing script
python data_processing.py

# Expected output:
# ✅ Data processing completed successfully!
# 📊 Generated analytics reports
# 📈 Calculated key metrics
```

### Step 2: Generate Business Insights
```bash
# Run the insights generator
python insights_generator.py

# Expected output:
# 🎯 SmartPay Executive Summary Report
# 📊 KEY METRICS
# 🔍 TOP INSIGHTS
# 🎯 STRATEGIC RECOMMENDATIONS
```

### Step 3: View Generated Reports
```bash
# Check the output directory for generated files
ls -la ../output/

# View the insights report
cat ../output/smartpay_insights_report.txt
```

## Power BI Dashboard Setup

### Step 1: Install Power BI Desktop
1. Download Power BI Desktop from Microsoft's official website
2. Install and launch the application
3. Sign in with your Microsoft account (optional but recommended)

### Step 2: Import Data
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to your data files and import:
   - `smartpay_users.csv`
   - `smartpay_transactions.csv`
   - `smartpay_app_activity.csv`

### Step 3: Build Dashboard
1. Follow the design specifications in `powerbi/SmartPay_Dashboard_Design.md`
2. Create the 5 dashboard pages as outlined
3. Implement the calculated measures and visualizations
4. Set up filters and interactions

### Step 4: Publish Dashboard
1. Click "Publish" in Power BI Desktop
2. Choose your Power BI workspace
3. Set up refresh schedule for data updates
4. Share with stakeholders

## Database Setup (Optional)

### SQL Server Setup
```sql
-- Create database
CREATE DATABASE smartpay_analytics;
GO

-- Use the database
USE smartpay_analytics;
GO

-- Run the analytics queries
-- Execute the contents of sql/analytics_queries.sql
```

### PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE smartpay_analytics;

-- Connect to database
\c smartpay_analytics

-- Run the analytics queries
-- Execute the contents of sql/analytics_queries.sql
```

## Testing the Setup

### Step 1: Run Test Suite
```bash
# Navigate to project root
cd ..

# Run tests
python -m pytest tests/ -v

# Expected output:
# ============================= test session starts ==============================
# collected X items
# tests/test_data_processing.py::test_data_loading PASSED
# tests/test_insights_generator.py::test_insights_generation PASSED
# ...
# ============================== X passed in Xs ===============================
```

### Step 2: Verify Data Quality
```bash
# Run data quality checks
python python/data_processing.py --validate

# Expected output:
# ✅ Data validation completed
# 📊 Data quality metrics:
# - Completeness: 98.5%
# - Accuracy: 99.2%
# - Consistency: 97.8%
```

### Step 3: Performance Test
```bash
# Run performance benchmark
python python/data_processing.py --benchmark

# Expected output:
# ⚡ Performance benchmark results:
# - Data loading: 2.3s
# - Processing: 8.7s
# - Analytics: 3.1s
# - Total time: 14.1s
```

## Troubleshooting

### Common Issues

#### Issue 1: Python Version Error
```bash
# Error: Python version 3.8+ required
# Solution: Update Python
python --version
# If < 3.8, download and install newer version
```

#### Issue 2: Package Installation Errors
```bash
# Error: Failed to install packages
# Solution: Update pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Issue 3: Data File Not Found
```bash
# Error: smartpay_users.csv not found
# Solution: Check file paths and permissions
ls -la data/
chmod 644 data/*.csv
```

#### Issue 4: Database Connection Error
```bash
# Error: Cannot connect to database
# Solution: Check connection settings
python -c "import pyodbc; print('Database driver available')"
```

#### Issue 5: Memory Issues
```bash
# Error: Out of memory
# Solution: Reduce data size or increase memory
# Edit data_processing.py to process data in chunks
```

### Getting Help

#### Check Logs
```bash
# View application logs
tail -f logs/smartpay_analytics.log

# Check error logs
grep ERROR logs/smartpay_analytics.log
```

#### Debug Mode
```bash
# Run in debug mode for detailed output
python python/data_processing.py --debug

# Set environment variable
export DEBUG=True
python python/data_processing.py
```

## Configuration Options

### Data Processing Settings
```python
# In data_processing.py, you can modify:
CHUNK_SIZE = 10000  # Process data in chunks
MAX_WORKERS = 4     # Number of parallel workers
CACHE_RESULTS = True # Cache intermediate results
```

### Analytics Settings
```python
# In insights_generator.py, you can modify:
INSIGHT_THRESHOLDS = {
    'high_value_user': 0.9,  # Top 10% users
    'churn_risk_days': 30,   # Days for churn calculation
    'success_rate_min': 0.8  # Minimum success rate
}
```

### Dashboard Settings
```python
# In Power BI, configure:
REFRESH_SCHEDULE = 'Daily'  # Data refresh frequency
RETENTION_PERIOD = 90       # Days to keep data
COMPRESSION_LEVEL = 'High'  # Data compression
```

## Security Considerations

### Data Protection
1. **Encrypt sensitive data** in transit and at rest
2. **Use environment variables** for credentials
3. **Implement access controls** for database and files
4. **Regular security updates** for dependencies

### Access Control
1. **Role-based permissions** for dashboard access
2. **Audit logging** for all data access
3. **Data masking** for sensitive information
4. **Session management** for web interfaces

## Performance Optimization

### Data Processing
1. **Use parallel processing** for large datasets
2. **Implement caching** for frequently accessed data
3. **Optimize SQL queries** with proper indexing
4. **Monitor memory usage** and optimize accordingly

### Dashboard Performance
1. **Incremental refresh** for large datasets
2. **Query optimization** with DAX measures
3. **Data compression** to reduce storage
4. **Caching strategies** for faster loading

## Maintenance

### Regular Tasks
1. **Daily**: Check data refresh status
2. **Weekly**: Review performance metrics
3. **Monthly**: Update dependencies and security patches
4. **Quarterly**: Review and optimize queries

### Backup Strategy
1. **Automated backups** of processed data
2. **Version control** for configuration files
3. **Disaster recovery** plan for critical systems
4. **Documentation updates** for changes

## Support and Resources

### Documentation
- [Project README](README.md)
- [API Documentation](docs/api.md)
- [User Guide](docs/user_guide.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

### Community
- [GitHub Issues](https://github.com/your-username/smartpay-analytics/issues)
- [Discussion Forum](https://github.com/your-username/smartpay-analytics/discussions)
- [Wiki](https://github.com/your-username/smartpay-analytics/wiki)

### Contact
- **Technical Support**: tech-support@smartpay.com
- **Project Lead**: project-lead@smartpay.com
- **Documentation**: docs@smartpay.com

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Status**: Production Ready 