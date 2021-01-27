def scrape_to_bucket(request):
    """
    Cloud Function for running bookings scraper and uploading to gcp bucket
    Parameters
    ----------
    request

    """

    import csv
    from scraper import scrape, create_url
    from params import (
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
    from params import filename, bucketname, schema, table_id

    # Construct a BigQuery client object.
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://{bucketname}/{filename}"

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()
    destination_table = client.get_table(table_id)

    return "Loaded {} rows.".format(destination_table.num_rows)
