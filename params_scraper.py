import os
import datetime

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

tmpfilepath = "/tmp/data.csv"
