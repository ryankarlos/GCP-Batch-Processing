def hello_world(request):
    """
    Cloud Function for running bookings scraper and uploading to gcp bucket
    Parameters
    ----------
    request

    Returns
    -------

    """

    import csv
    from scraper import scrape, create_url
    import os
    import datetime
    from gcloud import storage

    max_search = int(os.environ["MAX_SEARCH"])
    people = int(os.environ["PEOPLE"])
    city = [
        "London",
        "bristol",
        "cornwall",
        "brighton",
        "portsmouth",
        "bournemouth",
        "manchester",
        "yorkshire",
        "gloucestershire",
    ]
    checkin_date = datetime.datetime.now() + datetime.timedelta(
        int(os.environ["CHECKIN"])
    )
    checkout_date = checkin_date + datetime.timedelta(int(os.environ["CHECKOUT"]))
    # needs to be stored in tmp dir in gcp as dont have write permissions otherwise
    with open("/tmp/data.csv", "w") as outfile:
        fieldnames = [
            "name",
            "location",
            "price",
            "price_for",
            "room_type",
            "beds",
            "rating",
            "rating_title",
            "number_of_ratings",
        ]
        urllist = []
        for c in city:
            urllist.extend(
                create_url(people, c, checkin_date, checkout_date, max_search)
            )

        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for url in urllist:
            data = scrape(url)
            if data:
                try:
                    for h in data["hotels"]:
                        writer.writerow(h)
                except:
                    print("Skipping to next as offset exceeds max search")
                # sleep(5)
        print("Saved temp copy of csv")
        client = storage.Client()
        bucket = client.get_bucket("cloud-function-output-scrapper")
        blob = bucket.blob("booking.csv")
        blob.upload_from_filename("/tmp/data.csv")
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

    Returns
    -------

    """

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "lbghack2021team7.stage.booking_hotels"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Name", "STRING"),
            bigquery.SchemaField("Location", "STRING"),
            bigquery.SchemaField("Price", "INTEGER"),
            bigquery.SchemaField("Duration", "INTEGER"),
            bigquery.SchemaField("RoomType", "STRING"),
            bigquery.SchemaField("Beds", "INTEGER"),
            bigquery.SchemaField("Rating", "FLOAT"),
            bigquery.SchemaField("RatingTitle", "STRING"),
            bigquery.SchemaField("NumberRatings", "INTEGER"),
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
