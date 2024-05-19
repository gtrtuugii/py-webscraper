from selenium import webdriver
from selenium.webdriver.common.by import By  
import csv

# Constants
MAX_ROUNDS = 22
SEMI_FINAL = "SF"
GRAND_FINAL = "GF"
# url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R1'
# CMD to run for my macbook: /usr/local/bin/python3.7 /Users/School/Desktop/Sites/playhq/playhq.py
# Need to specify python 3.7 for my macbook due to my other projects using a different versionn

# The following div contains the match fixtures
# <div data-testid="fixture-list" class="sc-10c3c88-0 hLABJT">

def get_regular_rounds_data(base_url, start, end):
    all_rounds_data = []
    # Start a browser session (consider specifying the browser driver path)
    driver = webdriver.Chrome()
    for round in range(start, end + 1):
        url = base_url.format(round)
        driver.get(url)
        # Wait for dynamic content to load 
        driver.implicitly_wait(10)  # Set to 10 seconds (adjust the waiting time as needed)

        # Extract data from element with the specified class
        element = driver.find_element(By.CLASS_NAME, "sc-10c3c88-0")
        curr_round_data = []
        if element:
            curr_round_data.append(element.text)
        else:
            print("Element not found.")
        
        all_rounds_data.append(curr_round_data)

    # Close the browser session
    driver.quit()
    return all_rounds_data

def get_special_rounds_data(base_url, round_name):

    # Start a browser session (consider specifying the browser driver path)
    driver = webdriver.Chrome()
    url = base_url.format(round_name)
    driver.get(url)
    # Wait for dynamic content to load 
    driver.implicitly_wait(10)  # Set to 10 seconds (adjust the waiting time as needed)

    # Extract data from element with the specified class
    element = driver.find_element(By.CLASS_NAME, "sc-10c3c88-0")

    if element:
        print(element.text)
        return element.text
    else:
        print("Element not found.")
    # Close the browser session
    driver.quit()

def get_all_rounds_data():
    result = get_regular_rounds_data(base_url, 1, 22)
    result2 = get_special_rounds_data(base_url, SEMI_FINAL)
    result3 = get_special_rounds_data(base_url, GRAND_FINAL)
    result.append(result2)
    result.append(result3)
    return result


def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Round', 'Date', 'Team 1', 'Score 1', 'Result', 'Score 2', 'Team 2', 'Result Details', 'Time', 'Location'])

        for round_number, round_data in enumerate(data, start=1):
            csv_writer.writerow([f"Round {round_number}"] + round_data)
    print("WRITTEN TO CSV")
        
base_url = 'https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}'
data = get_regular_rounds_data(base_url, 1, 10)
print(data)
output_file = 'data.csv'
write_to_csv(data, output_file)


