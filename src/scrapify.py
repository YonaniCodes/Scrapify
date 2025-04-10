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
        try:
            amharic_content = amharic_only(content)
            if amharic_content:  # No need to compare with "" explicitly, just check if it's truthy
                # print(amharic_content)  # Uncomment if you want to inspect the content
                record = {
                    "url": url,
                    "scraper": scraper,
                    "content": amharic_content[:2000]  # Truncate long texts
                }

                save_to_jsonl([record])  # Save as a list of one dict (for JSONL)
                register_scraped_website(url, scraper)

        except Exception as e:
            register_unscraped_website(url, str(e))

       
       


def get_report():
    scraped_websites = get_all_scraped_websites()
    unscraped_websites = get_all_unscraped_websites()
    return scraped_websites,unscraped_websites

