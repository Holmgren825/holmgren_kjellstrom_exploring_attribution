#!/usr/bin/env python

import argparse
import os
from urllib.error import HTTPError
from urllib.request import urlretrieve

from tqdm.autonotebook import tqdm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch data from mora WS",
    )
    parser.add_argument("-i", "--id", required=True)
    parser.add_argument("-p", "--param", required=True)
    parser.add_argument("--st_id", required=True)
    parser.add_argument("--from_date", required=True)
    parser.add_argument("--to_date", required=True)
    parser.add_argument("-o", "--output", default=None)

    return parser.parse_args()


def get_ids_from_file(path: str) -> list:
    with open(path, "rt") as file:
        lines = file.readlines()
        ids = [line.split(",")[0] for line in lines[1:-1]]
        return ids


def build_urls(args: argparse.Namespace) -> list:
    param = args.param
    stat_id = args.st_id
    from_date = args.from_date
    to_date = args.to_date
    id = args.id

    if os.path.isfile(id):
        ids = get_ids_from_file(id)
        urls = [
            f"http://mora-apps.smhi.se/moraws/ws/value/v2/stationType/clim/stationId/{id}/parameter/{param}/statisticsFormula/{stat_id}/samplingTime/P1D/from/{from_date}/to/{to_date}?format=csv"
            for id in ids
        ]
    else:
        url = f"http://mora-apps.smhi.se/moraws/ws/value/v2/stationType/clim/stationId/{id}/parameter/{param}/statisticsFormula/{stat_id}/samplingTime/P1D/from/{from_date}/to/{to_date}?format=csv"
        urls = [url]

    return urls


def generate_filename(url: str) -> str:
    groups = url.split("/")
    groups = groups[10::2]
    groups[4] = groups[4][:10]
    groups[5] = groups[5][:10]
    filename = "_".join(groups)

    return filename + ".csv"


def download_file(url: str, output_dir: str) -> None:
    filename = generate_filename(url)
    if output_dir is not None:
        if not os.path.exists(output_dir):
            raise ValueError("Output path not a valid path")
        else:
            filename = os.path.join(output_dir, filename)
    else:
        filename = os.path.join(".", filename)
    if os.path.exists(filename):
        print("Data already available, skipping")
    else:
        try:
            urlretrieve(url, filename=filename)
        except HTTPError:
            print("404 Not found")


def fetch_data(urls: list[str], output_dir: str) -> None:
    """Simply a wrapper for download_file, taking care of looping over multiple urls."""
    for url in tqdm(urls):
        download_file(url, output_dir)


def main() -> None:
    args = parse_args()
    urls = build_urls(args)
    fetch_data(urls, args.output)


if __name__ == "__main__":
    main()
