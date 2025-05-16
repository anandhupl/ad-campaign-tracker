CREATE DATABASE ad_tracker;
USE ad_tracker;
CREATE TABLE campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(255),
    date DATE,
    clicks INT,
    impressions INT,
    conversions INT
);