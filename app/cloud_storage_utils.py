import csv
import logging

from google.cloud import storage


def download_csv_data_as_string_from_gcs(config):
    """
    Downloads a CSV file from Google Cloud Storage.

    :param config: The configuration object.
    :return: The CSV file content as a string.
    """
    try:
        # Initialize clients with credentials
        project_name = config["project"]["name"]
        storage_client = storage.Client(project_name)

        # Download the CSV file containing stock URLs from Cloud Storage
        bucket_name = config["cloud_storage"]["bucket_name"]
        source_blob_name = config["cloud_storage"]["csv_file"]

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        return blob.download_as_string()
    except FileNotFoundError:
        logging.error("CSV file not found in GCS: %s %s", bucket_name, source_blob_name)
        return None


def read_stock_symbols_from_string(csv_data):
    """
    Read stock symbols from a CSV file content.

    :param csv_data: The CSV file content as a string.
    :return: A list of stock symbols.
    """
    stock_symbols = []
    csv_data = csv_data.decode("utf-8").split("\n")
    csvreader = csv.reader(csv_data)
    for row in csvreader:
        # Skip empty rows
        if row:
            stock_symbols.append(row[1])
    return stock_symbols
