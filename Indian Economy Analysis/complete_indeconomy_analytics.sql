-- ============================================
-- INDIA ECONOMY ANALYTICS - COMPLETE SQL
-- ============================================

CREATE DATABASE IF NOT EXISTS india_economy_analytics;
USE india_economy_analytics;

DROP TABLE IF EXISTS economic_data;

CREATE TABLE economic_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT,
    sector VARCHAR(100),
    gdp_lakh_crore DECIMAL(15, 2),
    growth_rate DECIMAL(10, 4),
    employment_millions DECIMAL(10, 2),
    exports DECIMAL(15, 2),
    imports DECIMAL(15, 2),
    fdi_inflows DECIMAL(15, 2),
    inflation_rate DECIMAL(10, 4),
    cpi_index DECIMAL(10, 2),
    iip_growth DECIMAL(10, 4),
    tax_revenue DECIMAL(15, 2),
    financial_year VARCHAR(20),
    sector_category VARCHAR(50),
    economic_activity_category VARCHAR(50),
    stakeholder_category VARCHAR(50),
    trade_balance DECIMAL(15, 2),
    gdp_per_employment DECIMAL(15, 4),
    trade_openness DECIMAL(15, 4),
    fdi_to_gdp DECIMAL(15, 4),
    tax_efficiency DECIMAL(15, 4),
    growth_momentum DECIMAL(10, 4),
    economic_cycle VARCHAR(20),
    performance_score DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_year (year),
    INDEX idx_sector (sector),
    INDEX idx_sector_category (sector_category)
);

LOAD DATA LOCAL INFILE '../data/processed/indian_economy_featured.csv'
INTO TABLE economic_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(year, quarter, sector, gdp_lakh_crore, growth_rate, employment_millions, 
 exports, imports, fdi_inflows, inflation_rate, cpi_index, iip_growth, 
 tax_revenue, financial_year, sector_category, economic_activity_category, 
 stakeholder_category, trade_balance, gdp_per_employment, trade_openness, 
 fdi_to_gdp, tax_efficiency, growth_momentum, economic_cycle, performance_score);

UPDATE economic_data 
SET growth_rate = COALESCE(growth_rate, (SELECT AVG(growth_rate) FROM economic_data))
WHERE growth_rate IS NULL;

UPDATE economic_data 
SET inflation_rate = COALESCE(inflation_rate, (SELECT AVG(inflation_rate) FROM economic_data))
WHERE inflation_rate IS NULL;

UPDATE economic_data 
SET employment_millions = COALESCE(employment_millions, (SELECT AVG(employment_millions) FROM economic_data))
WHERE employment_millions IS NULL;

UPDATE economic_data 
SET trade_balance = exports - imports
WHERE trade_balance IS NULL;

UPDATE economic_data 
SET gdp_per_employment = CASE 
    WHEN employment_millions > 0 THEN gdp_lakh_crore / employment_millions 
    ELSE NULL 
END;

UPDATE economic_data 
SET trade_openness = CASE 
    WHEN gdp_lakh_crore > 0 THEN (exports + imports) / gdp_lakh_crore 
    ELSE NULL 
END;

UPDATE economic_data 
SET fdi_to_gdp = CASE 
    WHEN gdp_lakh_crore > 0 THEN fdi_inflows / gdp_lakh_crore 
    ELSE NULL 
END;

UPDATE economic_data 
SET tax_efficiency = CASE 
    WHEN gdp_lakh_crore > 0 THEN tax_revenue / gdp_lakh_crore 
    ELSE NULL 
END;

UPDATE economic_data 
SET economic_cycle = CASE 
    WHEN growth_rate > (SELECT AVG(growth_rate) FROM economic_data) 
    THEN 'Expansion' 
    ELSE 'Contraction' 
END;

UPDATE economic_data 
SET performance_score = (
    (growth_rate / NULLIF((SELECT MAX(growth_rate) FROM economic_data), 0)) +
    (gdp_lakh_crore / NULLIF((SELECT MAX(gdp_lakh_crore) FROM economic_data), 0)) +
    (employment_millions / NULLIF((SELECT MAX(employment_millions) FROM economic_data), 0))
) / 3;

CREATE OR REPLACE VIEW v_economic_summary AS
SELECT 
    year,
    COUNT(*) as total_records,
    SUM(gdp_lakh_crore) as total_gdp,
    AVG(growth_rate) as avg_growth,
    SUM(employment_millions) as total_employment,
    SUM(exports) as total_exports,
    SUM(imports) as total_imports,
    SUM(trade_balance) as total_trade_balance,
    SUM(fdi_inflows) as total_fdi,
    AVG(inflation_rate) as avg_inflation,
    AVG(cpi_index) as avg_cpi,
    AVG(iip_growth) as avg_iip_growth,
    SUM(tax_revenue) as total_tax_revenue,
    AVG(performance_score) as avg_performance_score
FROM economic_data
GROUP BY year
ORDER BY year DESC;

CREATE OR REPLACE VIEW v_sector_performance AS
SELECT 
    sector,
    sector_category,
    COUNT(*) as total_records,
    SUM(gdp_lakh_crore) as total_gdp,
    AVG(growth_rate) as avg_growth,
    SUM(employment_millions) as total_employment,
    SUM(fdi_inflows) as total_fdi,
    AVG(performance_score) as avg_performance_score,
    AVG(gdp_per_employment) as avg_gdp_per_employment
FROM economic_data
GROUP BY sector, sector_category
ORDER BY total_gdp DESC;

CREATE OR REPLACE VIEW v_trade_analysis AS
SELECT 
    year,
    sector,
    SUM(exports) as total_exports,
    SUM(imports) as total_imports,
    SUM(trade_balance) as total_trade_balance,
    CASE 
        WHEN SUM(trade_balance) > 0 THEN 'Surplus'
        WHEN SUM(trade_balance) < 0 THEN 'Deficit'
        ELSE 'Balanced'
    END as trade_status,
    AVG(trade_openness) as avg_trade_openness
FROM economic_data
GROUP BY year, sector
ORDER BY year DESC, total_trade_balance DESC;

CREATE OR REPLACE VIEW v_macro_indicators AS
SELECT 
    year,
    AVG(inflation_rate) as avg_inflation,
    AVG(cpi_index) as avg_cpi,
    AVG(iip_growth) as avg_iip_growth,
    AVG(growth_rate) as avg_growth,
    SUM(fdi_inflows) as total_fdi,
    CASE 
        WHEN AVG(inflation_rate) > 6 THEN 'High Inflation'
        WHEN AVG(inflation_rate) BETWEEN 4 AND 6 THEN 'Moderate Inflation'
        ELSE 'Low Inflation'
    END as inflation_category,
    CASE 
        WHEN AVG(growth_rate) > 7 THEN 'High Growth'
        WHEN AVG(growth_rate) BETWEEN 4 AND 7 THEN 'Moderate Growth'
        ELSE 'Low Growth'
    END as growth_category
FROM economic_data
GROUP BY year
ORDER BY year DESC;

CREATE OR REPLACE VIEW v_economic_health AS
SELECT 
    year,
    sector,
    AVG(growth_rate) as avg_growth,
    AVG(inflation_rate) as avg_inflation,
    SUM(fdi_inflows) as total_fdi,
    AVG(performance_score) as avg_performance,
    CASE 
        WHEN AVG(growth_rate) > 5 AND AVG(inflation_rate) < 5 THEN 'Strong'
        WHEN AVG(growth_rate) > 3 AND AVG(inflation_rate) < 6 THEN 'Stable'
        WHEN AVG(growth_rate) > 0 AND AVG(inflation_rate) < 8 THEN 'Moderate'
        ELSE 'Weak'
    END as economic_health,
    CASE 
        WHEN AVG(performance_score) >= 0.7 THEN 'Excellent'
        WHEN AVG(performance_score) >= 0.5 THEN 'Good'
        WHEN AVG(performance_score) >= 0.3 THEN 'Average'
        ELSE 'Needs Improvement'
    END as performance_rating
FROM economic_data
GROUP BY year, sector
ORDER BY year DESC, avg_performance DESC;

CREATE OR REPLACE VIEW v_stakeholder_analysis AS
SELECT 
    stakeholder_category,
    AVG(performance_score) as avg_performance,
    SUM(gdp_lakh_crore) as total_gdp,
    AVG(growth_rate) as avg_growth,
    SUM(employment_millions) as total_employment,
    SUM(fdi_inflows) as total_fdi,
    AVG(tax_efficiency) as avg_tax_efficiency,
    COUNT(*) as total_records
FROM economic_data
GROUP BY stakeholder_category
ORDER BY avg_performance DESC;

SELECT 
    year,
    SUM(gdp_lakh_crore) as total_gdp,
    LAG(SUM(gdp_lakh_crore)) OVER (ORDER BY year) as prev_year_gdp,
    ROUND(((SUM(gdp_lakh_crore) - LAG(SUM(gdp_lakh_crore)) OVER (ORDER BY year)) / LAG(SUM(gdp_lakh_crore)) OVER (ORDER BY year) * 100), 2) as yoy_growth_percent
FROM economic_data
GROUP BY year
ORDER BY year DESC;

SELECT 
    sector,
    sector_category,
    ROUND(AVG(growth_rate), 2) as avg_growth,
    ROUND(SUM(gdp_lakh_crore), 2) as total_gdp,
    ROUND(AVG(performance_score), 2) as avg_performance
FROM economic_data
WHERE year >= 2020
GROUP BY sector, sector_category
HAVING avg_growth > 0
ORDER BY avg_performance DESC
LIMIT 10;

SELECT 
    sector_category,
    year,
    ROUND(SUM(employment_millions), 2) as total_employment,
    ROUND(AVG(employment_millions), 2) as avg_employment
FROM economic_data
WHERE employment_millions IS NOT NULL
GROUP BY sector_category, year
ORDER BY year DESC, total_employment DESC;

SELECT 
    sector,
    sector_category,
    ROUND(SUM(fdi_inflows), 2) as total_fdi,
    ROW_NUMBER() OVER (ORDER BY SUM(fdi_inflows) DESC) as fdi_rank
FROM economic_data
WHERE fdi_inflows > 0
GROUP BY sector, sector_category
ORDER BY total_fdi DESC
LIMIT 15;

SELECT 
    year,
    ROUND(SUM(exports), 2) as total_exports,
    ROUND(SUM(imports), 2) as total_imports,
    ROUND(SUM(trade_balance), 2) as total_trade_balance,
    CASE 
        WHEN SUM(trade_balance) > 0 THEN 'Surplus'
        WHEN SUM(trade_balance) < 0 THEN 'Deficit'
        ELSE 'Balanced'
    END as trade_status
FROM economic_data
GROUP BY year
ORDER BY year;

SELECT 
    stakeholder_category,
    ROUND(AVG(performance_score), 2) as avg_performance,
    ROUND(SUM(gdp_lakh_crore), 2) as total_gdp,
    ROUND(AVG(growth_rate), 2) as avg_growth,
    ROUND(SUM(employment_millions), 2) as total_employment
FROM economic_data
GROUP BY stakeholder_category
ORDER BY avg_performance DESC;

WITH ranked_data AS (
    SELECT 
        year,
        sector,
        ROUND(gdp_lakh_crore, 2) as gdp,
        ROUND(growth_rate, 2) as growth,
        ROW_NUMBER() OVER (PARTITION BY year ORDER BY gdp_lakh_crore DESC) as gdp_rank,
        ROW_NUMBER() OVER (PARTITION BY year ORDER BY growth_rate DESC) as growth_rank
    FROM economic_data
)
SELECT 
    year,
    sector,
    gdp,
    growth,
    gdp_rank,
    growth_rank
FROM ranked_data
WHERE gdp_rank <= 3 OR growth_rank <= 3
ORDER BY year DESC, gdp_rank;

SELECT 
    year,
    ROUND(SUM(gdp_lakh_crore), 2) as total_gdp,
    ROUND(AVG(growth_rate), 2) as avg_growth,
    ROUND(SUM(employment_millions), 2) as total_employment,
    ROUND(SUM(fdi_inflows), 2) as total_fdi,
    ROUND(AVG(inflation_rate), 2) as avg_inflation
FROM economic_data
WHERE year >= 2018
GROUP BY year
ORDER BY year;

DROP PROCEDURE IF EXISTS sp_get_economic_summary;
DELIMITER //
CREATE PROCEDURE sp_get_economic_summary(IN p_year INT)
BEGIN
    SELECT 
        year,
        ROUND(SUM(gdp_lakh_crore), 2) as total_gdp,
        ROUND(AVG(growth_rate), 2) as avg_growth,
        ROUND(SUM(employment_millions), 2) as total_employment,
        ROUND(SUM(fdi_inflows), 2) as total_fdi,
        ROUND(AVG(inflation_rate), 2) as avg_inflation
    FROM economic_data
    WHERE year = p_year
    GROUP BY year;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_sector_performance;
DELIMITER //
CREATE PROCEDURE sp_get_sector_performance(IN p_year INT, IN p_sector VARCHAR(100))
BEGIN
    SELECT 
        sector,
        year,
        ROUND(gdp_lakh_crore, 2) as gdp,
        ROUND(growth_rate, 2) as growth,
        ROUND(employment_millions, 2) as employment,
        ROUND(fdi_inflows, 2) as fdi
    FROM economic_data
    WHERE year = p_year 
    AND sector = p_sector
    ORDER BY quarter;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_trade_analysis;
DELIMITER //
CREATE PROCEDURE sp_get_trade_analysis(IN p_year_start INT, IN p_year_end INT)
BEGIN
    SELECT 
        year,
        ROUND(SUM(exports), 2) as total_exports,
        ROUND(SUM(imports), 2) as total_imports,
        ROUND(SUM(trade_balance), 2) as trade_balance,
        CASE 
            WHEN SUM(trade_balance) > 0 THEN 'Surplus'
            WHEN SUM(trade_balance) < 0 THEN 'Deficit'
            ELSE 'Balanced'
        END as trade_status
    FROM economic_data
    WHERE year BETWEEN p_year_start AND p_year_end
    GROUP BY year
    ORDER BY year;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_forecast_data;
DELIMITER //
CREATE PROCEDURE sp_get_forecast_data(IN p_last_n_years INT)
BEGIN
    SELECT 
        year,
        ROUND(SUM(gdp_lakh_crore), 2) as total_gdp,
        ROUND(AVG(growth_rate), 2) as avg_growth,
        ROUND(SUM(employment_millions), 2) as total_employment,
        ROUND(SUM(fdi_inflows), 2) as total_fdi
    FROM economic_data
    WHERE year >= (SELECT MAX(year) - p_last_n_years FROM economic_data)
    GROUP BY year
    ORDER BY year;
END //
DELIMITER ;

CALL sp_get_economic_summary(2022);
CALL sp_get_sector_performance(2022, 'Manufacturing');
CALL sp_get_trade_analysis(2020, 2022);
CALL sp_get_forecast_data(3);

SELECT * FROM v_economic_summary;
SELECT * FROM v_sector_performance;
SELECT * FROM v_trade_analysis;
SELECT * FROM v_macro_indicators;
SELECT * FROM v_economic_health;
SELECT * FROM v_stakeholder_analysis;