from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import random

# Function to initialize a new WebDriver session
def start_driver():
    options = webdriver.ChromeOptions()
    
    # Set user-agent to avoid detection
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')
    
    # Add more options like proxy, headless mode if needed
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
with open("urls.txt","r") as e:
    u=e.readlines()
job_links =u
unique_jobs = []
seen_job_ids = set()

for link in job_links:
    # if link not contain 'view' then skip
    try:        
        job_id = link.split('/view/')[1].split('/')[0]
        if job_id not in seen_job_ids:
            seen_job_ids.add(job_id)
            unique_jobs.append(link)
       
    except:
        job_id = link.split('=')[1].split('&')[0]
        if job_id not in seen_job_ids:
            seen_job_ids.add(job_id)
            unique_jobs.append(link)
with open('filter_urls.txt', 'w') as file:
    for job in unique_jobs:
        file.write(job)

with open("filter_urls.txt","r") as f:
    links=f.readlines()
# List of URLs
urls = links

# Base path where the files will be saved
base_path = r"C:\Users\Haris Jan\Desktop\New folder"

# Ensure the base path exists
os.makedirs(base_path, exist_ok=True)

# Set the batch size to restart the driver
batch_size = 50

# Initialize the first WebDriver session
driver = start_driver()

# Loop through each URL and save the output to a separate file
for i, url in enumerate(urls, start=1):
    if i % batch_size == 0:
        driver.quit()
        driver = start_driver()
    
    try:
        driver.get(url)
        
        # Random delay to simulate human behavior
        time.sleep(random.uniform(2, 5))

        # Get the page source 
        html_content = driver.page_source

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Check if the <div> tag with text 'Remote' exists
        remote_div = soup.find('div', text=lambda x: x and 'remote' in x.lower())
   
        # Check if the specific <button> element exists
        apply_button = soup.find('button', {
            'aria-haspopup': 'dialog',
            'type': 'button',
            'buttontype': 'primary',
            'contenthtml': 'Apply now'
        })

        # Check if the word "clearance" is present in the page text (case-insensitive)
        page_text = soup.get_text().lower()
        has_expire = 'expired on Indeed' in page_text
        has_clearance = 'clearance' in page_text

        # Define the file name
        file_name = f"{i}.txt"
        file_path = os.path.join(base_path, file_name)

        # Save the content to the file
        with open(file_path, 'w', encoding='utf-8') as file: 
            if has_expire:
                file.write("expired ")  
            if has_clearance:
                file.write("Clearance ")                            
            if remote_div:
                file.write("Remote ")            
            if apply_button:
                file.write("5544\n")            
            
            file.write("Meta tags:\n")
            for meta in soup.find_all('meta'):
                file.write(str(meta) + "\n")
    
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Quit the driver at the end
driver.quit()
