def bucket_csv_to_bquery(event, context):
    """
    Cloud function which loads data into big query from cloud storage bucket.
    Triggered by updated csv landing in bucket

    Parameters
    ----------
    event
    context

    Returns
    -------

    """

    from gcloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "lbghack2021team7.stage.booking_hotels"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("location", "STRING"),
            bigquery.SchemaField("price", "INTEGER"),
            bigquery.SchemaField("price_for", "STRING"),
            bigquery.SchemaField("room_type", "INTEGER"),
            bigquery.SchemaField("beds", "STRING"),
            bigquery.SchemaField("rating", "FLOAT"),
            bigquery.SchemaField("rating_title", "STRING"),
            bigquery.SchemaField("number_of_ratings", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = "gs://cloud-function-output-scrapper/booking.csv"

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()
    destination_table = client.get_table(table_id)

    return "Loaded {} rows.".format(destination_table.num_rows)
