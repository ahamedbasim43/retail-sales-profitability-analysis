# 📊 Retail Sales & Profitability Analysis

A data analytics project that analyzes retail sales, profitability, product categories, regional performance, monthly sales trends, and discount impact using **Python, SQL, Pandas, NumPy, Matplotlib, Seaborn, Plotly, and Streamlit**.

The project transforms raw retail sales data into meaningful business insights through data cleaning, SQL analysis, exploratory data analysis (EDA), visualization, and an interactive dashboard.

## 🎯 Project Objectives

- Analyze overall retail sales and profitability.
- Identify top-performing product categories.
- Compare sales and profit across different regions.
- Understand monthly sales trends.
- Analyze the relationship between discounts and average profit.
- Identify loss-making product sub-categories.
- Build an interactive dashboard for business analysis.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and processing |
| SQL | Database management and queries |
| SQLite | Relational database |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts |
| Streamlit | Interactive dashboard |
| Git & GitHub | Version control and project hosting |

## 📂 Project Structure

```text
retail-sales-profitability-analysis/
│
├── app.py
├── business_insights.py
├── check_dataset.py
├── create_database.py
├── python_eda.py
├── python_visualization.py
├── run_sql.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── outputs/
│   ├── charts/
│   ├── tables/
│   └── screenshots/
│       ├── dashboard  page 1.png
│       ├── dashboard page 2.png
│       └── dashboard page 3.png
│
├── sql/
│   └── analysis_queries.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 📈 Key Performance Indicators (KPIs)

The project analyzes the following business metrics:

- Total Sales
- Total Profit
- Unique Orders
- Profit Margin
- Average Order Value

## 🖥️ Streamlit Dashboard Preview

### Dashboard Overview

![Dashboard Overview](outputs/screenshots/dashboard%20%20page%201.png)

### Monthly Sales Analysis

![Monthly Sales Analysis](outputs/screenshots/dashboard%20page%202.png)

### Discount and Profit Analysis

![Discount and Profit Analysis](outputs/screenshots/dashboard%20page%203.png)

## 📊 Dashboard Features

The Streamlit dashboard provides:

### 1. Interactive Filters

- Filter by year
- Filter by product category
- Filter by region

### 2. KPI Cards

- Total Sales
- Total Profit
- Unique Orders
- Profit Margin
- Average Order Value

### 3. Data Visualizations

- Sales by Product Category
- Profit by Region
- Monthly Sales Trend
- Discount vs Average Profit

### 4. Data Export

- View filtered sales records.
- Download filtered data as CSV.

## 🔍 Key Business Findings

Based on the Sample Superstore dataset:

- **Total Sales:** $2,297,200.86
- **Total Profit:** $286,397.02
- **Total Orders:** 5,009
- **Overall Profit Margin:** 12.47%
- **Average Order Value:** $458.61

### Category Performance

- Technology generated the highest sales and profit.
- Furniture generated substantial sales but comparatively lower profit.

### Regional Performance

- West region recorded the highest sales and profit.
- East region was the second-highest profit-generating region.

### Loss-Making Sub-Categories

- Tables: -$17,725.48
- Bookcases: -$3,472.56
- Supplies: -$1,189.10

### Discount Analysis

Some higher discount levels showed negative average profit. This highlights areas that may need further pricing and discount strategy analysis.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ahamedbasim43/retail-sales-profitability-analysis.git
```

### 2. Navigate to the Project Folder

```bash
cd retail-sales-profitability-analysis
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Add the Dataset

The dataset CSV files are excluded from this GitHub repository.

Place the original dataset in:

```text
data/raw/
```

After running the data cleaning process, place the cleaned dataset at:

```text
data/processed/superstore_cleaned.csv
```

The cleaned CSV file is required to run the Streamlit dashboard.

### 7. Run the Dashboard

```bash
python -m streamlit run app.py
```

Open the local dashboard in your browser:

http://localhost:8501

## 🗄️ SQL Analysis

SQL queries are included in:

```text
sql/analysis_queries.sql
```

The analysis covers:

- Overall sales and profit
- Category-wise performance
- Region-wise performance
- Loss-making sub-categories
- Product performance
- Monthly sales analysis

## 📷 Project Outputs

Generated visualizations and summary tables are available in:

```text
outputs/charts/
outputs/tables/
```

## 🚀 Future Improvements

- Deploy the Streamlit dashboard online.
- Add more advanced business KPIs.
- Implement sales forecasting using Machine Learning.
- Add customer segmentation analysis.
- Improve interactive filtering and reporting.

## 👨‍💻 Author

**Ahamed Basim**

B.Sc. Information Technology Student

Interested in Data Analytics, Python, SQL, Machine Learning, and Business Intelligence.

---

⭐ If you find this project useful, feel free to explore the repository and share your feedback!