import pandas as pd 
import glob 

files = glob.glob("../data/raw/citybike/od-trips-2025/2025-*.csv")

df_list = []

for file in files:
    temp_df = pd.read_csv(file, low_memory=False)
    df_list.append(temp_df)

df = pd.concat(df_list, ignore_index=True)


df["Departure"] = pd.to_datetime(df["Departure"], format="mixed")

df = df[
    (df["Departure"] >= "2025-04-01") &
    (df["Departure"] < "2025-11-01")
]

df["datetime_hour"] = df["Departure"].dt.floor("h")

hourly_departures = (
    df.groupby(["Departure station name", "datetime_hour"])
    .size()
    .reset_index(name="departures")
)

all_hours = pd.date_range(
    start="2025-04-01 00:00:00",
    end="2025-10-31 23:00:00",
    freq="h"
)

stations = df["Departure station name"].dropna().unique()

full_index = pd.MultiIndex.from_product(
    [stations, all_hours],
    names=["Departure station name", "datetime_hour"]
)

hourly_departures = (
    hourly_departures
    .set_index(["Departure station name", "datetime_hour"])
    .reindex(full_index, fill_value=0)
    .reset_index()
)

itämerentori = hourly_departures[
    hourly_departures["Departure station name"] == "Itämerentori"
].copy()

itämerentori["hour"] = itämerentori["datetime_hour"].dt.hour
itämerentori["weekday"] = itämerentori["datetime_hour"].dt.day_name()
itämerentori["month"] = itämerentori["datetime_hour"].dt.month_name()


weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

month_order = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October"
]

mean_by_hour = (
    itämerentori
    .groupby("hour")["departures"]
    .mean()
)

print(mean_by_hour)

mean_by_weekday = (
    itämerentori
    .groupby("weekday")["departures"]
    .mean()
)

print(mean_by_weekday[weekday_order])

mean_by_hour_weekday = (
    itämerentori
    .groupby(["hour", "weekday"])["departures"]
    .mean()
)



table = mean_by_hour_weekday.unstack()
table = table[weekday_order]

print(table)

mean_by_month = (
    itämerentori
    .groupby(["month"])["departures"]
    .mean()
)

print(mean_by_month[month_order])
