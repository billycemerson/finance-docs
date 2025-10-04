import pandas as pd

# Get data
fin_data = pd.read_csv("../results/All_Financials.csv")
tec_data = pd.read_csv("../results/monthly_close.csv")

# Select column
fin_data = fin_data[['Year', 'Month', 'TOTAL ASET', 'TOTAL LIABILITAS', 'TOTAL EKUITAS']]
tec_data = tec_data[['Year', 'Month', 'Close']]

# Rename columns for financial data
fin_data.columns = ['Year', 'Month', 'Total_Assets', 'Total_Liabilities', 'Total_Equity']

# Handling values: Remove dots and convert to numeric, coercing errors to NaN
for col in ['Total_Assets', 'Total_Liabilities', 'Total_Equity']:
    fin_data[col] = pd.to_numeric(fin_data[col].astype(str).str.replace('.', '', regex=False).str.strip(), errors='coerce')

# Handling Month in fin_data: Ensure it's numeric
month_map = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
}
fin_data['Month'] = fin_data['Month'].map(month_map)

# Set Year and Month to int for merging
fin_data['Year'] = fin_data['Year'].astype(int)
fin_data['Month'] = fin_data['Month'].astype(int)
tec_data['Year'] = tec_data['Year'].astype(int)
tec_data['Month'] = tec_data['Month'].astype(int)

# Convert 'Close' to numeric, coercing errors to NaN
tec_data['Close'] = pd.to_numeric(tec_data['Close'], errors='coerce')

# Merge datasets on Year and Month
merged_data = pd.merge(fin_data, tec_data, on=['Year', 'Month'], how='inner')

# Save to CSV
merged_data.to_csv("../results/merged_fin_tec.csv", index=False, encoding="utf-8-sig")
print("Merged data saved")