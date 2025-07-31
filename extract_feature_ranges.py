import pandas as pd
import json

files = [
    'tuesday_plus_cleaned.csv',
    'wednesday_plus_cleaned.csv',
    'thursday_plus_cleaned.csv',
    'friday_plus_cleaned.csv'
]

df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)

df = df.select_dtypes(include=['number'])

feature_ranges = {}
for col in df.columns:
    min_val = df[col].min()
    max_val = df[col].max()
    feature_ranges[col] = (float(min_val), float(max_val))

with open("feature_ranges.json", "w") as f:
    json.dump(feature_ranges, f, indent=2)

print("Feature ranges saved to feature_ranges.json")

