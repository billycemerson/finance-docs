import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
import re

def scrape_cnbc(query="BBCA", start_date="2015-01-01", end_date="2025-09-30", max_per_month=2):
    """
    Scrape article titles from CNBC Indonesia search results.
    Ambil maksimal 'max_per_month' artikel per bulan dari hasil pencarian.
    """
    base_url = "https://www.cnbcindonesia.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    results = []

    # Looping month by month
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current = start
    while current <= end:
        year = current.year
        month = current.month

        # Calculate month start and end dates
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        month_end = datetime(next_year, next_month, 1) - pd.Timedelta(days=1)

        # Define date range for the query
        fromdate = current.strftime("%Y/%m/%d")
        todate = month_end.strftime("%Y/%m/%d")

        url = f"{base_url}?query={query}&fromdate={fromdate}&todate={todate}&kanal=&tipe=artikel"

        print(f"Scraping {year}-{month:02d}: {url}")

        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error on {year}-{month:02d}: {e}")
            current = month_end + pd.Timedelta(days=1)
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        # All articles are within div with class "flex flex-col gap-6"
        container = soup.select_one("div.flex.flex-col.gap-6")
        if not container:
            print(f"No articles found for {year}-{month:02d}")
            current = month_end + pd.Timedelta(days=1)
            continue

        articles = container.find_all("article")
        count = 0

        for art in articles:
            a_tag = art.find("a", href=True)
            if not a_tag:
                continue

            title_tag = a_tag.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else None
            if not title:
                continue

            link = a_tag["href"]
            results.append({
                "Year": year,
                "Month": month,
                "Title": title,
                "URL": link
            })
            count += 1

            if count >= max_per_month:
                break  # stop if reached max articles for the month

        print(f"{year}-{month:02d}: {count} articles scraped.")

        # Add delay to avoid rate limiting
        time.sleep(1)

        # Go to next month
        current = month_end + pd.Timedelta(days=1)

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = scrape_cnbc(query="BBCA", start_date="2015-01-01", end_date="2025-09-30", max_per_month=5)

    if not df.empty:
        os.makedirs("../results", exist_ok=True)
        df.to_csv("../results/cnbc_bbca.csv", index=False, encoding="utf-8-sig")
        print(f"Saved {len(df)} rows")
    else:
        print("No data scraped.")