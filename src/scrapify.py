from database import register_scraped_website, register_unscraped_website, get_all_scraped_websites, get_all_unscraped_websites


def scrape():
    # Register the website as both scraped and unscraped
    register_scraped_website("https://yonasawoke", 'Yonas Awoke')
    register_unscraped_website("https://yonasawoke")

    # Get all scraped and unscraped websites
    scraped_websites = get_all_scraped_websites()
    unscraped_websites = get_all_unscraped_websites()

    # Print all scraped websites
    print("Scraped Websites:")
    for website in scraped_websites:
        print(website)

    # Print all unscraped websites
    print("Unscraped Websites:")
    for website in unscraped_websites:
        print(website)

    print("Scraping..........")

scrape()
