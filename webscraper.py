from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
import csv

# PYTHON WEB SCRAPER

# CMD to run for my macbook: /usr/local/bin/python3.7 /Users/School/Desktop/Sites/playhq/playhq.py
# Need to specify python 3.7 for my macbook due to my other projects using a different version

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import json
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PythonWebScraper:
    def __init__(self, config_path='config.json'):
        self.load_config(config_path)
        self.setup_driver()
        
    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.driver_path = self.config.get('driver_path', 'chromedriver')
        self.implicit_wait_time = self.config.get('implicit_wait_time', 10)
        self.base_url = self.config.get('base_url')
        self.pagination_pattern = self.config.get('pagination_pattern', '{}')
        self.output_file = self.config.get('output_file', 'output.csv')

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        if self.config.get('headless', True):
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
        self.driver.implicitly_wait(self.implicit_wait_time)

    def get_data_from_page(self, url, identifier, by='class'):
        result = []
        self.driver.get(url)
        try:
            if by == 'class':
                elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, identifier))
                )
            elif by == 'id':
                elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.ID, identifier))
                )
            else:
                raise ValueError("Invalid 'by' argument. Use 'class' or 'id'.")
            result = [element.text for element in elements]
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error retrieving elements: {e}")
        
        return result

    def get_data_from_pages(self, start, end, identifier, by='class'):
        all_rounds_data = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.get_data_from_page, self.base_url.format(self.pagination_pattern.format(round)), identifier, by) for round in range(start, end + 1)]
            for future in futures:
                try:
                    all_rounds_data.append(future.result())
                except Exception as e:
                    logging.error(f"Error retrieving data from page: {e}")
        return all_rounds_data

    def close(self):
        self.driver.quit()

    def write_to_csv(self, data):
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Round', 'Data'])
            for round_number, round_data in enumerate(data, start=1):
                csv_writer.writerow([f"Round {round_number}"] + round_data)
        logging.info("Data written to CSV")

# Sample config.json
'''
{
    "driver_path": "path/to/chromedriver",
    "implicit_wait_time": 10,
    "base_url": "https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}",
    "pagination_pattern": "{}",
    "output_file": "output.csv",
    "headless": true
}
'''



# Usage
scraper = PythonWebScraper(config_path='config.json')
data = scraper.get_data_from_pages(1, 5, 'sc-10c3c88-0', by='class')
scraper.write_to_csv(data)
scraper.close()

