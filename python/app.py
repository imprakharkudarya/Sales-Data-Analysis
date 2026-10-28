import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import mysql.connector

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="Sales Data Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analysis Dashboard")
st.write("Analyze sales performance by product and region.")
st.divider()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_records,
            COALESCE(SUM(quantity * unit_price), 0) AS total_revenue,
            COUNT(DISTINCT product_name) AS total_products
        FROM sales
    """)

    total_records, total_revenue, total_products = cursor.fetchone()

    st.subheader("Sales Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Total Sales Records", total_records)
    col3.metric("Products", total_products)

    

    st.divider()
    st.subheader("Revenue by Product")

    cursor.execute("""
        SELECT
            product_name,
            SUM(quantity * unit_price) AS total_revenue
        FROM sales
        GROUP BY product_name
        ORDER BY total_revenue DESC
    """)

    product_data = cursor.fetchall()

    product_names = [row[0] for row in product_data]
    product_revenues = [float(row[1]) for row in product_data]

    st.bar_chart(
        data=dict(zip(product_names, product_revenues)),
        x_label="Product",
        y_label="Revenue (₹)"
    )
    st.divider()
    st.subheader("Revenue by Region")

    cursor.execute("""
        SELECT
            region,
            SUM(quantity * unit_price) AS total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """)

    region_data = cursor.fetchall()

    regions = [row[0] for row in region_data]
    region_revenues = [float(row[1]) for row in region_data]

    st.bar_chart(
        data=dict(zip(regions, region_revenues)),
        x_label="Region",
        y_label="Revenue (₹)"
    )
    st.divider()
    st.subheader("All Sales Records")

    cursor.execute("""
        SELECT
            sale_id,
            sale_date,
            product_name,
            quantity,
            unit_price,
            quantity * unit_price AS sale_revenue,
            region
        FROM sales
        ORDER BY sale_date DESC
    """)

    sales_data = cursor.fetchall()

    st.dataframe(
        [
            {
                "Sale ID": row[0],
                "Date": row[1],
                "Product": row[2],
                "Quantity": row[3],
                "Unit Price (₹)": float(row[4]),
                "Revenue (₹)": float(row[5]),
                "Region": row[6]
            }
            for row in sales_data
        ],
        use_container_width=True,
        hide_index=True
    )
    
    
    st.divider()
    st.subheader("Sales Records")

    cursor.execute("""
        SELECT
            sale_id, sale_date, product_name, quantity,
            unit_price, quantity * unit_price AS sale_revenue, region
        FROM sales
        ORDER BY sale_date DESC
    """)

    sales_data = cursor.fetchall()

    products = ["All"] + sorted(set(row[2] for row in sales_data))
    regions = ["All"] + sorted(set(row[6] for row in sales_data))

    col1, col2 = st.columns(2)

    with col1:
        selected_product = st.selectbox("Filter by product", products)

    with col2:
        selected_region = st.selectbox("Filter by region", regions)

    filtered_sales = [
        row for row in sales_data
        if (selected_product == "All" or row[2] == selected_product)
        and (selected_region == "All" or row[6] == selected_region)
    ]

    st.dataframe(
        [
            {
                "Sale ID": row[0],
                "Date": row[1],
                "Product": row[2],
                "Quantity": row[3],
                "Unit Price (₹)": float(row[4]),
                "Revenue (₹)": float(row[5]),
                "Region": row[6]
            }
            for row in filtered_sales
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Showing {len(filtered_sales)} of {len(sales_data)} records.")

    

    st.success("Live data loaded from MySQL successfully!")
    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    st.error(f"Could not load data from MySQL: {error}")