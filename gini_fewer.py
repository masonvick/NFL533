import pandas as pd
import numpy as np
from scipy.stats import gini
import matplotlib.pyplot as plt
import seaborn as sns

# Load salary data
salary_data = pd.read_csv("NFL_Salary_Cap_Historical.csv")

# Function to calculate GINI index
def calculate_gini(salaries):
    """Calculate GINI index from a list of salaries."""
    salaries = np.sort(salaries)  # Sort salaries
    n = len(salaries)
    cumulative_income = np.cumsum(salaries) / np.sum(salaries)
    cumulative_share = np.arange(1, n + 1) / n
    return np.sum(cumulative_share - cumulative_income)

# Analyze top N salaries (e.g., 10, 20)
top_n_results = []
for n in [10, 20]:
    grouped = salary_data.groupby(["Year", "Team"])
    for (year, team), group in grouped:
        # Get the top N salaries
        top_n_salaries = group.nlargest(n, "Salary")["Salary"]
        if len(top_n_salaries) >= n:  # Ensure there are at least N players
            gini_index = calculate_gini(top_n_salaries.values)
            top_n_results.append({"Year": year, "Team": team, "GINI": gini_index, "TopN": n})

# Convert results to DataFrame
gini_top_n_df = pd.DataFrame(top_n_results)

# Save results
gini_top_n_df.to_csv("GINI_TopN.csv", index=False)

# Plot GINI comparison (Top 10 vs. Top 20)
sns.boxplot(x="TopN", y="GINI", data=gini_top_n_df)
plt.title("GINI Index for Top N Salaries")
plt.xlabel("Top N Salaries")
plt.ylabel("GINI Index")
plt.grid()
plt.show()
