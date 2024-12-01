from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor

# Function to initialize a new WebDriver session
def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')
    options.add_argument('--headless')  # Run in headless mode for better performance
    options.add_argument('--disable-gpu')  # Disable GPU for faster processing
    options.add_argument('--no-sandbox')  # Disable sandboxing for better performance
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to process a single URL
def process_url(url, i, base_path):
    try:
        driver = start_driver()
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Adjust delay to simulate human behavior

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Check if the 'Remote' keyword exists in the <div> tag
        remote_div = soup.find('div', text=lambda x: x and 'remote' in x.lower())

        # Check for the 'Apply now' button
        apply_button = soup.find('button', {
            'aria-haspopup': 'dialog',
            'type': 'button',
            'buttontype': 'primary',
            'contenthtml': 'Apply now'
        })

        # Check for keywords in the page text
        page_text = soup.get_text().lower()
        has_expire = 'expired on Indeed' in page_text
        has_clearance = 'clearance' in page_text

        # Save results to a text file
        file_name = f"{i}.txt"
        file_path = os.path.join(base_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            if has_expire:
                file.write("expired ")
            if has_clearance:
                file.write("Clearance ")
            if remote_div:
                file.write("Remote ")
            if apply_button:
                file.write("5544\n")

            # Save meta tags
            file.write("Meta tags:\n")
            for meta in soup.find_all('meta'):
                file.write(str(meta) + "\n")

        driver.quit()  # Quit the driver after processing the URL

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
  
with open('previews_urls','r') as file:
    p_urls=file.readlines()
    p_l=len(p_urls)
    
    
# Read and process URLs from the file
with open("urls.txt", "r") as file:
    job_links = file.readlines()
    
    
job_links=p_urls+job_links
# Filter unique jobs based on the job ID (avoid duplicates)
unique_jobs = []
seen_job_ids = set()
for link in job_links:
    try:
        # Extract job ID from URL
        job_id = link.split('/view/')[1].split('/')[0] if '/view/' in link else link.split('=')[1].split('&')[0]
        if job_id not in seen_job_ids:
            seen_job_ids.add(job_id)
            unique_jobs.append(link)
    except Exception as e:
        print(f"Error processing link {link}: {e}")

# Save the filtered URLs to a new file
with open('filter_urls.txt', 'w') as file:
    for job in unique_jobs: # Skip the first p_l jobs 
        if len(job)>=p_l:
             file.write(job)
    
with open('filter_urls.txt','r') as file:
    filter_urls=file.readlines()
    
with open('previews_urls.txt','w') as file:
    for job in unique_jobs:
        time.sleep(88)
        file.write(job)
        if len(job)==len(p_l):
            break
     

# Read the URLs from the file for further processing
with open("filter_urls.txt", "r") as file:
    links = file.readlines()
    
# Set the base path to save the result files
base_path = r"C:\Users\Haris Jan\Desktop\New folder"
os.makedirs(base_path, exist_ok=True)

# Use ThreadPoolExecutor to process URLs concurrently
with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers based on your system
    for i, url in enumerate(links, start=1):
        executor.submit(process_url, url.strip(), i, base_path)

