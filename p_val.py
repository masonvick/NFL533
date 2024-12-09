import pandas as pd
from scipy.stats import pearsonr

# Load the combined data
data = pd.read_csv('combined_data.csv')

# Define the columns for EPA metrics and Gini indices
epa_metrics = ['offense_epa_per_play', 'defense_epa_per_play']
gini_indices = ['GINI_gini20', 'GINI_gini30', 'GINI_gini40', 'GINI_gini50']

# Ensure the Gini columns exist in the data
data.rename(columns={
    'GINI': 'GINI_gini20',
    'GINI_gini30': 'GINI_gini30',
    'GINI_gini40': 'GINI_gini40',
    'GINI_gini50': 'GINI_gini50'
}, inplace=True)

# Initialize a list to store results
results = []

# Calculate Pearson correlation and p-values for each combination
for epa_metric in epa_metrics:
    for gini_index in gini_indices:
        if gini_index in data.columns:  # Check if the Gini index column exists
            corr, p_value = pearsonr(data[epa_metric], data[gini_index])
            results.append({
                'EPA Metric': epa_metric,
                'Gini Index': gini_index,
                'Correlation': corr,
                'P-Value': p_value
            })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv('correlation_results.csv', index=False)

# Print a confirmation message
print("Correlation analysis completed. Results saved to 'correlation_results.csv'.")
