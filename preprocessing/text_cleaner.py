import re

def clean_text(text, remove_urls=True, remove_emails=True):
    """
    Cleans and normalizes job description text.
    - Removes special characters (except essential punctuation)
    - Normalizes whitespace
    - Converts to lowercase
    - Optionally removes URLs and emails
    """
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    if remove_urls:
        # Simple URL removal
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    if remove_emails:
        # Simple email removal
        text = re.sub(r'\S*@\S*\s?', '', text)

    # Remove special characters but keep essential punctuation
    # We keep: . , ? ! ( ) -
    text = re.sub(r'[^a-zA-Z0-9\s.,?!()\-]', '', text)

    # Whitespace normalization
    text = re.sub(r'\s+', ' ', text).strip()

    return text
