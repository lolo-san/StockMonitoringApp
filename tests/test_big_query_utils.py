import pytest
from unittest.mock import ANY, patch, MagicMock
from google.api_core.exceptions import GoogleAPIError
from app.big_query_utils import upsert_stock_data


@pytest.fixture
def sample_config():
    return {
        "project": {"name": "test-project"},
        "bigquery": {"dataset_id": "test_dataset", "table_id": "test_table"},
    }


@pytest.fixture
def sample_stock_data():
    return {
        "isin": "TEST12345678",
        "name": "Test Company",
        "label": "TEST",
        "pe_ratio": 15.75,
        "div_yield": 2.5,
        "scraped_at": "2023-11-05T15:21:04.884757+00:00",
    }


@patch("app.big_query_utils.bigquery.Client")
def test_upsert_stock_data_success(
    mock_bigquery_client, sample_config, sample_stock_data
):

    # Mock the BigQuery client and its methods
    mock_query_job = MagicMock()
    mock_query_job.result.return_value = None
    mock_bigquery_client.return_value.query.return_value = mock_query_job

    # Call the function
    upsert_stock_data(sample_config, sample_stock_data)

    # Assertions
    mock_bigquery_client.assert_called_once()
    mock_bigquery_client.return_value.query.assert_called_once()
    mock_query_job.result.assert_called_once()


@patch("app.big_query_utils.bigquery.Client")
@patch("app.big_query_utils.logging")
def test_upsert_stock_data_client_error(
    mock_logging, mock_bigquery_client, sample_config, sample_stock_data
):

    # Mock the BigQuery client and its methods
    mock_client_instance = mock_bigquery_client.return_value
    mock_client_instance.query.side_effect = GoogleAPIError("Mocked GoogleAPIError")

    # Call the function
    upsert_stock_data(sample_config, sample_stock_data)

    # Assertions
    mock_bigquery_client.assert_called_once()
    mock_client_instance.query.assert_called_once()
    mock_logging.error.assert_called_once_with("An error occurred: %s", ANY)

    # Further assertions on the exception
    args, kwargs = mock_logging.error.call_args
    exception_arg = args[1]
    assert isinstance(exception_arg, GoogleAPIError)
    assert str(exception_arg) == "Mocked GoogleAPIError"
