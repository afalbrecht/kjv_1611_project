import re
from collections import Counter

def process_bible_text(bible_file, headings_file=None):
    # Read the entire Bible text
    with open(bible_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Split into words
    words = text.split()
    
    # If headings file is provided, add its words
    if headings_file:
        with open(headings_file, 'r', encoding='utf-8') as f:
            # Simply read lines and convert to lowercase
            heading_words = [line.strip().lower() for line in f]
            words.extend(heading_words)
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Sort words alphabetically
    sorted_words = sorted(word_counts.keys())
    
    # Write unique words in alphabetical order
    with open('kjv_1611_unique_words.txt', 'w', encoding='utf-8') as f_unique:
        for word in sorted_words:
            f_unique.write(f"{word}\n")
    
    # Write words with their frequencies (alphabetical)
    with open('kjv_1611_word_frequencies.txt', 'w', encoding='utf-8') as f_freq:
        for word in sorted_words:
            f_freq.write(f"{word} {word_counts[word]}\n")
    
    # Write words sorted by frequency (descending)
    with open('kjv_1611_word_frequencies_by_count.txt', 'w', encoding='utf-8') as f_freq_count:
        # Sort words by their frequency in descending order
        sorted_words_by_freq = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        for word, count in sorted_words_by_freq:
            f_freq_count.write(f"{word} {count}\n")
    
    print("Dictionary files created successfully!")


def clean_bible_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    current_book = None
    
    for line in lines:
        # Remove leading/trailing whitespace
        parts = line.strip().split(" ")
        if parts[0].isdigit():
            text = ' '.join(parts[3:])
        else:
            text = ' '.join(parts[2:])
        
        cleaned_lines.append(text)
    
    # Write cleaned lines to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    print(f"Conversion complete. Output saved to {output_file}")


def only_chapter_headings(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    current_book = None
    
    for line in lines:
        # Remove leading/trailing whitespace
        parts = line.strip().split(" ")
        if parts[0].isdigit():
            text = ' '.join(parts[:3])
        else:
            text = ' '.join(parts[:2])
        
        cleaned_lines.append(text)
    
    # Write cleaned lines to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))


# Specify input and output files
input = 'kjv_1611_bible.txt'
output = 'kjv_1611_bible_cleaned.txt'
output_chapters = 'kjv_1611_bible_chapters.txt'

# Run the cleaning
# clean_bible_text(input, output)

# Clean the bible text to only include book headings
# only_chapter_headings(input, output_chapters)

# Process the KJV 1611 Bible text file to create dictionary files
process_bible_text('kjv_1611_bible_cleaned.txt', 'kjv_1611_bible_book_headings.txt')
