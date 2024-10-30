import os
import re

# Path to the directory containing the text files
directory_path = r"C:\Users\Haris Jan\Desktop\New folder"
# Path to the new file where all contents will be saved
output_file_path = os.path.join(directory_path, "combined_output.txt")

# Function to read a file with fallback encoding
def read_file_with_fallback(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            return file.read()

# Function to extract numbers from the filename for sorting
def extract_number_from_filename(filename):
    # Use regex to find the first sequence of digits in the filename
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Function to sort filenames numerically based on extracted numbers
def numeric_sort(file_list):
    return sorted(file_list, key=extract_number_from_filename)

# Open the output file once and write to it in chunks
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Get all .txt files and sort them numerically
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    sorted_files = numeric_sort(txt_files)
    
    # Iterate through each sorted file in the directory
    for filename in sorted_files:
        file_path = os.path.join(directory_path, filename)
        print(f"Processing: {filename}")  # Debugging output
        # Read and write the file content
        content = read_file_with_fallback(file_path)
        output_file.write(content)
        output_file.write("\n")  # Add extra newlines between files

print(f"All text has been combined into {output_file_path}")
