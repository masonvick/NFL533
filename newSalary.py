import requests
import csv
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

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

def convert_salary_to_float(salary):
    try:
        return float(salary.replace('$', '').replace(',', '').replace('(', '').replace(')', ''))
    except:
        return 0.0

def parse_player_rows(section_soup):
    """Parse player rows from a given BeautifulSoup section and return a list of tuples:
       (PlayerName, Position, Salary, Status)
    """
    players = []
    player_cells = section_soup.find_all("td", class_="text-left sticky left-0")
    position_cells = section_soup.find_all("td", class_="w-50p text-center")
    salary_cells = section_soup.find_all("td", class_="highlight w-125p text-center")

    limit = min(len(player_cells), len(salary_cells))

    for i in range(limit):
        player_cell = player_cells[i]
        name = player_cell.text.strip().split('\n')[0]

        # Determine position index
        pos_index = i * 2
        position = position_cells[pos_index].text.strip() if pos_index < len(position_cells) else ""

        salary = salary_cells[i].text.strip()

        # Identify status from the link class
        # Find the 'a' tag in player_cell
        a_tag = player_cell.find("a", class_="link")
        if a_tag:
            link_classes = a_tag.get("class", [])
            # link_classes might be something like ["link", "injured-reserve"] or ["link", "dead-money"]
            if "injured-reserve" in link_classes:
                status = "IR"
            elif "dead-money" in link_classes:
                status = "Dead"
            else:
                status = "Active"
        else:
            status = "Active"

        players.append((name, position, salary, status))

    return players

with open("NFL_Salary_Cap_Historical.csv", "w", newline='', encoding='utf-8') as csvFile:
    csv_writer = csv.writer(csvFile)
    csv_writer.writerow(["Year", "Team", "Player", "Position", "Contract", "Status"])

    for year in range(2013, 2024):
        print(f"\nProcessing year {year}...")

        for team in teams:
            print(f"Processing {team} for {year}...")

            try:
                url = f"https://www.spotrac.com/nfl/{team}/cap/_/year/{year}"
                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    print(f"Failed to get data for {team} {year}. Status code: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                all_players = []

                # Active / Main roster
                main_section = soup.find("div", class_="main")
                if main_section:
                    active_players = parse_player_rows(main_section)
                    all_players.extend(active_players)
                else:
                    # If for some reason main_section isn't found, try whole soup
                    active_players = parse_player_rows(soup)
                    all_players.extend(active_players)

                # IR SECTION
                ir_section = soup.find("div", class_="ir-list")
                if ir_section:
                    ir_players = parse_player_rows(ir_section)
                    all_players.extend(ir_players)

                # DEAD CAP SECTION
                dead_section = soup.find("div", class_="dead-money-list")
                if dead_section:
                    dead_players = parse_player_rows(dead_section)
                    all_players.extend(dead_players)

                # Sort by salary descending and take top 50
                all_players.sort(key=lambda x: convert_salary_to_float(x[2]), reverse=True)
                top_50 = all_players[:50]

                for player in top_50:
                    csv_writer.writerow([
                        year,
                        team.replace("-", " ").title(),
                        player[0],
                        player[1],
                        player[2],
                        player[3]
                    ])

                print(f"Successfully added {min(50, len(all_players))} players from {team} {year}")
                time.sleep(1)

            except Exception as e:
                print(f"Error processing {team} {year}: {str(e)}")
                continue

        print(f"Completed year {year}")

print("\nAll years have been processed and saved to NFL_Salary_Cap_Historical.csv")
try:
    with open("NFL_Salary_Cap_Historical.csv", "r", encoding='utf-8') as f:
        line_count = sum(1 for line in f) - 1
        print(f"Total records written to CSV: {line_count}")
except Exception as e:
    print(f"Error verifying file: {str(e)}")
