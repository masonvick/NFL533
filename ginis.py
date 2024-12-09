import pandas as pd
import numpy as np

# Load the salary data
file_path = "NFL_Salary_Cap_Historical.csv"  # Update the path as needed
salary_data = pd.read_csv(file_path)

# Function to calculate GINI index
def calculate_gini(salaries):
    n = len(salaries)
    if n == 0:
        return np.nan  # Handle cases with no data
    mean_salary = np.mean(salaries)
    if mean_salary == 0:
        return 0  # Handle cases where all salaries are zero
    diffs = np.abs(np.subtract.outer(salaries, salaries)).sum()
    gini = diffs / (2 * n**2 * mean_salary)
    return gini

# Prepare a DataFrame to store GINI indices
gini_results = []

# Loop through each team and season
for year in range(2013, 2024):  # 11 seasons
    for team in salary_data["Team"].unique():
        team_data = salary_data[
            (salary_data["Year"] == year) & (salary_data["Team"] == team)
        ]
        top_50_salaries = team_data["Contract"].apply(
            lambda x: float(x.replace("$", "").replace(",", ""))
        ).sort_values(ascending=False).head(50)
        gini = calculate_gini(top_50_salaries.values)
        gini_results.append({"Year": year, "Team": team, "GINI": gini})

# Convert results to DataFrame
gini_df = pd.DataFrame(gini_results)

# Save GINI indices to a CSV
output_path = "NFL_Team_GINI_Indices.csv"
gini_df.to_csv(output_path, index=False)

print(f"GINI indices saved to {output_path}")
