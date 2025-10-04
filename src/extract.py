import camelot
import pandas as pd
import os
import re

data_folder = "../data/"

target_rows = [
    "TOTAL ASET",
    "TOTAL LIABILITAS",
    "TOTAL EKUITAS",
    "LABA (RUGI) OPERASIONAL",
    "LABA (RUGI) NON OPERASIONAL",
    "LABA (RUGI) BERSIH PERIODE BERJALAN"
]

final_data = []

for file in os.listdir(data_folder):
    if file.endswith(".pdf"):
        file_path = os.path.join(data_folder, file)
        print(f"Processing {file} ...")

        # Example filename: 20280229-laporan-keuangan-publikasi-bulanan-januari-2024-ID.pdf
        base_name = os.path.splitext(file)[0].lower()

        # Regex to capture "bulan" + year
        match = re.search(r"(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)[-_ ]?(\d{4})", base_name)
        
        if match:
            month = match.group(1).capitalize()
            year = match.group(2)
        else:
            print(f"Could not parse Month/Year from {file}")
            continue

        # Read all tables
        tables = camelot.read_pdf(file_path, pages="1-end", flavor="stream") # pyright: ignore[reportPrivateImportUsage]
        df_all = pd.concat([t.df for t in tables], ignore_index=True)

        # Select only column 1 & 2
        df_2 = df_all.iloc[:, 1:3]

        # Filter target rows
        df_filtered = df_2[df_2.iloc[:, 0].isin(target_rows)]
        df_filtered = df_filtered.drop_duplicates(subset=[df_filtered.columns[0]], keep="first")

        # Map to dictionary
        values = {row[0]: row[1] for row in df_filtered.values.tolist()}

        # Append result
        final_data.append({
            "Year": year,
            "Month": month,
            **{k: values.get(k, "") for k in target_rows}
        })

# Make final DataFrame
final_df = pd.DataFrame(final_data)

# Save to results directory
os.makedirs("../results", exist_ok=True)
final_df.to_csv("../results/All_Financials.csv", index=False, encoding="utf-8-sig")

print("All financial data saved")
print(final_df.head())