import os
import json
import logging

from .cloud_storage_utils import download_csv_data_as_string_from_gcs
from .cloud_storage_utils import read_stock_symbols_from_string
from .scraper import scrape_stock_data


def load_config():
    """
    Load configuration from config/config.json.
    """
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.json")
    with open(config_path, mode="r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config


def main():
    """
    Main function that orchestrates the data scraping and insertion process.
    """
    # Configure the logging
    logging.basicConfig(
        level=logging.INFO,  # Set to DEBUG for more verbose output
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()  # You can add FileHandler here to log to a file
        ],
    )

    # Load the configuration
    config = load_config()
    if not config:
        logging.error("Failed to load configuration")
        return

    logging.info("Configuration loaded: %s", config)

    # download the CSV file content as a string
    csv_data = download_csv_data_as_string_from_gcs(config)
    if not csv_data:
        logging.error("Failed to download CSV data from GCS")
        return

    # Read the stock symbols from the CSV file content
    stock_symbols = read_stock_symbols_from_string(csv_data)
    if not stock_symbols:
        logging.error("Failed to read stock symbols from CSV data")
        return

    logging.info("Stock symbols loaded: %d", len(stock_symbols))

    # Scrape the stock data for each symbol
    for symbol in stock_symbols:
        stock_data = scrape_stock_data(symbol)
        if stock_data:
            logging.info("Stock Data for %s: %s", symbol, stock_data)
        else:
            logging.warning("Failed to retrieve data for %s", symbol)


if __name__ == "__main__":
    main()
