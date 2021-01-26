
import csv
from scraper import scrape, create_url


offset=100
people = 1
city = ['London', 'bristol', 'cornwall', 'brighton', 'portsmouth', 'bournemouth', 'manchester', 'yorkshire', 'gloucestershire']

with open('data.csv','w') as outfile:
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
        urllist.extend(create_url(people, c, offset))

    writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for url in urllist:
        data = scrape(url)
        if data:
            try:
                for h in data['hotels']:
                    writer.writerow(h)
            except:
                print("Skipping to next as offset exceeds max search")
            # sleep(5)
