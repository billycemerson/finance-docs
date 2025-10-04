import pandas as pd

# Load CSV file
data = pd.read_csv("Agustus-2025_all.csv")

# Take only column 1 and 2
data_2 = data.iloc[:, 1:3]

# Define target rows we want to filter by
target_rows = [
    "TOTAL ASET",
    "TOTAL LIABILITAS",
    "TOTAL EKUITAS",
    "LABA (RUGI) OPERASIONAL",
    "LABA (RUGI) NON OPERASIONAL",
    "LABA (RUGI) BERSIH PERIODE BERJALAN"
]

# Filter rows: keep only those where column 0 matches the list
data_3 = data_2[data_2.iloc[:, 0].isin(target_rows)]

# Drop duplicates → keep only the first occurrence for each keyword
data_3 = data_3.drop_duplicates(subset=[data_3.columns[0]], keep="first")

# Rename columns to something cleaner (optional)
data_3.columns = ["Item", "Value"]

# Save the filtered DataFrame to a new CSV file (without index, no header row)
data_3.to_csv("Agustus-2025_filtered.csv", index=False, header=False, encoding="utf-8-sig")

print("Filtered rows saved")