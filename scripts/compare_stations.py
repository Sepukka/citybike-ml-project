import pandas as pd
import glob

files_2024 = glob.glob("../data/raw/citybike/od-trips-2024/2024-*.csv")
files_2025 = glob.glob("../data/raw/citybike/od-trips-2025/2025-*.csv")

df_2024 = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files_2024],
    ignore_index=True
)

df_2025 = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files_2025],
    ignore_index=True
)

stations_2024 = set(
    df_2024["Departure station name"].dropna().unique()
)

stations_2025 = set(
    df_2025["Departure station name"].dropna().unique()
)

common_stations = stations_2024 & stations_2025
only_2024 = stations_2024 - stations_2025
only_2025 = stations_2025 - stations_2024

print("Stations in 2024:", len(stations_2024))
print("Stations in 2025:", len(stations_2025))
print("Common stations:", len(common_stations))

print("\nOnly in 2024:")
print(sorted(only_2024))

print("\nOnly in 2025:")
print(sorted(only_2025))

print("\nIs Itämerentori in both years?")
print("Itämerentori" in common_stations)