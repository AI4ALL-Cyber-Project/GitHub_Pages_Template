import pandas as pd
import numpy as np

print("Running test script")
print("Script started")

def clean_csv(file_name):
    print(f"Cleaning {file_name}...")

    try:
        df = pd.read_csv(file_name)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Drop unneeded columns (keep 'Label' or 'Attempted Category' for categories)
    columns_to_drop = [
        'Src IP dec', 'Dst IP dec', 'Timestamp',
        'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg',
        'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg',
        # Drop Attempted Category only if you don't want it
        # 'Attempted Category'
    ]
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop columns with >50% missing data
    df.dropna(thresh=len(df)*0.5, axis=1, inplace=True)

    # Fill remaining NaNs with median
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Map labels to categories
    # Keep 'BENIGN' as 'Benign', others keep original attack names for multi-class classification
    df['Label'] = df['Label'].apply(lambda x: 'Benign' if x == 'BENIGN' else x)

    # check unique attack categories present
    print("Unique Labels after mapping:", df['Label'].unique())

    # Save cleaned data
    output_file = file_name.replace('.csv', '_cleaned.csv')
    try:
        df.to_csv(output_file, index=False)
        print(f"Data cleaned and saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving file: {e}")

clean_csv('thursday_plus.csv')


#Steffina's code - wednesday
#load the files
df_wed = pd.read_csv("wednesday_plus.csv")

#replace missing cells with NA
df_wed.replace([float('inf'), float('-inf')], pd.NA, inplace=True)

#Drop rows with any missing values
df_wed.dropna(inplace=True)

#remove unnecessary colums
columns_to_drop = [
    'Src IP dec', 'Dst IP dec', 'Src Port', 'Dst Port', 'Timestamp',
    'Fwd PSH Flags', 'Bwd PSH Flags',
    'Fwd URG Flags', 'Bwd URG Flags',
    'Fwd RST Flags', 'Bwd RST Flags',
    'FWD Init Win Bytes', 'Bwd Init Win Bytes',
    'Fwd Act Data Pkts', 'Fwd Seg Size Min',
    'ICMP Code', 'ICMP Type'
]

#drop the cols if they exist
df_wed.drop(columns=[col for col in columns_to_drop if col in df_wed.columns], inplace=True)

   # Map labels to categories
    # Keep 'BENIGN' as 'Benign', others keep original attack names for multi-class classification
    df_wed['Label'] = df_wed['Label'].apply(lambda x: 'Benign' if x == 'BENIGN' else x)

    # check unique attack categories present
    print("Unique Labels after mapping:", df_wed['Label'].unique())

    # Save cleaned data
    output_file_wed = file_name.replace('.csv', '_cleaned_wed.csv')
    try:
        df_wed.to_csv(output_file_wed, index=False)
        print(f"Data cleaned and saved to '{output_file_wed}'")
    except Exception as e:
        print(f"Error saving file: {e}")

clean_csv_wed('wednesday_plus.csv')

