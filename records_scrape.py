import nfl_data_py as nfl
import pandas as pd

# Specify the range of years you want to fetch data for
start_year = 2013
end_year = 2022

# Initialize a DataFrame to store the results
all_schedules = pd.DataFrame()

for year in range(start_year, end_year + 1):
    print(f"Fetching schedules for {year}...")
    
    try:
        # Fetch game schedules for the year
        schedules = nfl.import_schedules([year])
        
        # Debug: Print the shape and a sample of the data
        print(f"Schedules fetched for {year}: {schedules.shape}")
        print(schedules.head())
        
        # Append data to the final DataFrame
        all_schedules = pd.concat([all_schedules, schedules], ignore_index=True)
    except Exception as e:
        print(f"Error fetching schedules for {year}: {e}")

# Save all schedules to a CSV
if not all_schedules.empty:
    all_schedules.to_csv("NFL_Schedules.csv", index=False)
    print("Schedules saved to NFL_Schedules.csv")
else:
    print("No data to write. Please check the logs for errors.")
