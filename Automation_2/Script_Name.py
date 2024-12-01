import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Directory to save the extracted data
OUTPUT_DIR = "extracted_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chrome profile name
PROFILE_NAME = "M.Naqqash"

# Function to initialize the driver and connect to the existing Chrome session
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to existing Chrome instance
    service = Service(ChromeDriverManager().install())  # Automatically manage ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to extract data from the page source
def extract_data_from_tab(driver, file_index):
    try:
        # Get the current page source
        page_source = driver.page_source.splitlines()

        # Check for specific keywords
        contains_5544 = any("5544" in line for line in page_source)
        contains_remote = any("Remote" in line for line in page_source)
        contains_clearance = any("Clearance" in line for line in page_source)
        contains_expired = any("expired" in line.lower() for line in page_source)

        # Extract the company name from meta tags
        company_name = ""
        for line in page_source:
            if '<meta content="' in line and ('property="og:description"' in line or 'name="twitter:description"' in line):
                start_index = line.find('content="') + len('content="')
                end_index = line.find('"', start_index)
                company_name = line[start_index:end_index]
                break

        # Construct the output text
        output_text = company_name.strip()
        if contains_clearance:
            output_text = f"Clearance {output_text}"
        if contains_5544:
            output_text = f"5544 {output_text}"
        if contains_remote:
            output_text = f"Remote {output_text}"
        if contains_expired:
            output_text = f"expired {output_text}"

        # Save the result to a file
        output_file_path = os.path.join(OUTPUT_DIR, f"output_{file_index}.txt")
        with open(output_file_path, "w") as output_file:
            output_file.write(output_text)
        print(f"Data saved to {output_file_path}")

    except Exception as e:
        print(f"Error processing tab: {e}")

# Main function to iterate through all opened tabs
def process_open_tabs():
    try:
        # Initialize the web driver
        driver = initialize_driver()

        # Get all open tabs
        open_tabs = driver.window_handles
        print(f"Number of tabs found: {len(open_tabs)}")

        # Process each tab
        for index, tab in enumerate(open_tabs, start=1):
            driver.switch_to.window(tab)
            print(f"Processing tab {index}/{len(open_tabs)}: {driver.current_url}")
            extract_data_from_tab(driver, index)

        # Close the driver after processing
        driver.quit()

    except Exception as e:
        print(f"Error in process_open_tabs: {e}")

# Entry point of the script
if __name__ == "__main__":
    print("Starting extraction from open Chrome tabs...")
    process_open_tabs()
