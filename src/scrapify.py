from database import (
    register_scraped_website,
    register_unscraped_website,
    get_all_scraped_websites,
    get_all_unscraped_websites,
    is_registered
)
headers = {'User-Agent': 'Mozilla/5.0'}
from functions import (
    amharic_only,
    extract_from_pdf,
    extract_from_web,
    is_pdf,
    save_to_jsonl
)

def scrape(urls, scraper="unknown"):
    for url in urls:
        print(f"Processing: {url}")
        
        if is_registered(url):
            print("⚠️ URL is already registered, skipping.")
            continue

        try:
            if is_pdf(url):
                content = extract_from_pdf(url)
            else:
                content = extract_from_web(url)
        except Exception as e:
            print(f"❌ Error at extraction: {str(e)}")
            register_unscraped_website(url,str(e))
            continue  # Don't stop the whole process for one bad URL
        # print(content)
        amharic_content = amharic_only(content)
        if amharic_content!="":
            # print(amharic_content)
            record = {
                "url": url,
                "scraper": scraper,
                "content": amharic_content[:2000]  # Truncate long texts
            }

            save_to_jsonl([record])  # Save as a list of one dict (for JSONL)
            register_scraped_website(url, scraper)
        else:
            print("no data")


scrape(["https://ndcoilknkl"])
class ScrapeManager:
    def __init__(self):
        self.scraped = get_all_scraped_websites()
        self.unscraped = get_all_unscraped_websites()
    def get_scraped(self):
        """Returns the list of scraped websites."""
        return self.scraped

    def get_unscraped(self):
        """Returns the list of unscraped websites."""
        return self.unscraped

scrape(["https://fetena.net/books_asset/books_27/collection/grade%2010-amharic_fetena_net_1096.pdf"])