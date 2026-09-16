import pandas as pd 
import numpy as np

df = pd.read_csv("data/raw/citybike/2025-04.csv")

departures = np.zeros((30, 24), dtype=int)

print(df.head())

print(df.columns)

