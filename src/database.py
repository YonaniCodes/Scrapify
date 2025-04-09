import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with the service account key
cred = credentials.Certificate("config/firebase-adminsdk.json")  # Path to your Firebase service account JSON file
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def register_scraped_website(website_url, scraper_name):
    if is_registered(website_url):
        print(f"❌ This website has already been scraped: {website_url}")
        return False
    else:
        # Add new entry
        db.collection("scraped_websites").add({
            "url": website_url,
            "scraper": scraper_name,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Successfully registered: {website_url}")
        return True
    
def register_unscraped_website(website_url):
    if is_registered(website_url):
        print(f"❌ This website has already been registered: {website_url}")
    else:
        # Add new entry
        db.collection("unscraped_websites").add({
            "url": website_url,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Successfully registered: {website_url}")
        return True

def is_registered(website_url):
    scraped_docs = db.collection("scraped_websites").where("url", "==", website_url).get()
    unscraped_docs = db.collection("unscraped_websites").where("url", "==", website_url).get()
    
    if scraped_docs or unscraped_docs:
        return True
    else:
        return False

# Function to get all scraped websites
def get_all_scraped_websites():
    scraped_websites = db.collection("scraped_websites").stream()
    websites = []
    
    for doc in scraped_websites:
        website_data = doc.to_dict()
        # Safely get the 'timestamp' field
        timestamp = website_data.get("timestamp", "No timestamp available")
        
        websites.append({
            "url": website_data.get("url"),
            "scraper": website_data.get("scraper"),
            "timestamp": timestamp
        })
    
    return websites


# Function to get all unscraped websites
def get_all_unscraped_websites():
    unscraped_websites = db.collection("unscraped_websites").stream()
    websites = [{"url": doc.to_dict()["url"], "timestamp": doc.to_dict()["timestamp"]} for doc in unscraped_websites]
    return websites
