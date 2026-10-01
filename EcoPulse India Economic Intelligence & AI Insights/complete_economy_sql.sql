-- ============================================
-- ECOPULSE INDIA ECONOMIC INTELLIGENCE
-- Complete Database Setup
-- ============================================

CREATE DATABASE IF NOT EXISTS ecopulse_india;
USE ecopulse_india;

DROP TABLE IF EXISTS economy_data;

CREATE TABLE economy_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter VARCHAR(10),
    sector VARCHAR(100),
    gdp DECIMAL(15,2),
    growth DECIMAL(10,2),
    employment DECIMAL(10,2),
    exports DECIMAL(15,2),
    imports DECIMAL(15,2),
    fdi DECIMAL(15,2),
    inflation DECIMAL(10,2),
    cpi DECIMAL(10,2),
    iip DECIMAL(10,2),
    tax_revenue DECIMAL(15,2),
    financial_year VARCHAR(20),
    sector_category VARCHAR(50),
    stakeholder VARCHAR(50),
    INDEX idx_year (year),
    INDEX idx_sector (sector),
    INDEX idx_category (sector_category)
);

-- ============================================
-- ANALYTICAL VIEWS
-- ============================================

CREATE OR REPLACE VIEW v_yearly_summary AS
SELECT 
    year,
    COUNT(*) AS total_records,
    ROUND(SUM(gdp), 2) AS total_gdp,
    ROUND(AVG(growth), 2) AS avg_growth,
    ROUND(SUM(employment), 2) AS total_employment,
    ROUND(SUM(exports), 2) AS total_exports,
    ROUND(SUM(imports), 2) AS total_imports,
    ROUND(SUM(fdi), 2) AS total_fdi,
    ROUND(AVG(inflation), 2) AS avg_inflation
FROM economy_data
GROUP BY year
ORDER BY year DESC;

CREATE OR REPLACE VIEW v_sector_performance AS
SELECT 
    sector,
    sector_category,
    COUNT(*) AS total_records,
    ROUND(SUM(gdp), 2) AS total_gdp,
    ROUND(AVG(growth), 2) AS avg_growth,
    ROUND(SUM(employment), 2) AS total_employment,
    ROUND(SUM(fdi), 2) AS total_fdi
FROM economy_data
GROUP BY sector, sector_category
ORDER BY total_gdp DESC;

CREATE OR REPLACE VIEW v_trade_analysis AS
SELECT 
    year,
    ROUND(SUM(exports), 2) AS total_exports,
    ROUND(SUM(imports), 2) AS total_imports,
    ROUND(SUM(exports - imports), 2) AS trade_balance,
    CASE 
        WHEN SUM(exports - imports) > 0 THEN 'Surplus'
        WHEN SUM(exports - imports) < 0 THEN 'Deficit'
        ELSE 'Balanced'
    END AS trade_status
FROM economy_data
GROUP BY year
ORDER BY year DESC;

-- ============================================
-- STORED PROCEDURES
-- ============================================

DROP PROCEDURE IF EXISTS sp_get_sector_summary;

DELIMITER //
CREATE PROCEDURE sp_get_sector_summary(IN p_year INT)
BEGIN
    SELECT 
        sector,
        ROUND(SUM(gdp), 2) AS total_gdp,
        ROUND(AVG(growth), 2) AS avg_growth,
        ROUND(SUM(fdi), 2) AS total_fdi
    FROM economy_data
    WHERE year = p_year
    GROUP BY sector
    ORDER BY total_gdp DESC;
END //
DELIMITER ;

-- ============================================
-- TEST QUERIES
-- ============================================

SELECT 'Total Records' AS status, COUNT(*) AS count FROM economy_data;
SELECT 'Years Range' AS status, MIN(year) AS min_year, MAX(year) AS max_year FROM economy_data;
SELECT 'Sectors' AS status, COUNT(DISTINCT sector) AS count FROM economy_data;