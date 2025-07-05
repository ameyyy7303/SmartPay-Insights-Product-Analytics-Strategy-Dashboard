-- =====================================================
-- SmartPay Analytics - KPI Calculations (SQL Server)
-- =====================================================

-- 1. USER OVERVIEW KPIs
-- =====================================================

-- Total Users Count
SELECT COUNT(*) as total_users FROM smartpay_users;

-- Monthly Active Users (MAU) - Last 3 months
SELECT 
    FORMAT(t.timestamp, 'yyyy-MM') as month,
    COUNT(DISTINCT t.user_id) as monthly_active_users
FROM smartpay_transactions t
WHERE t.timestamp >= DATEADD(MONTH, -3, GETDATE())
GROUP BY FORMAT(t.timestamp, 'yyyy-MM')
ORDER BY month DESC;

-- Daily Active Users (DAU) - Last 30 days
SELECT 
    CAST(t.timestamp AS DATE) as date,
    COUNT(DISTINCT t.user_id) as daily_active_users
FROM smartpay_transactions t
WHERE t.timestamp >= DATEADD(DAY, -30, GETDATE())
GROUP BY CAST(t.timestamp AS DATE)
ORDER BY date DESC;

-- User Growth Rate (Monthly)
WITH monthly_signups AS (
    SELECT 
        FORMAT(signup_date, 'yyyy-MM') as month,
        COUNT(*) as new_users
    FROM smartpay_users
    GROUP BY FORMAT(signup_date, 'yyyy-MM')
)
SELECT 
    month,
    new_users,
    LAG(new_users) OVER (ORDER BY month) as prev_month_users,
    ROUND(((CAST(new_users AS FLOAT) - LAG(new_users) OVER (ORDER BY month)) / 
           LAG(new_users) OVER (ORDER BY month)) * 100, 2) as growth_rate
FROM monthly_signups
ORDER BY month DESC;

-- Churn Rate (Users inactive for 30+ days)
SELECT 
    COUNT(CASE WHEN aa.last_transaction_date < DATEADD(DAY, -30, GETDATE()) THEN 1 END) as churned_users,
    COUNT(*) as total_users,
    ROUND((CAST(COUNT(CASE WHEN aa.last_transaction_date < DATEADD(DAY, -30, GETDATE()) THEN 1 END) AS FLOAT) / COUNT(*)) * 100, 2) as churn_rate_percentage
FROM smartpay_app_activity aa;

-- User Segmentation by Activity Level
SELECT 
    CASE 
        WHEN aa.days_active_per_month >= 20 THEN 'High Activity'
        WHEN aa.days_active_per_month >= 10 THEN 'Medium Activity'
        ELSE 'Low Activity'
    END as activity_segment,
    COUNT(*) as user_count,
    ROUND((CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM smartpay_app_activity)) * 100, 2) as percentage
FROM smartpay_app_activity aa
GROUP BY 
    CASE 
        WHEN aa.days_active_per_month >= 20 THEN 'High Activity'
        WHEN aa.days_active_per_month >= 10 THEN 'Medium Activity'
        ELSE 'Low Activity'
    END
ORDER BY user_count DESC;

-- Geographic Distribution
SELECT 
    u.location,
    COUNT(*) as user_count,
    ROUND((CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM smartpay_users)) * 100, 2) as percentage
FROM smartpay_users u
GROUP BY u.location
ORDER BY user_count DESC;

-- Age Group Distribution
SELECT 
    CASE 
        WHEN u.age < 25 THEN '18-24'
        WHEN u.age < 35 THEN '25-34'
        WHEN u.age < 45 THEN '35-44'
        WHEN u.age < 55 THEN '45-54'
        ELSE '55+'
    END as age_group,
    COUNT(*) as user_count,
    ROUND((CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM smartpay_users)) * 100, 2) as percentage
FROM smartpay_users u
GROUP BY 
    CASE 
        WHEN u.age < 25 THEN '18-24'
        WHEN u.age < 35 THEN '25-34'
        WHEN u.age < 45 THEN '35-44'
        WHEN u.age < 55 THEN '45-54'
        ELSE '55+'
    END
ORDER BY age_group;

-- =====================================================
-- 2. TRANSACTION KPIs
-- =====================================================

-- Transaction Success Rate by Feature
SELECT 
    t.feature,
    COUNT(*) as total_transactions,
    COUNT(CASE WHEN t.status = 'Success' THEN 1 END) as successful_transactions,
    ROUND((CAST(COUNT(CASE WHEN t.status = 'Success' THEN 1 END) AS FLOAT) / COUNT(*)) * 100, 2) as success_rate
FROM smartpay_transactions t
GROUP BY t.feature
ORDER BY success_rate DESC;

-- Daily Transaction Volume
SELECT 
    CAST(t.timestamp AS DATE) as date,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue
FROM smartpay_transactions t
WHERE t.timestamp >= DATEADD(DAY, -30, GETDATE())
GROUP BY CAST(t.timestamp AS DATE)
ORDER BY date DESC;

-- Monthly Transaction Trends
SELECT 
    FORMAT(t.timestamp, 'yyyy-MM') as month,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue,
    AVG(CASE WHEN t.status = 'Success' THEN t.amount END) as avg_transaction_value
FROM smartpay_transactions t
GROUP BY FORMAT(t.timestamp, 'yyyy-MM')
ORDER BY month DESC;

-- Average Transaction Value (ATV) by Feature
SELECT 
    t.feature,
    COUNT(*) as transaction_count,
    AVG(CASE WHEN t.status = 'Success' THEN t.amount END) as avg_transaction_value,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue
FROM smartpay_transactions t
GROUP BY t.feature
ORDER BY avg_transaction_value DESC;

-- Revenue per User (ARPU)
SELECT 
    FORMAT(t.timestamp, 'yyyy-MM') as month,
    COUNT(DISTINCT t.user_id) as active_users,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue,
    ROUND(SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) / CAST(COUNT(DISTINCT t.user_id) AS FLOAT), 2) as arpu
FROM smartpay_transactions t
GROUP BY FORMAT(t.timestamp, 'yyyy-MM')
ORDER BY month DESC;

-- Transaction Status Distribution
SELECT 
    t.status,
    COUNT(*) as count,
    ROUND((CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM smartpay_transactions)) * 100, 2) as percentage
FROM smartpay_transactions t
GROUP BY t.status
ORDER BY count DESC;

-- =====================================================
-- 3. FUNNEL ANALYSIS KPIs
-- =====================================================

-- Feature Usage Funnel
SELECT 
    t.feature,
    COUNT(DISTINCT t.user_id) as users_who_used_feature,
    COUNT(CASE WHEN t.status = 'Success' THEN t.user_id END) as successful_transactions,
    ROUND((CAST(COUNT(CASE WHEN t.status = 'Success' THEN t.user_id END) AS FLOAT) / COUNT(DISTINCT t.user_id)) * 100, 2) as conversion_rate
FROM smartpay_transactions t
GROUP BY t.feature
ORDER BY users_who_used_feature DESC;

-- Overall Funnel Metrics
SELECT 
    'App Opens' as funnel_stage,
    COUNT(DISTINCT aa.user_id) as user_count,
    100 as conversion_rate
FROM smartpay_app_activity aa
WHERE aa.app_open_count > 0

UNION ALL

SELECT 
    'Feature Used' as funnel_stage,
    COUNT(DISTINCT t.user_id) as user_count,
    ROUND((CAST(COUNT(DISTINCT t.user_id) AS FLOAT) / (SELECT COUNT(DISTINCT aa.user_id) FROM smartpay_app_activity aa WHERE aa.app_open_count > 0)) * 100, 2) as conversion_rate
FROM smartpay_transactions t

UNION ALL

SELECT 
    'Transaction Started' as funnel_stage,
    COUNT(DISTINCT t.user_id) as user_count,
    ROUND((CAST(COUNT(DISTINCT t.user_id) AS FLOAT) / (SELECT COUNT(DISTINCT aa.user_id) FROM smartpay_app_activity aa WHERE aa.app_open_count > 0)) * 100, 2) as conversion_rate
FROM smartpay_transactions t
WHERE t.status IN ('Success', 'Failed', 'Abandoned')

UNION ALL

SELECT 
    'Transaction Completed' as funnel_stage,
    COUNT(DISTINCT t.user_id) as user_count,
    ROUND((CAST(COUNT(DISTINCT t.user_id) AS FLOAT) / (SELECT COUNT(DISTINCT aa.user_id) FROM smartpay_app_activity aa WHERE aa.app_open_count > 0)) * 100, 2) as conversion_rate
FROM smartpay_transactions t
WHERE t.status = 'Success';

-- =====================================================
-- 4. FEATURE ENGAGEMENT KPIs
-- =====================================================

-- Feature Usage Heatmap (by hour of day)
SELECT 
    t.feature,
    DATEPART(HOUR, t.timestamp) as hour_of_day,
    COUNT(*) as usage_count
FROM smartpay_transactions t
GROUP BY t.feature, DATEPART(HOUR, t.timestamp)
ORDER BY t.feature, hour_of_day;

-- Feature Usage by Day of Week
SELECT 
    t.feature,
    DATENAME(WEEKDAY, t.timestamp) as day_of_week,
    COUNT(*) as usage_count
FROM smartpay_transactions t
GROUP BY t.feature, DATENAME(WEEKDAY, t.timestamp)
ORDER BY t.feature, 
    CASE DATENAME(WEEKDAY, t.timestamp)
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;

-- User Retention by Feature (30-day retention)
SELECT 
    t.feature,
    COUNT(DISTINCT t.user_id) as total_users,
    COUNT(DISTINCT CASE WHEN t.timestamp >= DATEADD(DAY, -30, GETDATE()) THEN t.user_id END) as retained_users,
    ROUND((CAST(COUNT(DISTINCT CASE WHEN t.timestamp >= DATEADD(DAY, -30, GETDATE()) THEN t.user_id END) AS FLOAT) / COUNT(DISTINCT t.user_id)) * 100, 2) as retention_rate
FROM smartpay_transactions t
GROUP BY t.feature
ORDER BY retention_rate DESC;

-- Feature Adoption Trends (Monthly)
SELECT 
    FORMAT(t.timestamp, 'yyyy-MM') as month,
    t.feature,
    COUNT(DISTINCT t.user_id) as unique_users
FROM smartpay_transactions t
GROUP BY FORMAT(t.timestamp, 'yyyy-MM'), t.feature
ORDER BY month DESC, unique_users DESC;

-- =====================================================
-- 5. ADVANCED ANALYTICS KPIs
-- =====================================================

-- High-Value Users (Top 10% by transaction value)
WITH user_revenue AS (
    SELECT 
        t.user_id,
        SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue,
        COUNT(*) as transaction_count
    FROM smartpay_transactions t
    GROUP BY t.user_id
),
user_percentiles AS (
    SELECT 
        user_id,
        total_revenue,
        transaction_count,
        NTILE(10) OVER (ORDER BY total_revenue DESC) as revenue_percentile
    FROM user_revenue
)
SELECT 
    up.user_id,
    u.name,
    u.age,
    u.location,
    up.total_revenue,
    up.transaction_count,
    CASE WHEN up.revenue_percentile = 1 THEN 'Top 10%' ELSE 'Other' END as user_segment
FROM user_percentiles up
JOIN smartpay_users u ON up.user_id = u.user_id
WHERE up.revenue_percentile = 1
ORDER BY up.total_revenue DESC;

-- Transaction Failure Analysis
SELECT 
    t.feature,
    t.status,
    COUNT(*) as failure_count,
    AVG(t.amount) as avg_amount,
    ROUND((CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM smartpay_transactions WHERE status = 'Failed')) * 100, 2) as failure_percentage
FROM smartpay_transactions t
WHERE t.status = 'Failed'
GROUP BY t.feature, t.status
ORDER BY failure_count DESC;

-- User Engagement Score
SELECT 
    aa.user_id,
    u.name,
    u.age,
    u.location,
    aa.app_open_count,
    aa.days_active_per_month,
    DATEDIFF(DAY, aa.last_transaction_date, GETDATE()) as days_since_last_transaction,
    CASE 
        WHEN aa.days_active_per_month >= 20 AND aa.app_open_count >= 200 THEN 'High Engagement'
        WHEN aa.days_active_per_month >= 10 AND aa.app_open_count >= 100 THEN 'Medium Engagement'
        ELSE 'Low Engagement'
    END as engagement_level
FROM smartpay_app_activity aa
JOIN smartpay_users u ON aa.user_id = u.user_id
ORDER BY aa.days_active_per_month DESC, aa.app_open_count DESC;

-- =====================================================
-- 6. BUSINESS INTELLIGENCE VIEWS
-- =====================================================

-- Create a comprehensive user summary view
GO
CREATE OR ALTER VIEW user_summary AS
SELECT 
    u.user_id,
    u.name,
    u.age,
    u.location,
    u.signup_date,
    aa.app_open_count,
    aa.days_active_per_month,
    aa.last_transaction_date,
    DATEDIFF(DAY, aa.last_transaction_date, GETDATE()) as days_since_last_transaction,
    COUNT(t.transaction_id) as total_transactions,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue,
    AVG(CASE WHEN t.status = 'Success' THEN t.amount END) as avg_transaction_value,
    COUNT(DISTINCT t.feature) as features_used,
    CASE 
        WHEN DATEDIFF(DAY, aa.last_transaction_date, GETDATE()) > 30 THEN 'Churned'
        WHEN DATEDIFF(DAY, aa.last_transaction_date, GETDATE()) > 7 THEN 'At Risk'
        ELSE 'Active'
    END as user_status
FROM smartpay_users u
LEFT JOIN smartpay_app_activity aa ON u.user_id = aa.user_id
LEFT JOIN smartpay_transactions t ON u.user_id = t.user_id
GROUP BY u.user_id, u.name, u.age, u.location, u.signup_date, 
         aa.app_open_count, aa.days_active_per_month, aa.last_transaction_date;
GO

-- Create a transaction summary view
GO
CREATE OR ALTER VIEW transaction_summary AS
SELECT 
    CAST(t.timestamp AS DATE) as transaction_date,
    t.feature,
    t.status,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN t.status = 'Success' THEN t.amount ELSE 0 END) as total_revenue,
    AVG(CASE WHEN t.status = 'Success' THEN t.amount END) as avg_transaction_value,
    COUNT(DISTINCT t.user_id) as unique_users
FROM smartpay_transactions t
GROUP BY CAST(t.timestamp AS DATE), t.feature, t.status;
GO 