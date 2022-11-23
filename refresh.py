#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
    ./refresh.py quarkus
    ./refresh.py -h
"""
import json
import logging
import os
from glob import glob

from eole.core import Metadata, UpdateMethod
from eole.github import GitHubApiException, GitHubRepository
from eole.infrastucture import parse_args, set_up_logging

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


args = parse_args()
set_up_logging(logging.DEBUG if args.verbose else logging.INFO)
if __name__ == "__main__":
    if len(args.products) > 0:
        for product in args.products:
            refresh_product(f"products/{product}.md")
    else:
        for product_file in glob("products/*.md"):
            refresh_product(product_file)
