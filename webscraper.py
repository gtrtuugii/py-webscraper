from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
import csv


# PYTHON WEB SCRAPER

# CMD to run for my macbook: /usr/local/bin/python3.7 /Users/School/Desktop/Sites/playhq/playhq.py
# Need to specify python 3.7 for my macbook due to my other projects using a different versionn

class PythonWebScraper:
    def __init__(self, driver_path='chromedriver', implicit_wait_time=10):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.driver.implicitly_wait(implicit_wait_time)
        
    def get_data_from_page(self, url, class_name):
        # List to store the result data
        result = []

        self.driver.get(url)

        try:
            elements = self.driver.find_elements(By.CLASS_NAME, class_name)
            for element in elements:
                result.append(element.text)
        except NoSuchElementException:
            print("Element not found")
        
        return result

    def get_data_from_pages(self, base_url, class_name, start, end, pagination_pattern):
        # Handling the pagination in URLs
        all_rounds_data = []

        for round in range(start, end + 1):
            formatted_url = base_url.format(pagination_pattern.format(round))
            self.driver.get(formatted_url)

            try:
                elements = self.driver.find_elements(By.CLASS_NAME, class_name)
                curr_round_data = [element.text for element in elements]
            except NoSuchElementException:
                print("Element not found.")
                curr_round_data = []
            
            all_rounds_data.append(curr_round_data)

        return all_rounds_data

    def close(self):
        # Close the browser session
        self.driver.quit()

    @staticmethod
    def write_to_csv(data, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Round', 'Date', 'Team 1', 'Score 1', 'Result', 'Score 2', 'Team 2', 'Result Details', 'Time', 'Location'])

            for round_number, round_data in enumerate(data, start=1):
                csv_writer.writerow([f"Round {round_number}"] + (round_data if round_data else ['Data not found']))
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


if __name__ == "__main__":
    # TODO: FILL
    scraper = PythonWebScraper()
    base_url = 'https://example.com/page/{}'
    div = 'list-content'
    data = scraper.get_data_from_page(base_url, div)

    output_file = 'data.csv'
    PythonWebScraper.write_to_csv(data, output_file)


