import pandas as pd
import nfl_data_py as nfl

# Specify the range of years you want to fetch data for
start_year = 2013
end_year = 2023

# Fetch game schedules (both REG and POST combined)
print("Fetching combined schedules (REG + POST)...")
try:
    all_schedules = nfl.import_schedules([year for year in range(start_year, end_year + 1)])
    print(f"Data fetched: {all_schedules.shape}")
    print("Unique game types:", all_schedules["game_type"].unique())  # Debug game types
except Exception as e:
    print(f"Error fetching schedules: {e}")
    exit()

# Ensure required columns exist
required_columns = ["season", "home_team", "away_team", "home_score", "away_score", "game_type"]
if not all(col in all_schedules.columns for col in required_columns):
    print("Required columns not found in the dataset.")
    exit()

# Separate regular season and postseason games
regular_season = all_schedules[all_schedules["game_type"] == "REG"]
postseason = all_schedules[all_schedules["game_type"].isin(["WC", "DIV", "CON", "SB"])]

# Debug: Check data availability
if regular_season.empty:
    print("No regular season data found.")
if postseason.empty:
    print("No postseason data found.")

# Function to calculate standings
def calculate_standings(df):
    results = []
    for _, row in df.iterrows():
        season = row["season"]
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_score = row["home_score"]
        away_score = row["away_score"]

        if home_score > away_score:
            results.append({"season": season, "team": home_team, "result": "win"})
            results.append({"season": season, "team": away_team, "result": "loss"})
        elif away_score > home_score:
            results.append({"season": season, "team": away_team, "result": "win"})
            results.append({"season": season, "team": home_team, "result": "loss"})
        else:
            results.append({"season": season, "team": home_team, "result": "tie"})
            results.append({"season": season, "team": away_team, "result": "tie"})

    results_df = pd.DataFrame(results)
    standings = results_df.groupby(["season", "team", "result"]).size().unstack(fill_value=0).reset_index()
    standings.rename(columns={"win": "wins", "loss": "losses", "tie": "ties"}, inplace=True)
    return standings

# Calculate regular season standings
regular_season_standings = calculate_standings(regular_season)

# Calculate postseason standings
postseason_standings = calculate_standings(postseason)

# Add playoff qualification to regular season standings
regular_season_standings["made_playoffs"] = regular_season_standings["team"].isin(postseason["home_team"]).astype(int) | \
                                            regular_season_standings["team"].isin(postseason["away_team"]).astype(int)

# Merge playoff performance into regular season standings
playoff_performance = postseason_standings.rename(columns={"wins": "playoff_wins", "losses": "playoff_losses", "ties": "playoff_ties"})
final_standings = pd.merge(regular_season_standings, playoff_performance, on=["season", "team"], how="left")
final_standings.fillna({"playoff_wins": 0, "playoff_losses": 0, "playoff_ties": 0}, inplace=True)

# Save to CSV
final_standings.to_csv("NFL_Team_Standings_2013_2023.csv", index=False)
print("Final standings saved to NFL_Team_Standings_2013_2023.csv")
