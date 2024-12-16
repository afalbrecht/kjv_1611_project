import requests
import re
import os
import logging
import time
import random
from bs4 import BeautifulSoup

def clean_verse_text(text):
    """Clean and normalize verse text."""
    # Remove leading verse numbers
    text = re.sub(r'^\d+\s*', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove website metadata and navigation text
    text = re.sub(r'(Home|Interlinear|Parallel|Analysis|Library|Bible|Next Chapter|Copyright|Terms of Use|Privacy Policy).*', '', text, flags=re.IGNORECASE)
    
    return text

def is_valid_verse(text):
    """Check if the text looks like a genuine Bible verse."""

    # Check if line is longer than 8 characters ("Jesus wept" is shortest verse)
    if len(text) < 8:
        return False
    
    if (text.startswith(":1")):
        return False
    
    # Exclude lines that look like website text
    exclude_patterns = [
        r'^(Home|Interlinear|Parallel|Analysis|Library|Bible|Next Chapter|Copyright|Terms of Use|Privacy Policy)',
        r'^\d+\s*(Home|Interlinear|Parallel|Analysis|Library|Bible)',
        r'^(v\d+|©|\(c\))',
        r'^(Textus Receptus|King James Bible)',
        r'^(Cookies|Accept|Reject)'
    ]
    
    for pattern in exclude_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False
    
    return True

def fetch_kjv_1611_verses():
    """Scrape KJV 1611 verses from textusreceptusbibles.com"""
    # Base URL for the Bible site
    base_url = "https://textusreceptusbibles.com/KJV1611/{}/{}"
    
    # Books of the Bible with their chapter counts
    books = {
        "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, 
        "Deuteronomy": 34, "Joshua": 24, "Judges": 21, "Ruth": 4, 
        "1 Samuel": 31, "2 Samuel": 24, "1 Kings": 22, "2 Kings": 25,
        "1 Chronicles": 29, "2 Chronicles": 36, "Ezra": 10, "Nehemiah": 13, 
        "Esther": 10, "Job": 42, "Psalms": 150, "Proverbs": 31, 
        "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66, 
        "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12,
        "Hosea": 14, "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4, 
        "Micah": 7, "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3, 
        "Haggai": 2, "Zechariah": 14, "Malachi": 4, "Matthew": 28, 
        "Mark": 16, "Luke": 24, "John": 21, "Acts": 28, "Romans": 16,
        "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6, 
        "Ephesians": 6, "Philippians": 4, "Colossians": 4, 
        "1 Thessalonians": 5, "2 Thessalonians": 3, "1 Timothy": 6, 
        "2 Timothy": 4, "Titus": 3, "Philemon": 1, "Hebrews": 13, 
        "James": 5, "1 Peter": 5, "2 Peter": 3, "1 John": 5, 
        "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
    }
    
    # Book name to number mapping
    book_to_number = {
        book: index + 1 for index, book in enumerate(books.keys())
    }
    
    # Output file path
    output_file = os.path.join(os.getcwd(), "kjv_1611_bible.txt")
    
    # User agents to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    
    # Open file for writing
    with open(output_file, 'w', encoding='utf-8') as f:
        # Track total verses and errors
        total_verses = 0
        error_count = 0
        
        # Iterate through books
        for book, chapters in books.items():
            logging.info(f"Processing {book}...")
            
            # Get book number
            book_number = book_to_number[book]
            
            # Iterate through chapters
            for chapter in range(1, chapters + 1):
                try:
                    # Construct URL
                    url = base_url.format(book_number, chapter)
                    
                    # Set headers to mimic browser
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Referer': 'https://textusreceptusbibles.com/',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'
                    }
                    
                    # Fetch the page with more robust request
                    response = requests.get(
                        url, 
                        headers=headers, 
                        timeout=15,
                        allow_redirects=True
                    )
                    response.raise_for_status()
                    
                    # Use BeautifulSoup for parsing
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # More precise verse extraction
                    verse_elements = soup.find_all(['p', 'span', 'div', 'td'])
                    
                    verses_found = 0
                    chapter_check = False
                    king_james = False
                    for element in verse_elements:
                        
                        # Try to extract text
                        verse_text = element.get_text(strip=True) 
                        
                        # Clean the verse
                        cleaned_verse = clean_verse_text(verse_text)
                        
                        # Validate and write verse
                        if is_valid_verse(cleaned_verse):
                            if chapter_check:
                                if "King James" in verse_text:
                                        king_james = True
                                if not king_james:
                                    f.write(f"{book} {chapter}:{verses_found + 1} {cleaned_verse}\n")
                                    total_verses += 1
                                    verses_found += 1

                            if "Chapter:" in cleaned_verse:
                                chapter_check = True
                        
                    
                    logging.info(f"  Processed {book} Chapter {chapter}: {verses_found} verses")
                    
                    # Randomized delay to avoid detection
                    time.sleep(random.uniform(0.5, 2.0))
                
                except requests.RequestException as e:
                    logging.error(f"Request error processing {book} Chapter {chapter}: {e}")
                    error_count += 1
                
                except Exception as e:
                    logging.error(f"Unexpected error processing {book} Chapter {chapter}: {e}")
                    error_count += 1
                    
                    # Stop if too many errors occur
                    if error_count > 10:
                        logging.warning("Too many errors. Stopping scraping.")
                        break
            
            # Break outer loop if too many errors
            if error_count > 10:
                break
        
        logging.info(f"Bible saved to {output_file}")
        logging.info(f"Total verses processed: {total_verses}")
        logging.info(f"Total errors: {error_count}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Run the scraper
if __name__ == "__main__":
    fetch_kjv_1611_verses()