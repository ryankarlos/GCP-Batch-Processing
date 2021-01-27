import os
import datetime
from google.cloud import bigquery


max_search = int(os.environ["MAX_SEARCH"])
people = int(os.environ["PEOPLE"])

with open("counties.txt", "r") as text_file:
    # lst = [i.rstrip('n') for i in text_file.readlines()]
    counties = text_file.read().splitlines()

checkin_date = datetime.datetime.now() + datetime.timedelta(int(os.environ["CHECKIN"]))
checkout_date = checkin_date + datetime.timedelta(int(os.environ["CHECKOUT"]))
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

bucketname = os.environ["BUCKET"]
filename = os.environ("FILENAME")
tmpfilepath = "/tmp/data.csv"
table_id = "lbghack2021team7.stage.booking_hotels"
schema = (
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
