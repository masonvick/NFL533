import pandas as pd

# Load data files
epa_data = pd.read_csv('team_offense_defense_epa_per_play_2013_2023.csv')
gini_20 = pd.read_csv('Top20_GINI_Indices.csv')
gini_30 = pd.read_csv('Top30_GINI_Indices.csv')
gini_40 = pd.read_csv('Top40_GINI_Indices.csv')
gini_50 = pd.read_csv('Top50_GINI_Indices.csv')

# Team name mapping
team_name_mapping = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "LV": "Las Vegas Raiders",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SEA": "Seattle Seahawks",
    "SF": "San Francisco 49ers",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders"
}

# Map abbreviations to full team names in the EPA dataset
epa_data['team_full_name'] = epa_data['team'].map(team_name_mapping)

# Merge data using full team names and season/year
combined_data = epa_data.merge(gini_20, left_on=['team_full_name', 'season'], right_on=['Team', 'Year'], suffixes=('', '_gini20'))
combined_data = combined_data.merge(gini_30, left_on=['team_full_name', 'season'], right_on=['Team', 'Year'], suffixes=('', '_gini30'))
combined_data = combined_data.merge(gini_40, left_on=['team_full_name', 'season'], right_on=['Team', 'Year'], suffixes=('', '_gini40'))
combined_data = combined_data.merge(gini_50, left_on=['team_full_name', 'season'], right_on=['Team', 'Year'], suffixes=('', '_gini50'))

# Drop duplicate columns if any
combined_data = combined_data.drop(columns=['Team_gini20', 'Year_gini20', 'Team_gini30', 'Year_gini30', 'Team_gini40', 'Year_gini40', 'Team_gini50', 'Year_gini50'], errors='ignore')

# Save combined data
combined_data.to_csv('combined_data.csv', index=False)

print("Data combined successfully and saved as 'combined_data.csv'.")
