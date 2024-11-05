import logging

from google.cloud import bigquery
from google.api_core.exceptions import ClientError


def upsert_stock_data(config, stock_data):
    """
    Upsert stock data into BigQuery.

    :param config: The configuration object.
    :param stock_data: The stock data to upsert.
    """
    client = bigquery.Client()

    # Initialize clients with credentials
    project = config["project"]["name"]
    dataset = config["bigquery"]["dataset_id"]
    table = config["bigquery"]["table_id"]

    table_id = f"{project}.{dataset}.{table}"

    merge_query = f"""
    MERGE `{table_id}` AS T
    USING (
      SELECT
        @isin AS isin,
        @name AS name,
        @label AS label,
        @pe_ratio AS pe_ratio,
        @div_yield AS div_yield,
        @scraped_at AS scraped_at
    ) AS S
    ON T.isin = S.isin
    WHEN MATCHED THEN
      UPDATE SET
        name = S.name,
        label = S.label,
        pe_ratio = S.pe_ratio,
        div_yield = S.div_yield,
        scraped_at = S.scraped_at
    WHEN NOT MATCHED THEN
      INSERT (isin, name, label, pe_ratio, div_yield, scraped_at)
      VALUES (S.isin, S.name, S.label, S.pe_ratio, S.div_yield, S.scraped_at)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("isin", "STRING", stock_data["isin"]),
            bigquery.ScalarQueryParameter("name", "STRING", stock_data["name"]),
            bigquery.ScalarQueryParameter("label", "STRING", stock_data["label"]),
            bigquery.ScalarQueryParameter(
                "pe_ratio", "NUMERIC", stock_data["pe_ratio"]
            ),
            bigquery.ScalarQueryParameter(
                "div_yield", "NUMERIC", stock_data["div_yield"]
            ),
            bigquery.ScalarQueryParameter(
                "scraped_at", "TIMESTAMP", stock_data["scraped_at"]
            ),
        ]
    )

    try:
        query_job = client.query(merge_query, job_config=job_config)
        query_job.result()  # Waits for the job to complete.
        logging.info("Upserted data for ISIN: %s", stock_data["isin"])
    except ClientError as e:
        logging.error("An error occurred: %s", e)
