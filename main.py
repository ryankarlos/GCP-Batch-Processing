
import csv
from scraper import scrape, create_url

people = 1
city = 'London'

with open("urls.txt",'r') as urllist, open('data.csv','w') as outfile:
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
    urllist = create_url(people, city)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for url in urllist:
        data = scrape(url)
        if data:
            for h in data['hotels']:
                writer.writerow(h)
            # sleep(5)
