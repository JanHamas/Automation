import os

# Specify the directory containing the files
directory_path = r"C:\Users\Haris Jan\Desktop\New folderrr"

# Get a list of all text files in the directory
files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

# Ensure files are sorted for consistent processing
files.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else x)

# Loop through each file
for i, file_name in enumerate(files, start=1):
    file_path = os.path.join(directory_path, file_name)
    
    print(f"Processing file: {file_name}")  # Log file being processed
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Log number of lines in the file
        print(f"Number of lines in {file_name}: {len(lines)}")
        
        # Check if the file contains "5544"
        contains_5544 = any("5544" in line for line in lines)
        
        # Check if the file contains the word "Remote"
        contains_remote = any("Remote" in line for line in lines)
        contains_clearance = any("Clearance" in line for line in lines)
        contains_expired = any("expired" in line for line in lines)
        
        # Find the company name in the meta tags
        company_name = ""
        for line in lines:
            if '<meta content="' in line and ('property="og:description"' in line or 'name="twitter:description"' in line):
                start_index = line.find('content="') + len('content="')
                end_index = line.find('"', start_index)
                company_name = line[start_index:end_index]
                break
        
        # Log extracted company name
        print(f"Extracted company name from {file_name}: {company_name.strip()}")
        
        # Construct the output text
        output_text = company_name.strip()
        if contains_clearance:
            output_text = f'Clearance {output_text}'
        
        if contains_5544:
            output_text = f"5544 {output_text}"
        if contains_remote:
            output_text = f'Remote {output_text}'
        if  contains_expired:
            output_text = f'expired {output_text}'

        
        # Specify the output file path
        output_file_path = os.path.join(directory_path, f"output_{i}.txt")
        
        # Save the text to a new file
        with open(output_file_path, 'w') as output_file:
            output_file.write(output_text)
        
        print(f"Processed and saved: {output_file_path}")
    
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
