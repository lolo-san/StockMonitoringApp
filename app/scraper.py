import logging
import requests
from bs4 import BeautifulSoup


def convert_string_to_float(value):
    """
    Convert scraped value to a float.

    :param value: The extracted text value.
    :return: A cleaned float value.
    """
    try:
        # Remove unwanted characters and replace comma with period
        cleaned_value = value.replace(",", ".").replace("%", "").strip()
        return float(cleaned_value)
    except (ValueError, AttributeError) as e:
        # Return None or a default value if conversion fails
        logging.error("Conversion failed for value '%s': %s", value, e)
        return None


def get_stock_page(stock_symbol):
    """
    Fetches the stock page from Boursorama for a given stock symbol.

    :param stock_symbol: The stock symbol to scrape data for.
    :return: The response object containing the HTML content.
    """

    # Configure logging for this function
    logger = logging.getLogger(__name__)

    url = f"https://www.boursorama.com/cours/{stock_symbol}"
    logger.info("Fetching data for %s from %s", stock_symbol, url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred for %s: %s", stock_symbol, http_err)
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error("Request exception occurred for %s: %s", stock_symbol, req_err)
        return None

    return response


def scrape_stock_data(stock_symbol):
    """
    Scrapes stock data from Boursorama for a given stock symbol.

    :param stock_symbol: The stock symbol to scrape data for.
    :return: A dictionary containing the scraped data.
    """
    # Configure logging for this function
    logger = logging.getLogger(__name__)

    # # request the stock's page from the website
    response = get_stock_page(stock_symbol)

    # analyze the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    stock_data = {}

    try:
        # Retrieve the company's name and ISIN code
        stock_data["name"] = soup.find(
            "a", class_="c-faceplate__company-link"
        ).text.strip()
        stock_data["isin"] = soup.find("h2", class_="c-faceplate__isin").text.strip()

        # Find the 'c-faceplate__data' div
        data_div = soup.find("div", class_="c-faceplate__data")

        # Find all 'p' elements in order
        p_elements = data_div.find_all("p", recursive=True)

        data_points = {}
        heading = None

        # Build a dictionary of data points from the 'p' elements
        for p in p_elements:
            classes = p.get("class", [])
            text = p.get_text(strip=True)
            if "c-list-info__heading" in classes:
                heading = text.lower()
                data_points[heading] = None  # Initialize with None
            elif "c-list-info__value" in classes and heading:
                data_points[heading] = text
                heading = None  # Reset heading after pairing
            else:
                continue  # Skip unrelated <p> elements

        # Extract the specific data points
        for key, val in data_points.items():
            if "rendement" in key:
                stock_data["div_yield"] = convert_string_to_float(val)
            elif "per" in key:
                stock_data["pe_ratio"] = convert_string_to_float(val)

        if stock_data["div_yield"] is None:
            stock_data["div_yield"] = 0.0
            logger.warning("Dividend yield not found for %s", stock_symbol)

        if stock_data["pe_ratio"] is None:
            stock_data["pe_ratio"] = 0.0
            logger.warning("PE ratio not found for %s", stock_symbol)

        if stock_data["div_yield"] == 0.0 or stock_data["pe_ratio"] == 0.0:
            logger.info("Partially scraped data for %s", stock_symbol)
        else:
            logger.info("Successfully scraped data for %s", stock_symbol)

    except AttributeError as e:
        logger.error("Data extraction error for %s: %s", stock_symbol, e)
        return None

    return stock_data
