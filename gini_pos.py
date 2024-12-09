import pandas as pd
import numpy as np

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

# Load the salary data
salary_data = pd.read_csv("NFL_Salary_Cap_Historical.csv")

# Debug: Display column names
print("Columns in salary data:", salary_data.columns)

# Convert 'Contract' column to numeric (removing $ and commas)
if 'Contract' in salary_data.columns:
    salary_data['Contract'] = salary_data['Contract'].replace(
        {'\$': '', ',': ''}, regex=True
    ).astype(float)
else:
    raise KeyError("Contract column not found in the dataset. Please verify the column name.")

# Define the list of positions to analyze
positions = ['QB', 'WR', 'RB', 'OL', 'DL', 'LB', 'CB', 'S', 'TE', 'K', 'P']

# Prepare an empty DataFrame to store GINI indices
gini_by_position = []

# Loop through each year and team
for year in salary_data['Year'].unique():
    for team in salary_data['Team'].unique():
        for position in positions:
            # Filter salaries for the current year, team, and position
            filtered_data = salary_data[
                (salary_data['Year'] == year) &
                (salary_data['Team'] == team) &
                (salary_data['Position'] == position)
            ]
            
            # Debug: Display filtered data sample
            print(f"Filtered data for Year {year}, Team {team}, Position {position}:\n", filtered_data.head())
            
            # Extract salaries
            salaries = filtered_data['Contract'].dropna().values

            # Calculate the GINI index if there are salaries available
            if len(salaries) > 0:
                gini_index = calculate_gini(salaries)
            else:
                gini_index = None
            
            # Store the result
            gini_by_position.append({
                'Year': year,
                'Team': team,
                'Position': position,
                'GINI': gini_index
            })

# Convert to a DataFrame
gini_by_position_df = pd.DataFrame(gini_by_position)

# Save to CSV
gini_by_position_df.to_csv("NFL_Position_GINI_Indices.csv", index=False)
print("GINI indices by position saved to NFL_Position_GINI_Indices.csv")
