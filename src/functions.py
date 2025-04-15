import re
import requests
import json
import os
import requests
from bs4 import BeautifulSoup
import  fitz  # PyMuPDF
import json
from urllib.parse import urlparse
 

 
 
headers = {'User-Agent': 'Mozilla/5.0'}

# --- 1. extract from web ---
def extract_from_web(url):
  
    response= requests.get(url,timeout=10,headers=headers)
    response.raise_for_status()  # Throws an error for bad responses (e.g. 404, 500)

    soup = BeautifulSoup(response.text,'html.parser')
    paragraphs = soup.find_all([
        'p', 'div', 'span', 'li', 'article', 'section',  
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
 
def is_amharic(token):
    return re.search(r'[\u1200-\u137F]', token) is not None

def is_punct_or_number(token):
    return re.fullmatch(r'[0-9፡።፣፤፥፦፧፨.,:;!?\'"()\-]+', token) is not None

def amharic_only(text):
    # Tokenize text into words and symbols
    text = re.sub(r':\s*:', '።', text)
    tokens = re.findall(r'\w+|[^\w\s]', text)
 
    filtered = []
    for i, token in enumerate(tokens):
        if is_amharic(token):
            filtered.append(token)
        elif is_punct_or_number(token):
            prev = tokens[i - 1] if i > 0 else ''
            next_ = tokens[i + 1] if i < len(tokens) - 1 else ''
            if is_amharic(prev) or is_amharic(next_):
                filtered.append(token)
    
    joined = re.sub(r'\s+', ' ', text)
    joined = ' '.join(filtered).strip()

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

 
