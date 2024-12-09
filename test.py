#Initial scraping of data from spotrac
import requests
import csv
from bs4 import BeautifulSoup
from csv import writer

# Add headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get("https://www.spotrac.com/nfl/arizona-cardinals/cap/#", headers=headers).text
soup = BeautifulSoup(response, "html.parser")

# Updated selectors based on the actual HTML structure
player_cells = soup.find_all("td", class_="text-left sticky left-0")
position_cells = soup.find_all("td", class_="w-50p text-center")
salary_cells = soup.find_all("td", class_="highlight w-125p text-center")

# Extract player names
player_list = []
for cell in player_cells:
    player_text = cell.text.strip().split('\n')[0]  # Get just the first line which is the player name
    player_list.append(player_text)
print(f"Players found: {len(player_list)}")

# Extract positions (every other w-50p cell contains position)
position_list = []
for i in range(0, len(position_cells), 2):  # Skip every other cell since we see pattern of position,age
    position_list.append(position_cells[i].text.strip())
print(f"Positions found: {len(position_list)}")

# Extract salaries (the highlighted cells contain the cap hit)
salary_list = []
for cell in salary_cells:
    salary_list.append(cell.text.strip())
print(f"Salaries found: {len(salary_list)}")

# Print the first few entries of each list to verify data
print("\nFirst 5 entries of each list:")
print("Players:", player_list[:5])
print("Positions:", position_list[:5])
print("Salaries:", salary_list[:5])

# Write to CSV if we have data
if len(player_list) > 0 and len(position_list) > 0 and len(salary_list) > 0:
    with open("salaryCap1.csv", "w", newline='', encoding='utf-8') as csvFile:
        csv_writer = writer(csvFile)
        headers = ["Player", "Position", "Contract"]
        csv_writer.writerow(headers)
        for i in range(min(len(player_list), len(position_list), len(salary_list))):
            csv_writer.writerow([player_list[i], position_list[i], salary_list[i]])
    print("\nCSV file has been written successfully")
else:
    print("\nNo data was written to CSV because one or more lists are empty")