"""
run_queries.py
Runs every .sql file in sql/ against hr.duckdb, prints each result,
and saves it to results/<query_name>.csv.

Run:  python run_queries.py
"""
from pathlib import Path
import duckdb

SQL_DIR = Path("sql")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

con = duckdb.connect("hr.duckdb", read_only=True)

for sql_file in sorted(SQL_DIR.glob("*.sql")):
    query = sql_file.read_text()
    question = query.splitlines()[0].lstrip("- ").strip()   # first comment line = the question
    df = con.execute(query).df()

    print("\n" + "=" * 80)
    print(question)
    print("=" * 80)
    print(df.to_string(index=False))

    df.to_csv(RESULTS_DIR / f"{sql_file.stem}.csv", index=False)

con.close()
print(f"\nSaved {len(list(SQL_DIR.glob('*.sql')))} result files to {RESULTS_DIR}/")
