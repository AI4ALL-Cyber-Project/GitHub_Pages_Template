import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def clean_csv(file_name, output_dir='cleaned'):
    print(f"Cleaning {file_name}...")

    try:
        df = pd.read_csv(file_name)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Drop unneeded columns (keep 'Label' or 'Attempted Category' for categories)
    columns_to_drop = [
        'Src IP dec', 'Dst IP dec', 'Local', 'Local_1', 'Local_2', 'Local_3', 
        'Local_4', 'Local_5', 'Local_6', 'Local_7', 'Local_8', 'Local_9', 'Local_10', 'Local_11',
        'Local_12', 'Local_13', 'Local_14', 'Attempted Category','Timestamp'
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
    df = df[~df['Label'].str.contains('Attempted', case=False, na=False)]
    
    

    # check unique attack categories present
    print("Unique Labels after mapping:", df['Label'].unique())
    encoder = LabelEncoder()
    df['Label'] = encoder.fit_transform(df['Label'])
    print(dict(zip(encoder.classes_, encoder.transform(encoder.classes_))))

    # Save cleaned data
    base_file_name = os.path.basename(file_name)
    output_filename = base_file_name.replace('.csv', '_cleaned.csv')
    output_filepath = os.path.join(output_dir, output_filename)
    try:
        df.to_csv(output_filepath, index=False)
        print(f"Data cleaned and saved to '{output_filepath}'")

    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    # Make directory for cleaned files if it doesn't exist
    output_dir = input("Enter directory to save cleaned files (default 'cleaned'): ") or 'cleaned'
    os.makedirs(output_dir, exist_ok=True)
    dataset_dir = input("Enter directory containing the CSV files (default './dataset'): ") or './dataset'

    # Loop through each file in the dataset directory
    for file_name in os.listdir(dataset_dir):
        if file_name.endswith('.csv'):
            clean_csv(os.path.join(dataset_dir, file_name), output_dir=output_dir)

#if __name__ == "__main__":
    #main()

#clean_csv('tuesday_plus.csv')
#clean_csv('friday_plus.csv')
#clean_csv('wednesday_plus.csv')
clean_csv('thursday_plus.csv')

