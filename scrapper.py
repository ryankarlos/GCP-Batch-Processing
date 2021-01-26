import json
from booking_scraper import bkscraper
import argparse

def get_results_from_booking(city, limit, detail=True):
    input_search = {'city':city, 'limit':limit, 'detail':detail}

    return bkscraper.get_result(**input_search)

def result_to_json(result, path):
    with open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
    f.close()


def argparse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        help="Used to specify the number of page to fetch.",
        default=1,
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "--city",
        help="Add the country to the booking request.",
        default="New York",
        nargs="?",
    )
    parser.add_argument(
        "--out_format",
        help="Add the format for the output file. Add excel, json or csv.",
        default="json",
        choices=["json", "excel", "csv"],
        nargs="?",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argparse_args()
    result = get_results_from_booking(args.city, args.limit)
    result_to_json(result, path="output.json")