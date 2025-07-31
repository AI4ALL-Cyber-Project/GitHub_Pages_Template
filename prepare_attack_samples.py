import pandas as pd
import os

# List of cleaned CSV files
files = [
    "tuesday_plus_cleaned.csv",
    "wednesday_plus_cleaned.csv",
    "thursday_plus_cleaned.csv",
    "friday_plus_cleaned.csv"
]

attack_samples = []

for file in files:
    if os.path.exists(file):
        print(f"Loading {file}")
        df = pd.read_csv(file)
        df['Label'] = df['Label'].str.upper()
        df['Label'] = df['Label'].apply(lambda x: 'Benign' if x == 'BENIGN' else 'Attack')
        attack_df = df[df['Label'] == 'Attack'].drop(columns=['Label'])
        attack_samples.append(attack_df)
    else:
        print(f"⚠️ File not found: {file}")

# Combine all attack samples into one DataFrame
if attack_samples:
    combined_attacks = pd.concat(attack_samples, ignore_index=True)
    sampled_attacks = combined_attacks.sample(n=1000, random_state=42)  # Adjust n if needed
    sampled_attacks.to_csv("attack_samples.csv", index=False)
    print("✅ Saved 1000 attack samples to 'attack_samples.csv'")
else:
    print("❌ No valid files found or no attack samples.")

