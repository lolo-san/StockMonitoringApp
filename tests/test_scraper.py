import requests
from unittest.mock import patch
from app.scraper import scrape_stock_data
from app.scraper import get_stock_page
from app.scraper import convert_string_to_float


@patch("requests.get")
def test_scrape_stock_data_success(mock_get):
    # Updated sample HTML with actual labels
    sample_html = """
    <html>
    <head><title>Test Stock Page</title></head>
    <body>
        <a class="c-faceplate__company-link">Test Company</a>
        <h2 class="c-faceplate__isin">FR1234567890</h2>
        <div class="c-faceplate__data">
            <p class="c-list-info__heading u-color-neutral">
                rendement estimé 2024
            </p>
            <p class="c-list-info__value u-color-big-stone">
                2,50%
            </p>
            <p class="c-list-info__heading u-color-neutral">
                PER estimé 2024
            </p>
            <p class="c-list-info__value u-color-big-stone">
                15,75
            </p>
        </div>
    </body>
    </html>
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = sample_html.encode("utf-8")

    stock_data = scrape_stock_data("1rPTC")

    assert stock_data is not None
    assert stock_data["name"] == "Test Company"
    assert stock_data["isin"] == "FR1234567890"
    assert stock_data["label"] == "1rPTC"
    assert stock_data["div_yield"] == 2.5
    assert stock_data["pe_ratio"] == 15.75
    assert "scraped_at" in stock_data


@patch("requests.get")
def test_scrape_stock_data_http_error(mock_get):
    # Simulate an HTTP error
    mock_get.return_value.status_code = 404
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error"
    )

    stock_data = get_stock_page("INVALID_SYMBOL")

    assert stock_data is None


@patch("requests.get")
def test_scrape_stock_data_parsing_error(mock_get):
    # Return HTML that will cause a parsing error
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = "<html></html>".encode("utf-8")

    stock_data = scrape_stock_data("1rINVALID")

    assert stock_data is None


def test_convert_string_with_percentage_to_float_success():
    value = "3.14%"
    result = convert_string_to_float(value)
    assert result == 3.14


def test_convert_string_with_comma_instead_of_point_to_float_success():
    value = "34,56"
    result = convert_string_to_float(value)
    assert result == 34.56
