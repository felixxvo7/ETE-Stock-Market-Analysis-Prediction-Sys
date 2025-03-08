import os
import pandas as pd
from config import RAW_DATA_PATH

# Define the raw data file path
raw_file_name = "raw_collected_1year_data.csv"
raw_file_path = os.path.join(RAW_DATA_PATH, raw_file_name)
print(f"Loading raw data from: {raw_file_path}")

# Load the raw data into a DataFrame
df = pd.read_csv(raw_file_path)

# Step 1: Filter rows starting from row 253 (index 252, zero-based)
rows_to_process = df.iloc[283:]  # Rows from index 252 onward

# Step 2: Collect values from columns after column 8 (index 8)
# Each row has exactly 5 values in this range
column_values = rows_to_process.iloc[:, 8:]  # All columns starting from column 8

# Step 3: Copy the 5 values to columns B-F (indices 1-5) for the filtered rows
for i, row_index in enumerate(rows_to_process.index):
    # Extract the 5 non-null values from the row (starting from column 8)
    values = column_values.iloc[i].dropna().values[:5]  # Take the first 5 non-null values
    if len(values) == 5:  # Ensure there are exactly 5 values
        df.loc[row_index, df.columns[1:6]] = values  # Copy to columns B-F

# Step 1: Drop the second row (index 1, zero-based)
df = df.drop(index = 0)

# Step 2: Drop columns starting from column I (index 8)
df = df.drop(df.columns[8:], axis=1)

# Step 4: Save the updated DataFrame to a new CSV file
output_file_name = "updated_collected_data.csv"
output_file_path = os.path.join(RAW_DATA_PATH, output_file_name)

# Ensure the output directory exists
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# Save the DataFrame to a CSV file
df.to_csv(output_file_path, index=False)

print(f"Updated data saved to {output_file_path}")