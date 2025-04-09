import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with the service account key
cred = credentials.Certificate("config/firebase-adminsdk.json")  # Path to your Firebase service account JSON file
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Function to register a scraped website
def register_scraped_website(website_url, scraper_name):
    doc_ref = db.collection("scraped_websites").document(website_url)
    doc_ref.set({
        "url": website_url,
        "scraper": scraper_name,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"Website {website_url} has been registered.")

# Function to check if a website is already scraped
def is_website_scraped(website_url):
    doc_ref = db.collection("scraped_websites").document(website_url)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Website {website_url} already scraped by {doc.to_dict()['scraper']}.")
        return True
    else:
        print(f"Website {website_url} has not been scraped yet.")
        return False
