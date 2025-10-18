import pandas as pd
from main import load_data

loaded_data = load_data("../grating2AFC S11.mat")

df = pd.DataFrame(loaded_data)

# Convert to CSV and save to file
df.to_csv('../grating2AFC_S11.csv', index = False) # index=False removes the row numbers