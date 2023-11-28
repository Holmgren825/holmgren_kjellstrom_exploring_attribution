#!/usr/bin/env python

import argparse
import re

import pandas as pd
import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert excel and file of stationsföljning to yml.",
    )
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)

    return parser.parse_args()


def construct_dict(df: pd.DataFrame) -> dict:
    merges_dict = {}
    count = 0
    n_stations = 0
    for row in df.iterrows():
        if re.search(r"(?<!\S)\d(?!\S)", str(row[1][2])):
            n_stations = row[1][2]
            station_name = row[1][1]
            count = 0
            station_dict = {}
            station_dict["id"] = row[1][0]
            station_dict["periods"] = {}
            station_dict["to_merge"] = []
        elif count <= n_stations:
            # Make life easier and keep the stations in a separate list as well.
            station_dict["to_merge"].append(row[1][0])
            period_start = str(row[1][2])
            period_end = str(row[1][3])
            sub_station_dict = {"to": period_end, "id": str(row[1][0])}
            # We use the period start as key as opposed to the station id since the id
            # is not necessarily unique.
            station_dict["periods"][period_start] = sub_station_dict
            count += 1

        merges_dict[station_name] = station_dict

    return merges_dict


def main() -> None:
    args = parse_args()
    df = pd.read_excel(
        args.input,
        header=None,
    )

    merges_dict = construct_dict(df)

    output = args.output
    with open(output, "w") as file:
        yaml.dump(merges_dict, stream=file, allow_unicode=True)


if __name__ == "__main__":
    main()
