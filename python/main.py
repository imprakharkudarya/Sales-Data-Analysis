import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        region,
        SUM(quantity * unit_price) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
""")

regional_revenues = cursor.fetchall()

print("\n===== REVENUE BY REGION =====")

for region, revenue in regional_revenues:
    print(f"{region}: ₹{revenue:,.2f}")