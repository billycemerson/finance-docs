import camelot
import pandas as pd

# Get all tables from the PDF
tables = camelot.read_pdf("Agustus-2025.pdf", pages="1-end", flavor="stream") # pyright: ignore[reportPrivateImportUsage]
print("Total tables extracted:", tables.n)

# Concat all tables into a single DataFrame
df_all = pd.concat([t.df for t in tables], ignore_index=True)

# Save to CSV
df_all.to_csv("Agustus-2025_all.csv", index=False, encoding="utf-8-sig")

print("All table saved")