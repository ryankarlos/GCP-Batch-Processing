from google.cloud import bigquery
import os

project_id = os.environ["PROJECT_ID"]
schema = os.environ["SCHEMA"]
table = os.environ["TABLE"]

bucketname = os.environ["BUCKET"]
filename = os.environ["FILENAME"]
table_schema = (
    [
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
)
