import os
import re

def extract_emails_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        return emails

def extract_emails_from_folder(folder_path):
    extracted_emails = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            emails = extract_emails_from_file(file_path)
            extracted_emails.extend(emails)
    return extracted_emails

def save_emails_to_file(emails, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for email in emails:
            output_file.write(email + '\n')

if __name__ == "__main__":
    folder_path = r'C:\Users\Almas\Desktop\download'
    output_file_path = r'C:\Users\Almas\Desktop\extracted_emails.txt'

    extracted_emails = extract_emails_from_folder(folder_path)
    save_emails_to_file(extracted_emails, output_file_path)

    print(f"Email addresses extracted and saved to {output_file_path}")
