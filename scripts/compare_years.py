import pandas as pd
import glob

station_name = "Itämerentori"

files_2024 = glob.glob(
    "../data/raw/citybike/od-trips-2024/2024-*.csv"
)

files_2025 = glob.glob(
    "../data/raw/citybike/od-trips-2025/2025-*.csv"
)

df_2024 = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files_2024],
    ignore_index=True
)

df_2025 = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files_2025],
    ignore_index=True
)

df_2024["Departure station name"] = (
    df_2024["Departure station name"].str.strip()
)

df_2025["Departure station name"] = (
    df_2025["Departure station name"].str.strip()
)

df_2024["Departure"] = pd.to_datetime(
    df_2024["Departure"],
    format="mixed"
)

df_2025["Departure"] = pd.to_datetime(
    df_2025["Departure"],
    format="mixed"
)

station_2024 = df_2024[
    df_2024["Departure station name"] == station_name
].copy()

station_2025 = df_2025[
    df_2025["Departure station name"] == station_name
].copy()

station_2024["month"] = station_2024["Departure"].dt.month_name()
station_2025["month"] = station_2025["Departure"].dt.month_name()

month_order = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October"
]

print("Total departures")
print("2024:", len(station_2024))
print("2025:", len(station_2025))

print("\nMonthly departures")

monthly_2024 = (
    station_2024
    .groupby("month")
    .size()
)

monthly_2025 = (
    station_2025
    .groupby("month")
    .size()
)

comparison = pd.DataFrame({
    "2024": monthly_2024,
    "2025": monthly_2025
})

comparison = comparison.reindex(month_order)

print(comparison)

print("\nDifference 2025 - 2024")

comparison["difference"] = (
    comparison["2025"] - comparison["2024"]
)

print(comparison)