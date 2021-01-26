import requests
from selectorlib import Extractor
import datetime

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('booking.yml')


today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(1)


def create_url(people, city, offset, datein=today, dateout=tomorrow):

    url_list = []

    for i in range(1, offset, 25):

        url = "https://www.booking.com/searchresults.en-gb.html?checkin_month={in_month}" \
            "&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}" \
            "&checkout_monthday={out_day}&checkout_year={out_year}&group_adults={people}" \
            "&group_children=0&order=price&ss={city}&offset={offset}"\
            .format(in_month=str(datein.month),
                    in_day=str(datein.day),
                    in_year=str(datein.year),
                    out_month=str(dateout.month),
                    out_day=str(dateout.day),
                    out_year=str(dateout.year),
                    people=people,
                    city=city,
                    offset=i)

        url_list.append(url)
    return url_list


def scrape(url):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Pass the HTML of the page and create
    return e.extract(r.text,base_url=url)

