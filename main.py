def scrape_to_bucket(request):
    """
    Cloud Function for running bookings scraper and uploading to gcp bucket
    Parameters
    ----------
    request

    """

    import csv
    from scraper import scrape, create_url
    from params_scraper import (
        counties,
        people,
        checkin_date,
        checkout_date,
        max_search,
        fieldnames,
        filename,
        bucketname,
        tmpfilepath,
    )
    from gcloud import storage

    urllist = []
    for county in counties:
        urllist.extend(
            create_url(people, county, checkin_date, checkout_date, max_search)
        )

    # needs to be stored in tmp dir in gcp as dont have write permissions otherwise
    with open(tmpfilepath, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for url in urllist:
            data = scrape(url)
            if data:
                try:
                    for h in data["hotels"]:
                        if len(h['name'].split()) <= 6:
                            writer.writerow(h)
                except:
                    print("Skipping to next as offset exceeds max search")
                # sleep(5)
        print("Saved temp copy of csv")
        client = storage.Client()
        bucket = client.get_bucket(bucketname)
        blob = bucket.blob(filename)
        blob.upload_from_filename(tmpfilepath)
        # seems to throw error at end if return statement with some str not there.
        return "Upload to bucket completed"


def bucket_csv_to_bquery(event, context):
    """
    Cloud function which loads data into big query from cloud storage bucket.
    Triggered by updated csv landing in bucket

    Parameters
    ----------
    event
    context
    """
    from google.cloud import bigquery
    from params_bq import filename, bucketname, schema, table, project_id, table_schema

    table_id = f"{project_id}.{schema}.{table}"
    # Construct a BigQuery client object.
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        schema=table_schema,
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://{bucketname}/{filename}"

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()
    destination_table = client.get_table(table_id)

    return "Loaded {} rows.".format(destination_table.num_rows)


def senti(request):
    from google.cloud import bigquery
    from google.cloud import language_v1
    from google.cloud.bigquery import SchemaField
    import csv

    client = language_v1.LanguageServiceClient()
    bigquery_client = bigquery.Client()

    # Fetch users comments from BigQuery public dataset
    # -------------------------------------------------

    QUERY = 'SELECT * FROM `lbghack2021team7.stage.stage_twitter_tweets`'
    query_job = bigquery_client.query(QUERY)

    # Run each comment through the natural language API to get the sentiment of the comment
    # -------------------------------------------------------------------------------------

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8
    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    fieldnames = ["comment_id", "comment", "sentiment_score", "sentiment_maginitude"]
    rows_to_insert = []
    records_processed = 0

    # check if table exists and if not create one
    table_id = "lbghack2021team7.stage.stage_sentiment"

    table_schema = [
        bigquery.SchemaField("CommentID", "INTEGER"),
        bigquery.SchemaField("Tweet", "STRING"),
        bigquery.SchemaField("SentimentScore", "FLOAT"),
        bigquery.SchemaField("SentimentMagnitude", "FLOAT"),
    ]

    # If the table does not exist, delete_table raises
    # google.api_core.exceptions.NotFound unless not_found_ok is True.
    bigquery_client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print("Deleted existing table '{}'.".format(table_id))

    table = bigquery.Table(table_id, schema=table_schema)
    table = bigquery_client.create_table(table)  # Make an API request.
    print("Created empty table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

    for row in query_job:
        comment_id, comment = row[0], row[1]
        records_processed += 1
        print('Processing record %d:' % (records_processed))
        try:
            document = {"content": comment, "type_": type_, "language": language}
            response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
            row_ = {"CommentID": comment_id, "Tweet": comment, "SentimentScore": response.document_sentiment.score,
                    "SentimentMagnitude": response.document_sentiment.magnitude}
            print(row_)
            rows_to_insert.append(row_)
        except Exception as e:
            print(e)

    errors = bigquery_client.insert_rows_json(table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert))
    return "Done"
