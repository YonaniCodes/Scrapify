import re
import requests
import json
import os
import requests
from bs4 import BeautifulSoup
import  fitz  # PyMuPDF
import json
from urllib.parse import urlparse

from src.preprocessing import normalize_amharic

 
 
headers = {'User-Agent': 'Mozilla/5.0'}

# --- 1. extract from web ---
def extract_from_web(url):
  
    response= requests.get(url,timeout=10,headers=headers)
    response.raise_for_status()  # Throws an error for bad responses (e.g. 404, 500)

    soup = BeautifulSoup(response.text,'html.parser')
    paragraphs = soup.find_all([
        'p', 'div', 'span', 'li', 'article', 'section', 'header', 'footer',
        'main', 'aside', 'blockquote', 'pre'
        , 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
    ])
    content= "  ".join(p.get_text() for p in paragraphs)
    return content.strip()

# --- 2. extract from scanned pdf code not complete edit here---
# def extract_from_scanned_pdf(url):
#     try:
#         response=requests.get(url, timeout=10, headers=headers)
#         images= convert_from_bytes(response.content)

#         text=""
#         for img in images:
#             text+=pytesseract.image_to_string(img,lang='amh+eng')
#         return text.strip()
#     except Exception as e:
         
#         return f"Error extracting from scanned pdf: {str(e)}"
    
# --- 2. extract from pdf ---
def extract_from_pdf(url):
    response = requests.get(url, timeout=10, headers=headers)
    response.raise_for_status()  # Throws an error for bad responses (e.g. 404, 500)
    
    filename= "data/pdf/temp.pdf"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(response.content)

    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# --- 3. check if it is pdf ---
def is_pdf(url):
    return url.lower().endswith(".pdf")

# --- 4. Use simple google search ---


def save_to_json(data, filename="data/extracted_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {filename}")
 
def amharic_only(text):
    normalized_text = normalize_amharic(text)
    cleaned_text = re.sub(r'\s+', ' ', normalized_text)
    # Extract Amharic script characters
    amhariconly = re.findall(r'[\u1200-\u137F\u1370-\u137C\u2160-\u217F0-9፡።፣፤፥፦፧፨]+', cleaned_text)
    joined = " ".join(amhariconly).strip()

    # Language detection on the extracted Amharic-looking text
   

    return joined


def save_to_jsonl(data, filename="data/extracted_data.jsonl"):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'a', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    print(f"Saved {len(data)} records to {filename}")


def is_valid_url(url):
    """Check if the URL has a valid format (scheme and netloc)."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

 
