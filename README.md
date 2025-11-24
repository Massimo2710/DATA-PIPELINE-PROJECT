# 🚀 Modern Data Pipeline Project

A complete end-to-end data pipeline demonstrating modern data engineering best practices using **Python**, **DuckDB**, **dbt**, and **Dagster**.

## 📊 Project Overview

This project implements a lightweight yet powerful data pipeline that follows the **medallion architecture** (Bronze → Silver → Gold) for data transformation. It's designed to be:

- **Lightweight**: Runs entirely on a local machine (MacBook Air M2 compatible)
- **Scalable**: Architecture patterns applicable to production environments
- **Educational**: Clear separation of concerns and best practices
- **Modern**: Uses industry-standard tools (dbt, Dagster, DuckDB)

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA PIPELINE FLOW                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Source     │      │   Storage    │      │ Transformation│      │ Orchestration│
│              │      │              │      │              │      │              │
│   Python     │─────▶│   DuckDB     │─────▶│     dbt      │─────▶│   Dagster    │
│   + Faker    │      │   (raw)      │      │  (models)    │      │   (assets)   │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
     │                      │                      │                      │
     │                      │                      │                      │
 Generates            Stores raw data      Creates staging        Orchestrates &
 fake data            in 'raw' schema      & analytics           monitors pipeline
 (users, products,                         tables in 'main'
  purchases)                               schema
```

### Data Flow Details

1. **Ingestion Layer** (`ingestion/generate_data.py`)
   - Generates synthetic data using Python Faker library
   - Creates 3 source tables: `users`, `products`, `purchases`
   - Loads data into DuckDB `raw` schema
   - **Output**: ~100 users, ~50 products, ~500 purchase transactions

2. **Storage Layer** (DuckDB)
   - Lightweight analytical database (single file: `data/analytics.duckdb`)
   - `raw` schema: immutable source data
   - `main` schema: transformed data (staging + analytics)

3. **Transformation Layer** (dbt)
   - **Staging models** (`stg_*`): Clean and standardize raw data
     - `stg_users`: User dimension
     - `stg_products`: Product dimension  
     - `stg_purchases`: Purchase facts
   - **Analytics models**: Business logic and aggregations
     - `fct_purchases`: Enriched fact table with pricing
     - `user_purchases_summary`: User-level KPIs (total spent, avg order value)
     - `category_sales_summary`: Category performance metrics

4. **Orchestration Layer** (Dagster)
   - Manages dependencies between pipeline steps
   - Provides web UI for monitoring and execution
   - Two main assets:
     - `raw_data`: Runs ingestion script
     - `dbt_staging_and_analytics`: Executes all dbt models

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.9 | Scripting and orchestration |
| **Ingestion** | Faker | Generate realistic fake data |
| **Database** | DuckDB | Embedded analytical database |
| **Transformation** | dbt Core | SQL-based data transformations |
| **Orchestration** | Dagster | Pipeline orchestration & monitoring |
| **Environment** | Conda | Dependency management |
| **Visualization** | DBeaver | Database exploration (optional) |

## 📋 Prerequisites

- **macOS** (tested on MacBook Air M2)
- **Anaconda** or **Miniconda** installed
- **Python 3.9+**
- **Git** (for version control)
- **Docker Desktop** (optional, not used in this lightweight setup)

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Massimo2710/DATA-PIPELINE-PROJECT.git
cd DATA-PIPELINE-PROJECT
```

### 2. Create Conda Environment
```bash
# Create environment with Python 3.9
conda create -n data-pipeline python=3.9 -y

# Activate environment
conda activate data-pipeline
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install \
  dbt-core \
  dbt-duckdb \
  dagster \
  dagster-webserver \
  dagster-dbt \
  pandas \
  faker \
  duckdb
```

### 4. Verify dbt Configuration
```bash
cd dbt_project
dbt debug
```

Expected output: `All checks passed!`

### 5. Run Initial Data Load (Optional)
```bash
cd ../ingestion
python generate_data.py
```

This creates the initial dataset in `data/analytics.duckdb`.

### 6. Launch Dagster
```bash
cd ../dagster_project
dagster dev
```

Dagster UI will be available at: **http://localhost:3000**

### 7. Execute the Pipeline

1. Open **http://localhost:3000** in your browser
2. Click **"Assets"** in the left sidebar
3. Select both assets (`raw_data` and `dbt_staging_and_analytics`)
4. Click **"Materialize selected"**
5. Watch the pipeline execute in real-time!

## 📁 Project Structure
```
data-pipeline-project/
│
├── data/                          # DuckDB database files (gitignored)
│   └── analytics.duckdb          # Main analytical database
│
├── ingestion/                     # Data ingestion scripts
│   └── generate_data.py          # Faker-based data generator
│
├── dbt_project/                   # dbt transformation project
│   ├── models/
│   │   ├── staging/              # Staging models (stg_*)
│   │   │   ├── schema.yml        # Source definitions
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_products.sql
│   │   │   └── stg_purchases.sql
│   │   └── analytics/            # Analytics models
│   │       ├── fct_purchases.sql
│   │       ├── user_purchases_summary.sql
│   │       └── category_sales_summary.sql
│   ├── dbt_project.yml           # dbt configuration
│   └── target/                   # Compiled SQL (gitignored)
│
├── dagster_project/               # Dagster orchestration
│   └── dagster_project/
│       ├── assets.py             # Asset definitions
│       └── definitions.py        # Dagster definitions
│
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🎯 Usage Examples

### Running Individual Components

#### 1. Generate New Data
```bash
conda activate data-pipeline
cd ingestion
python generate_data.py
```

#### 2. Run dbt Transformations Only
```bash
cd dbt_project
dbt run                    # Run all models
dbt run --select staging   # Run only staging models
dbt test                   # Run data quality tests
```

#### 3. View dbt Documentation
```bash
dbt docs generate
dbt docs serve
```

Access at: **http://localhost:8080**

### Exploring the Data

#### Option 1: DBeaver (Recommended)

1. Install DBeaver Community Edition
2. Create new connection → DuckDB
3. Database path: `/path/to/data-pipeline-project/data/analytics.duckdb`
4. Explore schemas: `raw` and `main`

#### Option 2: Python
```python
import duckdb

conn = duckdb.connect('data/analytics.duckdb')

# View all tables
conn.execute("SHOW TABLES").fetchall()

# Query data
conn.execute("""
    SELECT * FROM main.user_purchases_summary 
    ORDER BY total_spent DESC 
    LIMIT 10
""").df()
```

## 📊 Data Model

### Source Tables (raw schema)

| Table | Description | Records |
|-------|-------------|---------|
| `raw.users` | Customer information | ~100 |
| `raw.products` | Product catalog | ~50 |
| `raw.purchases` | Transaction records | ~500 |

### Staging Tables (main schema)

| Table | Description | Transformation |
|-------|-------------|----------------|
| `stg_users` | Cleaned users | Column selection, type casting |
| `stg_products` | Cleaned products | Standardization |
| `stg_purchases` | Cleaned purchases | Date formatting |

### Analytics Tables (main schema)

| Table | Description | Key Metrics |
|-------|-------------|-------------|
| `fct_purchases` | Enriched fact table | `total_amount` = quantity × price |
| `user_purchases_summary` | User KPIs | `total_purchases`, `total_spent`, `avg_purchase_amount` |
| `category_sales_summary` | Category performance | `total_revenue`, `total_items_sold`, `avg_transaction_value` |

## 🔄 Pipeline Execution Flow
```
1. Dagster triggers `raw_data` asset
   ↓
2. Python script generates fake data
   ↓
3. Data loaded into DuckDB `raw` schema
   ↓
4. Dagster triggers `dbt_staging_and_analytics` asset
   ↓
5. dbt reads from `raw` schema
   ↓
6. dbt creates staging tables in `main` schema
   ↓
7. dbt creates analytics tables in `main` schema
   ↓
8. Pipeline complete ✅
```

## 🛠️ Troubleshooting

### Issue: `dbt command not found`

**Solution**: Ensure conda environment is activated
```bash
conda activate data-pipeline
which dbt  # Should show path in conda env
```

### Issue: DuckDB file locked

**Solution**: Close DBeaver or any other connections to the database

### Issue: Dagster assets not visible

**Solution**: Check `definitions.py` and `assets.py` are correctly configured
```bash
cd dagster_project
dagster asset list
```

### Issue: dbt models fail

**Solution**: Verify database connection
```bash
cd dbt_project
dbt debug
```

## 🚧 Future Enhancements

- [ ] Add data quality tests in dbt
- [ ] Implement incremental models for large datasets
- [ ] Add scheduling (run pipeline daily at 8 AM)
- [ ] Create Dagster sensors for file-based triggers
- [ ] Add email alerts on pipeline failures
- [ ] Integrate with BI tool (Metabase, Superset)
- [ ] Add CI/CD with GitHub Actions
- [ ] Implement data versioning

## 📚 Learning Resources

- **dbt**: https://docs.getdbt.com/
- **Dagster**: https://docs.dagster.io/
- **DuckDB**: https://duckdb.org/docs/
- **Medallion Architecture**: https://www.databricks.com/glossary/medallion-architecture

## 👨‍💻 Author

**Massimo D'Antonio**
- GitHub: [@Massimo2710](https://github.com/Massimo2710)

## 📄 License

This project is open source and available under the MIT License.

---

⭐ **If you find this project useful, please consider giving it a star!** ⭐