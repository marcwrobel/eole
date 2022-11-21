#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
    ./refresh.py quarkus
    ./refresh.py -h
"""
import argparse
import json
import logging
import os
from datetime import datetime, timezone
from glob import glob

from eole.core import Metadata, UpdateMethod
from eole.github import GitHubApiException, GitHubRepository

log = logging.getLogger(__name__)


def refresh_product(path) -> None:
    identifier = os.path.splitext(os.path.basename(path))[0]
    log.info("Refreshing data for %s", identifier)

    metadata = Metadata(path)
    try:
        do_refresh_product(identifier, metadata)
        log.info("Data refreshed for %s", identifier)
    except GitHubApiException as e:
        log.warning(
            "There was an unexpected error while refreshing %s : %s",
            identifier,
            e,
        )


def do_refresh_product(identifier, metadata) -> None:
    logging.debug(
        "Method for refreshing %s data is %s",
        identifier,
        metadata.update_version_method,
    )

    releases = {}
    if metadata.update_version_method == UpdateMethod.GITHUB:
        releases = GitHubRepository(metadata.update_version_specs).releases()

    print(
        json.dumps(
            list(
                map(lambda r: {"name": r.name, "date": str(r.date)}, releases)
            ),
            indent=4,
        )
    )


# https://stackoverflow.com/a/58777937/374236
def set_up_logging(level):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    logging.Formatter.formatTime = (
        lambda self, record, datefmt=None: datetime.fromtimestamp(
            record.created, timezone.utc
        ).isoformat(sep="T", timespec="milliseconds")
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Refresh products data")
    parser.add_argument(
        "products",
        metavar="product",
        type=str,
        nargs="*",
        help="an optional list of products to refresh",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show debug logs"
    )
    return parser.parse_args()


args = parse_args()
set_up_logging(logging.DEBUG if args.verbose else logging.INFO)
if __name__ == "__main__":
    if len(args.products) > 0:
        for product in args.products:
            refresh_product(f"products/{product}.md")
    else:
        for product_file in glob("products/*.md"):
            refresh_product(product_file)
