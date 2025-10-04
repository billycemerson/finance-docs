from GoogleNews import GoogleNews
import pandas as pd
from datetime import datetime
import time, random, os, json

def scrape_bca_news_safe(query="Saham BCA", start_year=2015, end_year=2025, save_file="../results/top_news.csv"):
    googlenews = GoogleNews(lang='id', region='ID', encode='utf-8')
    results = []

    # resume support
    if os.path.exists(save_file):
        try:
            results = pd.read_csv(save_file).to_dict('records')
            print(f"Resuming from {len(results)} existing rows")
        except pd.errors.EmptyDataError:
            print(f"{save_file} is empty. Starting fresh.")
            results = []

    for year in range(start_year, end_year + 1):
        max_month = 9 if year == 2025 else 12
        for month in range(1, max_month + 1):
            # skip if already scraped
            if any(r['Year'] == year and r['Month'] == month for r in results):
                continue

            start_date = datetime(year, month, 1)
            end_date = datetime(year + (month == 12), (month % 12) + 1, 1)

            start_str = start_date.strftime("%m/%d/%Y")
            end_str = end_date.strftime("%m/%d/%Y")

            success = False
            for attempt in range(3):  # max 3 retries
                try:
                    googlenews.set_time_range(start_str, end_str)
                    googlenews.search(query)
                    page_results = googlenews.results(sort=True)[:2]

                    for article in page_results:
                        results.append({
                            "Year": year,
                            "Month": month,
                            "Title": article.get("title", "")
                        })

                    googlenews.clear()
                    success = True
                    print(f"{year}-{month:02d} ({len(page_results)} articles)")
                    break
                except Exception as e:
                    print(f"Error {year}-{month:02d}: {e}, retrying ({attempt+1}/3)...")
                    time.sleep(10 + random.random() * 10)

            # save progress every loop
            pd.DataFrame(results).to_csv(save_file, index=False)

            # random sleep (avoid rate limit)
            sleep_time = random.randint(5, 15)
            print(f"Sleeping {sleep_time}s...\n")
            time.sleep(sleep_time)

            if not success:
                print(f"Failed {year}-{month:02d} after 3 retries, skipping.")

    print(f"\n Done! Saved {len(results)} rows to {save_file}")

# Run scraper
scrape_bca_news_safe()