from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
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
    
    # Make Selenium less detectable
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Configure proxy (optional, set it only if needed)
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = "your_http_proxy_here"  # Replace with your HTTP proxy
    proxy.ssl_proxy = "your_ssl_proxy_here"    # Replace with your SSL proxy
    
    # Set proxy to capabilities
    capabilities = options.to_capabilities()
    proxy.add_to_capabilities(capabilities)  # Corrected method
    
    # Return the WebDriver instance
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options,
        desired_capabilities=capabilities
    )

# Simulate human behavior with random delays and scrolling
def simulate_user_behavior(driver):
    time.sleep(random.uniform(2, 8))  # Random delay
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 5))  # Another delay after scrolling

# Function to save extracted content to a file
def save_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Read URLs from a file
with open("urls.txt", "r") as f:
    urls = f.readlines()

# Define base path for saving files
base_path = r"C:\Users\Haris Jan\Desktop\New folderrr"
os.makedirs(base_path, exist_ok=True)

# Batch size for restarting the WebDriver
batch_size = 50

# Initialize WebDriver
driver = start_driver()

# Loop through each URL
for i, url in enumerate(urls, start=1):
    # Restart WebDriver every batch_size requests to avoid detection
    if i % batch_size == 0:
        driver.quit()
        driver = start_driver()

    try:
        driver.get(url.strip())  # Open URL
        simulate_user_behavior(driver)  # Simulate user actions

        # Extract page source and parse with BeautifulSoup
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Define output file name and path
        file_name = f"{i}.txt"
        file_path = os.path.join(base_path, file_name)

        # Extract information
        is_remote = bool(soup.find('div', text=lambda x: x and 'remote' in x.lower()))
        has_expire = 'expired on Indeed' in soup.get_text().lower()
        has_clearance = 'clearance' in soup.get_text().lower()
        apply_button = soup.find('button', {
            'aria-haspopup': 'dialog',
            'type': 'button',
            'buttontype': 'primary',
            'contenthtml': 'Apply now'
        })

        # Build the content to save
        content = ""
        if has_expire:
            content += "expired\n"
        if has_clearance:
            content += "Clearance\n"
        if is_remote:
            content += "Remote\n"
        if apply_button:
            content += "5544\n"

        # Append meta tags
        content += "Meta tags:\n"
        for meta in soup.find_all('meta'):
            content += str(meta) + "\n"

        # Save content to the file
        save_content(file_path, content)

    except Exception as e:
        print(f"Error processing URL {url.strip()}: {e}")

# Quit WebDriver at the end
driver.quit()
