from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import os

# Path to store the output
output_dir = "scraped_data"
os.makedirs(output_dir, exist_ok=True)

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless for performance
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver
service = Service("path_to_chromedriver")  # Replace with your chromedriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to process URLs
def scrape_job_details(urls):
    for index, url in enumerate(urls, start=1):
        try:
            driver.get(url)
            time.sleep(3)  # Allow time for the page to load
            
            # Example: Locate and extract job title and company name
            try:
                job_title = driver.find_element(By.CLASS_NAME, "jobsearch-JobInfoHeader-title").text
            except NoSuchElementException:
                job_title = "Job title not found"
            
            try:
                company_name = driver.find_element(By.CLASS_NAME, "jobsearch-CompanyInfoContainer").text
            except NoSuchElementException:
                company_name = "Company name not found"
            
            # Save to a file
            with open(os.path.join(output_dir, f"{index}.txt"), "w", encoding="utf-8") as file:
                file.write(f"URL: {url}\n")
                file.write(f"Job Title: {job_title}\n")
                file.write(f"Company Name: {company_name}\n")
            
            print(f"Processed: {url}")
        
        except WebDriverException as e:
            print(f"Error processing URL {url}: {str(e)}")

# List of URLs to process
with open("urls.txt", "r") as file:
    job_urls = file.readlines()

# Execute scraping
scrape_job_details(job_urls)

# Close the browser
driver.quit()
