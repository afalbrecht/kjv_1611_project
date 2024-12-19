# KJV 1611 Bible Text Processing

Made a little scraper and some processing scripts for the KJV 1611 Bible, all to throw some gematria at it.
You can use the import function on cyphers.news with the txt files, as I've set them up in the right format, and added the necessary header [CREATE_GEMATRO_DB] at the top of each file, except for the kjv_bible.txt file.
If you want to make different slices of the text you can use the processing script, or you can contact me and I'll try to make it.
I made this quickly using Claude, and also discovered an interesting tidbit, namely that Claude is able to verbatim reproduce the complete KJV 1611 Bible text if you ask it to, which means it is stored somewhere in toto, in a highly compressed form. But if it can recite this verbatim, maybe it can recite any text it has read, which would make it probably the most compressed database we've ever been able to make. The whole of human knowledge is hiding somewhere in its neurons.

## File Descriptions

### Input Files

* `kjv_1611_bible.txt`: Original Bible text with line numbers and verse references
* `kjv_1611_bible_cleaned.txt`: Processed text without line numbers or verse references
* `kjv_1611_bible_book_headings.txt`: List of book names repeated for each chapter

### Output Files

* `kjv_1611_unique_words.txt`: Alphabetically sorted unique words from the Bible text
* `kjv_1611_word_frequencies.txt`: Words with their frequencies, sorted alphabetically
* `kjv_1611_word_frequencies_by_count.txt`: Words sorted by frequency in descending order

### Processing Details

* Converts all text to lowercase
* Removes punctuation
* Includes book names from headings in word frequency analysis
* Generates three different word list formats for analysis

## Usage

```python
process_bible_text('kjv_1611_bible_cleaned.txt', 'kjv_1611_bible_book_headings.txt')
```

## Note

Designed for numerological analysis of the King James Version (1611) Bible.
