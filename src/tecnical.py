import yfinance as yf
import pandas as pd

# Get data
data = yf.download("BBCA.JK", 
                         start="2015-01-01", 
                         end="2025-08-31", 
                         interval="1mo",
                         auto_adjust=False)

# Reset index to make 'Date' a column
close_data = data[['Close']].reset_index() # pyright: ignore[reportOptionalSubscript]

# Add Year and Month columns
close_data['Year'] = close_data['Date'].dt.year
close_data['Month'] = close_data['Date'].dt.month

# Reorder columns
close_data = close_data[['Year', 'Month', 'Close']]

# Rename columns to match desired header
close_data.columns = ['Year', 'Month', 'Close']

# Save to CSV
close_data.to_csv("../results/monthly_close.csv", index=False, header=True)
print(close_data.head())