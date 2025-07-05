# SmartPay Analytics - Setup & Usage Guide

## 🚀 Quick Start

This guide will help you set up and run the SmartPay Analytics dashboard project end-to-end.

---

## 📋 Prerequisites

### **Required Software**
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Power BI Desktop** - [Download here](https://powerbi.microsoft.com/desktop/)
- **SQL Server Management Studio** (or any SQL client) - [Download here](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)
- **Microsoft Excel** (for additional analysis)

### **Python Dependencies**
All required Python packages are listed in `python/requirements.txt`

---

## 🛠️ Installation Steps

### **Step 1: Clone/Download Project**
```bash
# If using git
git clone <repository-url>
cd "SmartPay Insights Product Analytics & Strategy Dashboard"

# Or download and extract the ZIP file
```

### **Step 2: Set Up Python Environment**
```bash
# Navigate to python directory
cd python

# Create virtual environment (recommended)
python -m venv smartpay_env

# Activate virtual environment
# On Windows:
smartpay_env\Scripts\activate
# On macOS/Linux:
source smartpay_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 3: Verify Data Files**
Ensure these CSV files are in the project root:
- `smartpay_users.csv`
- `smartpay_transactions.csv`
- `smartpay_app_activity.csv`

### **Step 4: Run Data Processing**
```bash
# From the python directory
python data_processing.py
```

This will:
- Load and validate the data
- Generate insights report
- Export processed data for Power BI

### **Step 5: Generate Business Insights**
```bash
# From the python directory
python insights_generator.py
```

This will:
- Analyze user behavior patterns
- Generate strategic recommendations
- Create executive summary report

---

## 📊 Power BI Dashboard Setup

### **Step 1: Import Data**
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Import the processed CSV files from `python/processed_data/`:
   - `user_summary.csv`
   - `transaction_summary.csv`
   - `feature_metrics.csv`
   - `funnel_data.csv`

### **Step 2: Set Up Data Model**
1. Go to "Model" view
2. Create relationships:
   - `user_summary[user_id]` → `transaction_summary[user_id]`
   - `user_summary[user_id]` → `feature_metrics[user_id]`

### **Step 3: Create Calculated Measures (DAX)**
Copy and paste these DAX formulas:

```dax
// Total Users
Total Users = COUNTROWS(user_summary)

// Monthly Active Users
MAU = CALCULATE(
    DISTINCTCOUNT(transaction_summary[user_id]),
    DATESINPERIOD(transaction_summary[timestamp], TODAY(), -30, DAY)
)

// Success Rate
Success Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(transaction_summary), transaction_summary[status] = "Success"),
    COUNTROWS(transaction_summary),
    0
)

// Average Transaction Value
ATV = 
CALCULATE(
    AVERAGE(transaction_summary[amount]),
    transaction_summary[status] = "Success"
)

// Revenue per User
ARPU = 
DIVIDE(
    CALCULATE(SUM(transaction_summary[amount]), transaction_summary[status] = "Success"),
    DISTINCTCOUNT(transaction_summary[user_id]),
    0
)
```

### **Step 4: Create Dashboard Pages**
Follow the detailed specifications in `powerbi/SmartPay_Dashboard_Design.md`

### **Step 5: Apply Styling**
- **Theme:** Modern professional
- **Primary Color:** #1E88E5 (Blue)
- **Success Color:** #4CAF50 (Green)
- **Warning Color:** #FF9800 (Orange)
- **Error Color:** #F44336 (Red)

---

## 📈 Running the Analysis

### **Option 1: Python Scripts (Recommended)**
```bash
# Run complete analysis
cd python
python data_processing.py
python insights_generator.py
```

### **Option 2: SQL Queries**
1. Import CSV files into your SQL database
2. Run queries from `sql/kpi_calculations.sql`
3. Export results for Power BI

### **Option 3: Excel Analysis**
1. Open CSV files in Excel
2. Use pivot tables for analysis
3. Create charts and dashboards

---

## 📊 Understanding the Output

### **Generated Reports**
- **Console Output:** Real-time insights and metrics
- **Processed Data:** CSV files ready for Power BI
- **Executive Summary:** `reports/stakeholder_summary.md`
- **Insights Report:** `python/smartpay_insights_report.txt`

### **Key Metrics Explained**
- **MAU (Monthly Active Users):** Users who made transactions in last 30 days
- **DAU (Daily Active Users):** Users who made transactions in last 24 hours
- **Churn Rate:** Percentage of users inactive for 30+ days
- **Success Rate:** Percentage of successful transactions
- **ARPU (Average Revenue Per User):** Total revenue divided by active users

### **Dashboard Pages**
1. **User Overview:** Demographics, growth, and activity
2. **Transaction Trends:** Performance, revenue, and success rates
3. **Feature Engagement:** Usage patterns and adoption
4. **Strategy & Recommendations:** Business insights and actions

---

## 🔧 Customization Options

### **Modify Data Sources**
Edit file paths in `python/data_processing.py`:
```python
processor = SmartPayDataProcessor(
    users_file='path/to/your/users.csv',
    transactions_file='path/to/your/transactions.csv',
    activity_file='path/to/your/activity.csv'
)
```

### **Add New Metrics**
Create new DAX measures in Power BI:
```dax
// Custom Metric Example
Custom Metric = 
CALCULATE(
    [Your Calculation],
    [Your Filters]
)
```

### **Modify Visualizations**
- Change chart types in Power BI
- Adjust colors and formatting
- Add new filters and slicers

### **Extend Analysis**
Add new analysis methods in `python/insights_generator.py`:
```python
def analyze_custom_metric(self):
    """Add your custom analysis here."""
    pass
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Python Errors**
```bash
# If you get import errors
pip install --upgrade pip
pip install -r requirements.txt

# If you get file not found errors
# Check that CSV files are in the correct location
```

#### **Power BI Issues**
- **Data not loading:** Check file paths and formats
- **Relationships not working:** Verify column names match
- **Visualizations not updating:** Refresh data source

#### **SQL Errors**
- **Syntax errors:** Use SQL Server compatible syntax from `sql/kpi_calculations.sql`
- **Date functions:** Ensure your database supports the date functions used

### **Performance Optimization**
- **Large datasets:** Use data sampling for development
- **Slow queries:** Add indexes to database tables
- **Power BI performance:** Use incremental refresh for large datasets

---

## 📚 Additional Resources

### **Documentation**
- `README.md` - Project overview
- `sql/kpi_calculations.sql` - SQL analysis queries
- `powerbi/SmartPay_Dashboard_Design.md` - Dashboard specifications
- `reports/stakeholder_summary.md` - Executive summary

### **Learning Resources**
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [DAX Reference](https://docs.microsoft.com/en-us/dax/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQL Tutorial](https://www.w3schools.com/sql/)

### **Best Practices**
- **Data Quality:** Always validate your data before analysis
- **Documentation:** Keep notes of your analysis process
- **Version Control:** Use git for tracking changes
- **Backup:** Keep backups of your original data

---

## 🎯 Next Steps

### **Immediate Actions**
1. Run the analysis scripts
2. Review the generated insights
3. Set up the Power BI dashboard
4. Share results with stakeholders

### **Advanced Features**
1. **Real-time Data:** Set up automated data refresh
2. **Alerts:** Configure automated alerts for key metrics
3. **Predictive Analytics:** Add machine learning models
4. **Competitive Analysis:** Integrate external data sources

### **Deployment**
1. **Power BI Service:** Publish dashboard to Power BI Service
2. **Scheduled Refresh:** Set up automatic data refresh
3. **User Access:** Configure permissions and sharing
4. **Training:** Conduct user training sessions

---

## 📞 Support

### **Getting Help**
- **Documentation:** Check this guide and project files
- **Issues:** Create an issue in the project repository
- **Questions:** Contact the analytics team

### **Contributing**
- **Code:** Submit pull requests for improvements
- **Documentation:** Help improve this guide
- **Feedback:** Share your experience and suggestions

---

*This setup guide provides everything you need to get started with SmartPay Analytics. Follow the steps in order for best results.*

**Last Updated:** January 2025  
**Version:** 1.0  
**Maintained by:** Product Analytics Team 