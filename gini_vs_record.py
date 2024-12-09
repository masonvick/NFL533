import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file mappings for GINI data
gini_files = {
    #"Top50_GINI_Indices.csv": "Top 50 Salaries",
    "Top40_GINI_Indices.csv": "Top 40 Salaries",
    "Top30_GINI_Indices.csv": "Top 30 Salaries",
    "Top20_GINI_Indices.csv": "Top 20 Salaries"
}

# Load standings data
standings_data = pd.read_csv("NFL_Team_Standings_2013_2023.csv")

# Create mapping of full team names to abbreviations
team_mapping = {
    "arizona cardinals": "ari",
    "atlanta falcons": "atl",
    "baltimore ravens": "bal",
    "buffalo bills": "buf",
    "carolina panthers": "car",
    "chicago bears": "chi",
    "cincinnati bengals": "cin",
    "cleveland browns": "cle",
    "dallas cowboys": "dal",
    "denver broncos": "den",
    "detroit lions": "det",
    "green bay packers": "gb",
    "houston texans": "hou",
    "indianapolis colts": "ind",
    "jacksonville jaguars": "jax",
    "kansas city chiefs": "kc",
    "las vegas raiders": "lv",
    "los angeles chargers": "lac",
    "los angeles rams": "la",
    "miami dolphins": "mia",
    "minnesota vikings": "min",
    "new england patriots": "ne",
    "new orleans saints": "no",
    "new york giants": "nyg",
    "new york jets": "nyj",
    "philadelphia eagles": "phi",
    "pittsburgh steelers": "pit",
    "san francisco 49ers": "sf",
    "seattle seahawks": "sea",
    "tampa bay buccaneers": "tb",
    "tennessee titans": "ten",
    "washington commanders": "was"
}

# Normalize standings data
standings_data["team"] = standings_data["team"].str.lower().str.strip()
standings_data["season"] = standings_data["season"].astype(int)

for file, title_suffix in gini_files.items():
    # Load GINI data
    gini_data = pd.read_csv(file)

    # Normalize and map team names
    gini_data["Team"] = gini_data["Team"].str.lower().str.strip().map(team_mapping)
    gini_data["Year"] = gini_data["Year"].astype(int)

    # Merge GINI indices with team standings
    merged_data = pd.merge(
        gini_data,
        standings_data,
        how="inner",
        left_on=["Year", "Team"],
        right_on=["season", "team"]
    )

    # Debug merged data
    print(f"\nMerged Data Info for {title_suffix}:")
    print(merged_data.info())
    if merged_data.empty:
        print(f"No rows matched for {title_suffix}. Skipping.")
        continue

    # Create derived columns
    merged_data["win_percentage"] = merged_data["wins"] / (
        merged_data["wins"] + merged_data["losses"]
    )
    merged_data["playoff_success"] = merged_data["playoff_wins"]

    # Recalculate correlations
    correlation = merged_data[["GINI", "win_percentage", "playoff_success"]].corr()
    print(f"\nCorrelation Matrix for {title_suffix}:")
    print(correlation)

    # Visualize relationships
    sns.scatterplot(x="GINI", y="win_percentage", data=merged_data)
    plt.title(f"GINI Index vs. Win Percentage ({title_suffix})")
    plt.xlabel("GINI Index")
    plt.ylabel("Win Percentage")
    plt.grid()
    plt.savefig(f"GINI_vs_WinPercentage_{title_suffix.replace(' ', '_')}.png")
    plt.show()

    sns.scatterplot(x="GINI", y="playoff_success", data=merged_data)
    plt.title(f"GINI Index vs. Playoff Success ({title_suffix})")
    plt.xlabel("GINI Index")
    plt.ylabel("Playoff Wins")
    plt.grid()
    plt.savefig(f"GINI_vs_PlayoffSuccess_{title_suffix.replace(' ', '_')}.png")
    plt.show()

print("Scatterplots created for all GINI datasets.")
