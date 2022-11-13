#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
    ./refresh.py quarkus
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from glob import glob

import frontmatter

from eole.core import UpdateMethod
from eole.github import GitHubApiException, GitHubRepository

log = logging.getLogger(__name__)


def refresh_product(path) -> None:
    identifier = os.path.splitext(os.path.basename(path))[0]
    log.info("Refreshing data for %s", identifier)

    with open(path, "r") as f:
        metadata = frontmatter.load(f)
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
    specs = metadata["update"]["versions"]
    method = UpdateMethod.safe_parse(specs["method"])
    logging.debug("Method for refreshing %s data is %s", identifier, method)

    releases = {}
    if method == UpdateMethod.GITHUB:
        releases = GitHubRepository(specs).releases()

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


set_up_logging(logging.INFO)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        refresh_product(f"products/{sys.argv[1]}.md")
    else:
        for product_file in glob("products/*.md"):
            refresh_product(product_file)
