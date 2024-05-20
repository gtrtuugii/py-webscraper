# Python Web Scraper

This project is a Python-based web scraper designed to scrape data from web pages using Selenium WebDriver. The scraper can handle pagination and retrieve elements based on class names or IDs. It also supports configuration through a JSON file for flexible usage.

## Features

- Scrapes data from web pages based on class names or IDs
- Handles paginated web pages
- Configurable through a JSON file
- Supports headless mode for background execution
- Parallel processing for faster data retrieval
- Logs errors and progress

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver compatible with your version of Chrome
- Required Python packages (see below)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/gtrtuugii/python-web-scraper.git
    cd python-web-scraper
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Download ChromeDriver and place it in your PATH or specify its path in the `config.json` file.

## Configuration

The scraper uses a configuration file `config.json` to set various parameters. An example configuration is provided below:

```json
{
    "driver_path": "path/to/chromedriver",
    "implicit_wait_time": 10,
    "base_url": "https://www.playhq.com/basketball-victoria/org/melbourne-central-basketball-association/sunday-cyms-senior-domestic-summer-202324/sunday-senior-men-a/a112a9d0/R{}",
    "pagination_pattern": "{}",
    "output_file": "output.csv",
    "headless": true
}
```

## Run the scraper
```bash
python webscraper.py
```

