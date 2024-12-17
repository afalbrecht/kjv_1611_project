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

# Specify input and output files
input_file = 'kjv_1611_bible.txt'
output_file = 'kjv_1611_bible_cleaned.txt'

# Run the conversion
clean_bible_text(input_file, output_file)

print(f"Conversion complete. Output saved to {output_file}")