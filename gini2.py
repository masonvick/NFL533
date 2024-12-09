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

# Function to calculate GINI indices for top N players
def calculate_gini_for_top_n(salary_data, top_n, output_file):
    gini_results = []

    for year in range(2013, 2024):  # 11 seasons
        for team in salary_data["Team"].unique():
            team_data = salary_data[
                (salary_data["Year"] == year) & (salary_data["Team"] == team)
            ]
            top_salaries = team_data["Contract"].apply(
                lambda x: float(x.replace("$", "").replace(",", ""))
            ).sort_values(ascending=False).head(top_n)
            gini = calculate_gini(top_salaries.values)
            gini_results.append({"Year": year, "Team": team, "GINI": gini})

    # Convert results to DataFrame and save to CSV
    gini_df = pd.DataFrame(gini_results)
    gini_df.to_csv(output_file, index=False)
    print(f"GINI indices saved to {output_file}")

# Calculate GINI indices for top 40, 30, and 20 players
calculate_gini_for_top_n(salary_data, 40, "Top40_GINI_Indices.csv")
calculate_gini_for_top_n(salary_data, 30, "Top30_GINI_Indices.csv")
calculate_gini_for_top_n(salary_data, 20, "Top20_GINI_Indices.csv")
