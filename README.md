
# Sales Data Analysis Dashboard

A Python and MySQL project that analyzes sales data and displays business insights through an interactive Streamlit dashboard.

## Features

- Total revenue, sales record, and product summary
- Revenue analysis by product
- Revenue analysis by region
- Detailed sales records table
- Interactive product and region filters
- Live data retrieval from MySQL

## Technologies Used

- Python
- MySQL
- SQL
- Streamlit
- Pandas
- Matplotlib

## Project Structure

Sales_Data_Analysis/
├── python/
│   ├── app.py
│   └── main.py
├── sql/
├── requirements.txt
└── README.md

## Setup Instructions

### 1. Install Python dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 2. Set up MySQL

Create the database and sales table using the SQL scripts in the `sql/` folder.

Database name: `sales_analysis`

Add your own MySQL connection details to the Python application.
Do not upload passwords or other secrets to GitHub.

### 3. Run the dashboard

From the project root, run:

```bash
python -m streamlit run python/app.py
```

Open the local URL shown in the terminal.

## Sample Data

The project currently uses 10 sample sales records for demonstration. Revenue and charts are calculated from the data stored in MySQL.

## Future Improvements

- Add date-range filters
- Export filtered records to CSV
- Use a larger real-world dataset
- Deploy the dashboard online


