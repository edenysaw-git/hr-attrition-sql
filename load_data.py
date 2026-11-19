"""
load_data.py
Loads the IBM HR Attrition CSV into a local DuckDB database (hr.duckdb).

Layers (same idea as a raw/silver/gold pipeline):
  raw_employees  -> the CSV exactly as downloaded
  employees      -> cleaned view: useless columns dropped, 0/1 flag and readable bands added

Run:  python load_data.py
"""
from pathlib import Path
import duckdb

RAW_CSV = Path("data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv")
SAMPLE_CSV = Path("data/sample/hr_attrition.csv")
DB_PATH = "hr.duckdb"

if not RAW_CSV.exists():
    raise FileNotFoundError(
        f"{RAW_CSV} not found. Run:\n"
        "kaggle datasets download -d pavansubhasht/ibm-hr-analytics-attrition-dataset "
        "-p data/raw --unzip"
    )

con = duckdb.connect(DB_PATH)

# 1) Raw layer: load the CSV as-is
con.execute(f"""
    CREATE OR REPLACE TABLE raw_employees AS
    SELECT * FROM read_csv_auto('{RAW_CSV.as_posix()}', header = true)
""")

# 2) Clean layer: drop constant columns, add analysis-friendly fields
con.execute("""
    CREATE OR REPLACE VIEW employees AS
    SELECT
        EmployeeNumber                         AS employee_id,
        Age                                    AS age,
        CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END AS left_company,
        BusinessTravel                         AS business_travel,
        Department                             AS department,
        JobRole                                AS job_role,
        JobLevel                               AS job_level,
        Gender                                 AS gender,
        MaritalStatus                          AS marital_status,
        Education                              AS education,
        EducationField                         AS education_field,
        DistanceFromHome                       AS distance_from_home,
        OverTime                               AS overtime,
        MonthlyIncome                          AS monthly_income,
        MonthlyIncome * 12                     AS annual_income,
        PercentSalaryHike                      AS pct_salary_hike,
        StockOptionLevel                       AS stock_option_level,
        PerformanceRating                      AS performance_rating,
        JobSatisfaction                        AS job_satisfaction,
        EnvironmentSatisfaction                AS environment_satisfaction,
        RelationshipSatisfaction               AS relationship_satisfaction,
        WorkLifeBalance                        AS work_life_balance,
        JobInvolvement                         AS job_involvement,
        NumCompaniesWorked                     AS num_companies_worked,
        TotalWorkingYears                      AS total_working_years,
        TrainingTimesLastYear                  AS training_times_last_year,
        YearsAtCompany                         AS years_at_company,
        YearsInCurrentRole                     AS years_in_current_role,
        YearsSinceLastPromotion                AS years_since_last_promotion,
        YearsWithCurrManager                   AS years_with_curr_manager,
        CASE
            WHEN YearsAtCompany < 2  THEN '0-1 yrs'
            WHEN YearsAtCompany < 5  THEN '2-4 yrs'
            WHEN YearsAtCompany < 10 THEN '5-9 yrs'
            ELSE '10+ yrs'
        END                                    AS tenure_band
    FROM raw_employees
    -- EmployeeCount, StandardHours and Over18 have one value for every row, so they are dropped
""")

# 3) Quick checks
rows, leavers = con.execute(
    "SELECT COUNT(*), SUM(left_company) FROM employees"
).fetchone()
print(f"Loaded {rows:,} employees ({leavers:,} left) into {DB_PATH}")

# 4) Save a copy for the Streamlit app (this file is small enough to commit)
SAMPLE_CSV.parent.mkdir(parents=True, exist_ok=True)
con.execute(f"COPY (SELECT * FROM employees) TO '{SAMPLE_CSV.as_posix()}' (HEADER)")
print(f"Wrote {SAMPLE_CSV}")

con.close()
