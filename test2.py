#Initial scraping of data from spotrac
import requests
import csv
from bs4 import BeautifulSoup
from csv import writer
import time

# Add headers as a dictionary, not a list
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# List of all NFL teams
teams = [
    "arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills",
    "carolina-panthers", "chicago-bears", "cincinnati-bengals", "cleveland-browns",
    "dallas-cowboys", "denver-broncos", "detroit-lions", "green-bay-packers",
    "houston-texans", "indianapolis-colts", "jacksonville-jaguars", "kansas-city-chiefs",
    "las-vegas-raiders", "los-angeles-chargers", "los-angeles-rams", "miami-dolphins",
    "minnesota-vikings", "new-england-patriots", "new-orleans-saints", "new-york-giants",
    "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers", "san-francisco-49ers",
    "seattle-seahawks", "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"
]

# Create master CSV file
with open("NFL_Salary_Cap_All_Teams.csv", "w", newline='', encoding='utf-8') as csvFile:
    csv_writer = writer(csvFile)
    headers_csv = ["Team", "Player", "Position", "Contract"]
    csv_writer.writerow(headers_csv)

    # Loop through each team
    for team in teams:
        print(f"\nProcessing {team}...")
        
        try:
            # Get the page with updated URL structure
            url = f"https://www.spotrac.com/nfl/{team}/cap/_/year/2024"
            response = requests.get(url, headers=headers)
            
            # Check if request was successful
            if response.status_code != 200:
                print(f"Failed to get data for {team}. Status code: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract data
            player_cells = soup.find_all("td", class_="text-left sticky left-0")
            position_cells = soup.find_all("td", class_="w-50p text-center")
            salary_cells = soup.find_all("td", class_="highlight w-125p text-center")

            # Extract player names
            player_list = []
            for cell in player_cells:
                player_text = cell.text.strip().split('\n')[0]
                player_list.append(player_text)

            # Extract positions (every other w-50p cell contains position)
            position_list = []
            for i in range(0, len(position_cells), 2):
                position_list.append(position_cells[i].text.strip())

            # Extract salaries
            salary_list = []
            for cell in salary_cells:
                salary_list.append(cell.text.strip())

            # Print debug info
            print(f"Found {len(player_list)} players")
            print(f"Found {len(position_list)} positions")
            print(f"Found {len(salary_list)} salaries")

            # Write data for this team
            min_length = min(len(player_list), len(position_list), len(salary_list))
            if min_length > 0:
                for i in range(min_length):
                    csv_writer.writerow([
                        team.replace("-", " ").title(),
                        player_list[i],
                        position_list[i],
                        salary_list[i]
                    ])
                print(f"Successfully added {min_length} players from {team}")
            else:
                print(f"No data found for {team}")

            # Add a delay between requests
            time.sleep(3)  # Increased delay to be more conservative

        except Exception as e:
            print(f"Error processing {team}: {str(e)}")
            continue

print("\nAll teams have been processed and saved to NFL_Salary_Cap_All_Teams.csv")

# Print final verification
try:
    with open("NFL_Salary_Cap_All_Teams.csv", "r", encoding='utf-8') as f:
        line_count = sum(1 for line in f) - 1  # Subtract 1 for header
        print(f"Total players written to CSV: {line_count}")
except Exception as e:
    print(f"Error verifying file: {str(e)}")