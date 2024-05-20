from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
import csv


# PYTHON WEB SCRAPER

# CONSTANTS



# CMD to run for my macbook: /usr/local/bin/python3.7 /Users/School/Desktop/Sites/playhq/playhq.py
# Need to specify python 3.7 for my macbook due to my other projects using a different versionn

class PythonWebScraper:
    def __init__(self, driver_path='chromedriver', implicit_wait_time=10):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.driver.implicitly_wait(implicit_wait_time)


    # EXTRACT DATA FROM A SINGE PAGE
    def get_data_from_page(url, class_name):
        # List to store the result data
        result = []
        # Start a browser session (may need to specify the browser driver path)
        driver = webdriver.Chrome()
        driver.get(url)
        # Wait for dynamic content to load 
        driver.implicitly_wait(10)  # Set to 10 seconds (adjust the waiting time as needed)

        # Extract data from element with the specified class
        element = driver.find_element(By.CLASS_NAME, class_name)
        if element:
            result.append(element.text)
        else:
            print("Element not found")

        # Close the browser session
        driver.quit()
        return result

    # EXTRACT DATA FROM A RANGE OF PAGES
    def get_data_from_pages(base_url, class_name, start, end):
        # Some web pages can be traversed based on their url
        # They often share the same div class names, but can be different

        # TODO: Store div names in a dict with their corresponding page number
        # Example:
        # url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R1'
        # url = 'https://au.eyebuydirect.com/eyeglasses#page=2/pagesize=30'

        # TODO: Need to identify where pagination is in the url example: #page=2 and /R1
        # Modified Example:
        # url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}'
        # url = 'https://au.eyebuydirect.com/eyeglasses#page={}/pagesize=30'

        all_rounds_data = []
        # Start a browser session (mayn need to specify the browser driver path)
        driver = webdriver.Chrome()
        for round in range(start, end + 1):
            url = base_url.format(round)
            driver.get(url)
            # Wait for dynamic content to load 
            driver.implicitly_wait(10)  # Set to 10 seconds (adjust the waiting time as needed)

            # Extract data from element with the specified class
            # element = driver.find_element(By.CLASS_NAME, "sc-10c3c88-0")
            element = driver.find_element(By.CLASS_NAME, class_name)

            curr_round_data = []
            if element:
                curr_round_data.append(element.text)
            else:
                print("Element not found.")
            
            all_rounds_data.append(curr_round_data)

        # Close the browser session
        driver.quit()
        return all_rounds_data

    # WRITE EXTRACTED DATA INTO A .csv FILE
    @staticmethod
    def write_to_csv(data, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Round', 'Date', 'Team 1', 'Score 1', 'Result', 'Score 2', 'Team 2', 'Result Details', 'Time', 'Location'])

            for round_number, round_data in enumerate(data, start=1):
                csv_writer.writerow([f"Round {round_number}"] + round_data)
        print("WRITTEN TO CSV")

# Example: PlayHQ
# PlayHQ url modified
# base_url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}'

# Round 1 url
# base_url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R1'
# div="sc-10c3c88-0"

# The following div contains the match fixtures
# <div data-testid="fixture-list" class="sc-10c3c88-0 hLABJT">
# class_name = "sc-10c3c88-0"
# data = get_regular_rounds_data(base_url,"sc-10c3c88-0", 1, 10)
# print(data)
# output_file = 'data.csv'
# write_to_csv(data, output_file)

# Example: Eyebuydirect
# TODO: Quits if there is a ad/Modal blocking the content

# base_url = 'https://au.eyebuydirect.com/eyeglasses#page=2/pagesize=30'
# div = 'list-content'

# modified url
# url = 'https://au.eyebuydirect.com/eyeglasses#page={}/pagesize=30'




# Usage Example:
if __name__ == "__main__":
    # TODO: FILL
    scraper = PythonWebScraper()
    base_url = 'https://example.com/page/{}'
    data = scraper.get_data_from_page(base_url, div)

    output_file = 'data.csv'
    PythonWebScraper.write_to_csv(data, output_file)


# Example: PlayHQ
# PlayHQ url modified
# base_url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}'

# PlayHQ Round 1 url
# base_url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R1'
# div="sc-10c3c88-0"

# The following div contains the match fixtures
# <div data-testid="fixture-list" class="sc-10c3c88-0 hLABJT">
# class_name = "sc-10c3c88-0"
# data = get_regular_rounds_data(base_url,"sc-10c3c88-0", 1, 10)
# print(data)
# output_file = 'data.csv'
# write_to_csv(data, output_file)

# Example: Eyebuydirect
# TODO: Quits if there is a ad/Modal blocking the content

# base_url = 'https://au.eyebuydirect.com/eyeglasses#page=2/pagesize=30'
# div = 'list-content'

# modified url
# url = 'https://au.eyebuydirect.com/eyeglasses#page={}/pagesize=30'

# if __name__ == "__main__":
#     # TODO: FILL WITH ACTUAL DATA/EXAMPLE
#     scraper = PythonWebScraper()
#     base_url = 'https://example.com/page/{}'
#     div = 'list-content'
#     data = scraper.get_data_from_page(base_url, div)

#     output_file = 'data.csv'
#     PythonWebScraper.write_to_csv(data, output_file)
