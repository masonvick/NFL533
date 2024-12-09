import requests
import csv
from bs4 import BeautifulSoup
import time

headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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

def get_player_data(soup, class_name, limit):
   cells = soup.find_all("td", class_=class_name)
   return [cell.text.strip().split('\n')[0] for cell in cells[:limit]]

def get_position_data(position_cells, limit):
   return [position_cells[i].text.strip() for i in range(0, min(len(position_cells), limit*2), 2)]

def convert_salary_to_float(salary):
   try:
       return float(salary.replace('$', '').replace(',', ''))
   except:
       return 0

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

               # Regular roster
               regular_players = []
               player_cells = soup.find_all("td", class_="text-left sticky left-0")[:50]
               position_cells = soup.find_all("td", class_="w-50p text-center")
               salary_cells = soup.find_all("td", class_="highlight w-125p text-center")[:50]

               for i in range(min(len(player_cells), len(salary_cells))):
                   if i < len(position_cells)//2:
                       regular_players.append((
                           player_cells[i].text.strip().split('\n')[0],
                           position_cells[i*2].text.strip(),
                           salary_cells[i].text.strip(),
                           "Active"
                       ))

               # IR List - look for div with IR players
               ir_section = soup.find("div", class_="ir-list")
               if ir_section:
                   ir_player_cells = ir_section.find_all("td", class_="text-left sticky left-0")[:5]
                   ir_position_cells = ir_section.find_all("td", class_="w-50p text-center")
                   ir_salary_cells = ir_section.find_all("td", class_="highlight w-125p text-center")[:5]
                   
                   for i in range(min(len(ir_player_cells), len(ir_salary_cells))):
                       if i < len(ir_position_cells)//2:
                           regular_players.append((
                               ir_player_cells[i].text.strip().split('\n')[0],
                               ir_position_cells[i*2].text.strip(),
                               ir_salary_cells[i].text.strip(),
                               "IR"
                           ))

               # Sort all players by salary and take top 50
               regular_players.sort(
                   key=lambda x: convert_salary_to_float(x[2]), 
                   reverse=True
               )
               
               # Write top 50 to CSV
               for player in regular_players[:50]:
                   csv_writer.writerow([
                       year,
                       team.replace("-", " ").title(),
                       player[0],  # Player name
                       player[1],  # Position
                       player[2],  # Salary
                       player[3]   # Status
                   ])

               print(f"Successfully added {min(50, len(regular_players))} players from {team} {year}")
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