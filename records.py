import pandas as pd

# Load the schedules data
schedules = pd.read_csv("NFL_Schedules.csv")

# Inspect the first few rows to understand structure
print(schedules.head())

# Ensure relevant columns exist
if all(col in schedules.columns for col in ["season", "home_team", "away_team", "home_score", "away_score"]):
    # Initialize a list to store results
    records = []

    # Process each game to calculate results
    for _, row in schedules.iterrows():
        season = row["season"]
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_score = row["home_score"]
        away_score = row["away_score"]

        # Determine game result
        if home_score > away_score:
            records.append({"season": season, "team": home_team, "result": "win"})
            records.append({"season": season, "team": away_team, "result": "loss"})
        elif away_score > home_score:
            records.append({"season": season, "team": away_team, "result": "win"})
            records.append({"season": season, "team": home_team, "result": "loss"})
        else:
            records.append({"season": season, "team": home_team, "result": "tie"})
            records.append({"season": season, "team": away_team, "result": "tie"})

    # Convert results to a DataFrame
    results_df = pd.DataFrame(records)

    # Calculate standings
    standings = results_df.groupby(["season", "team", "result"]).size().unstack(fill_value=0).reset_index()
    standings.rename(columns={"win": "wins", "loss": "losses", "tie": "ties"}, inplace=True)

    # Save standings to a CSV
    standings.to_csv("NFL_Team_Standings_Processed.csv", index=False)
    print("Standings saved to NFL_Team_Standings_Processed.csv")
else:
    print("Required columns not found in the dataset.")
