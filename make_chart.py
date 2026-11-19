from pathlib import Path
import duckdb
import matplotlib.pyplot as plt

Path("images").mkdir(exist_ok=True)
con = duckdb.connect("hr.duckdb", read_only=True)
overall = con.execute("SELECT 100.0 * AVG(left_company) FROM employees").fetchone()[0]

segments = con.execute("""
    WITH q AS (SELECT *, NTILE(4) OVER (ORDER BY monthly_income) AS income_quartile FROM employees)
    SELECT 'Sales Representatives' AS segment, 100.0 * AVG(left_company) AS pct FROM q WHERE job_role = 'Sales Representative'
    UNION ALL SELECT 'First 2 years at company', 100.0 * AVG(left_company) FROM q WHERE years_at_company < 2
    UNION ALL SELECT 'Works overtime',           100.0 * AVG(left_company) FROM q WHERE overtime = 'Yes'
    UNION ALL SELECT 'Lowest pay quartile',      100.0 * AVG(left_company) FROM q WHERE income_quartile = 1
    UNION ALL SELECT 'No overtime',              100.0 * AVG(left_company) FROM q WHERE overtime = 'No'
    UNION ALL SELECT 'Top pay quartile',         100.0 * AVG(left_company) FROM q WHERE income_quartile = 4
""").df().sort_values("pct")
con.close()

colors = ["#c0392b" if p > overall else "#7f8c8d" for p in segments["pct"]]
fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.barh(segments["segment"], segments["pct"], color=colors)
ax.axvline(overall, color="#2c3e50", linestyle="--", linewidth=1)
ax.text(overall + 0.5, -0.6, f"Company average {overall:.1f}%", color="#2c3e50", fontsize=9)
for bar, p in zip(bars, segments["pct"]):
    ax.text(p + 0.5, bar.get_y() + bar.get_height() / 2, f"{p:.1f}%", va="center", fontsize=9)
ax.set_title("Attrition rate by employee segment (IBM HR data, n = 1,470)", loc="left", fontsize=11)
ax.set_xlabel("Share of employees who left (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlim(0, max(segments["pct"]) + 8)
plt.tight_layout()
plt.savefig("images/attrition_drivers.png", dpi=160)
print("Saved images/attrition_drivers.png")