#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
    ./refresh.py quarkus
"""
import json
import os
import sys
from glob import glob

import frontmatter

from eole.core import UpdateMethod
from eole.github import GitHubRepository


def refresh_product(path) -> None:
    identifier = os.path.splitext(os.path.basename(path))[0]
    print(f"Refreshing data for {identifier}")

    with open(path, "r") as f:
        metadata = frontmatter.load(f)
        do_refresh_product(metadata)


def do_refresh_product(metadata) -> None:
    specs = metadata["update"]["versions"]
    method = UpdateMethod.safe_parse(specs["method"])

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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        refresh_product(f"products/{sys.argv[1]}.md")
    else:
        for product_file in glob("products/*.md"):
            refresh_product(product_file)
