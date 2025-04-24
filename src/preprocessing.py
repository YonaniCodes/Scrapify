import re

# Function to normalize sentence endings
def normalize_sentence_ending(text):
    # Replace ": :" (with optional spaces) → "።"
    text = re.sub(r':\s*:', '።', text)

    # Replace "፡ ፡" (with optional spaces) → "።"
    text = re.sub(r'፡\s*፡', '።', text)

    # Replace ". ፡ ፡" (with optional spaces) → "።"
    text = re.sub(r'\.\s*፡\s*፡', '።', text)

    # Remove any period before "፡ ፡" and replace with "።"
    text = re.sub(r'\.\s*፡\s*፡', '።', text)

    # Remove duplicate full stops ("።።" → "።")
    text = re.sub(r'።{2,}', '።', text)

    # Tidy spaces around ። (keep one space before and after it)
    text = re.sub(r'\s*።\s*', ' ። ', text)

    # Replace multiple spaces with one space
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()

# Main function to normalize Amharic text
def normalize_amharic(text):
    replacements = {
        '\n': ' '
    }

    # Apply sentence-ending normalization
    text = normalize_sentence_ending(text)

    # Apply character family replacements
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text
