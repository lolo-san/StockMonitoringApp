# import json
# import os
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
        cleaned_value = value.replace(',', '.').replace('%', '').strip()
        return float(cleaned_value)
    except (ValueError, AttributeError):
        # Return None or a default value if conversion fails
        return None

def scrape_stock_data(stock_symbol):
    """
    Scrapes stock data from Boursorama for a given stock symbol.

    :param stock_symbol: The stock symbol to scrape data for.
    :return: A dictionary containing the scraped data.
    """
    # request the stock's page from the website
    url = f"https://www.boursorama.com/cours/{stock_symbol}"
    response = requests.get(url)

    # check for a succesful request
    if response.status_code != 200:
        # print an error message with the status code
        print(f"Failed to fetch page for {stock_symbol}. Status code: {response.status_code}")
        return None

    # analyze the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    stock_data = {}

    # retrieve the company's name and isin code
    stock_data['name'] = soup.find('a', class_='c-faceplate__company-link').text.strip()
    stock_data['isin'] = soup.find('h2', class_='c-faceplate__isin').text.strip()

    company_data = soup.find('div', class_='c-faceplate__data').contents[3].find_all('p')

    # retrieve the company's stock dividend yield and P/E ratio
    stock_data['div_yield'] = convert_string_to_float(company_data[1].text)
    stock_data['pe_ratio'] = convert_string_to_float(company_data[3].text)

    return stock_data

def main():
    """
    Main function that orchestrates the data scraping and insertion process.
    """
    # https://www.boursorama.com/cours/1rPAI/
    stock_data = scrape_stock_data('1rPAI')
    print(stock_data)

if __name__ == '__main__':
    main()
