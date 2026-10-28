
CREATE DATABASE IF NOT EXISTS sales_analysis;

USE sales_analysis;

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    region VARCHAR(50) NOT NULL
);
