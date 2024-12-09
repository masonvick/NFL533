import nfl_data_py as nfl
import pandas as pd

# Specify the range of years
start_year = 2013
end_year = 2023
years = list(range(start_year, end_year + 1))

all_years_data = []

print("Importing PBP data for all years...")
pbp_all = nfl.import_pbp_data(years=years, downcast=True)  # Load all years at once

# We now have a DataFrame pbp_all containing all the plays from 2013 to 2023.

# Calculate offense and defense EPA per play by year
for yr in years:
    pbp_year = pbp_all[pbp_all["season"] == yr].copy()

    # Average offensive EPA/play: group by posteam
    # posteam is the team on offense
    offense_df = pbp_year.groupby("posteam", as_index=False)["epa"].mean()
    offense_df.rename(columns={"posteam": "team", "epa": "offense_epa_per_play"}, inplace=True)

    # Average defensive EPA/play: group by defteam
    # defteam is the team on defense
    defense_df = pbp_year.groupby("defteam", as_index=False)["epa"].mean()
    defense_df.rename(columns={"defteam": "team", "epa": "defense_epa_per_play"}, inplace=True)

    # Merge offense and defense on team
    merged_df = pd.merge(offense_df, defense_df, on="team", how="outer")
    merged_df["season"] = yr

    all_years_data.append(merged_df)

# Combine all years
final_df = pd.concat(all_years_data, ignore_index=True)

# Optionally sort by season then team
final_df.sort_values(["season", "team"], inplace=True)

# Save to CSV
final_df.to_csv("team_offense_defense_epa_per_play_2013_2023.csv", index=False)
print("CSV file saved: team_offense_defense_epa_per_play_2013_2023.csv")
