import pytest
from unittest.mock import patch

from app.cloud_storage_utils import read_stock_symbols_from_string
from app.cloud_storage_utils import download_csv_data_as_string_from_gcs


@pytest.fixture
def sample_csv_data():
    return b"Test Company,1rPTC\n"


def test_read_stock_symbols_from_string(sample_csv_data):
    stock_symbols = read_stock_symbols_from_string(sample_csv_data)
    assert stock_symbols == ["1rPTC"]


@patch("google.cloud.storage.Client")
def test_download_csv_data_as_string_from_gcs(mock_client, sample_csv_data):
    # Mock the bucket and blob
    mock_bucket = mock_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    mock_blob.download_as_string.return_value = sample_csv_data

    config = {
        "project": {"name": "test-project"},
        "cloud_storage": {"bucket_name": "test-bucket", "csv_file": "test.csv"},
    }

    csv_data = download_csv_data_as_string_from_gcs(config)
    assert csv_data == sample_csv_data
