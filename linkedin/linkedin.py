from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from errors_1 import *
from  errors_2 import *
from errors_3 import *
from errors_4 import *
from errors_5 import *

# List of URLs to process
urls = [
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=1",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=2",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=3",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=4",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=5",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=6",
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=Data%20Analyst&sortBy=R"
    "ank&f_TPR=r604800&position=1&pageNum=7",
]

# Configure Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver with WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
class a():
    with open('correct_links.txt','+') as correct_links:
        pass
    # Open a text file to save the results
    with open('correct_name') as correct_name:
        pass  
    
    for url in urls:
        try:
                # Open the LinkedIn job page
            driver.get(url)

                # Use WebDriverWait to wait until the element is present
            wait = WebDriverWait(driver, 10)
            company_name_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'topcard__org-name-link')))

                # Extract the company name text
            company_name = company_name_tag.text.strip()

                # Write the company name to the output file
            output_file.write(f"{company_name}\n")          
                
            if company_name=="Failed to extract company name":
                pass
            else:
                correct_links.write(f"{url}\n")
                    
            print(f"Company name '{company_name}' extracted from {url}")

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
            with open('errors_1.py', '+') as error_file:
                error_file.write('"'+ url + '"' + ","+"\n")
def second():
    urls = open("errors_1.py","r")
    with open('correct_links.txt', '+') as correct_links:
        pass
# Open a text file to save the results
with open('Correct_names.txt', '+') as output_file:
    for url in urls:
        try:
            # Open the LinkedIn job page
            driver.get(url)

            # Use WebDriverWait to wait until the element is present
            wait = WebDriverWait(driver, 10)
            company_name_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'topcard__org-name-link')))

            # Extract the company name text
            company_name = company_name_tag.text.strip()

            # Write the company name to the output file
            output_file.write(f"{company_name}\n")          
            
            if company_name=="Failed to extract company name":
                pass
            else:
                    correct_links.write(f"{url}\n")
                
            print(f"Company name '{company_name}' extracted from {url}")

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
            with open('errors_1.py', 'a') as error_file:
                
                
                 
                
                

# Close the browser
second()
driver.quit()


print("All URLs processed and company names saved to 'company_names.txt'.")
