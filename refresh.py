#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
    ./refresh.py quarkus
"""

import os
import sys
from glob import glob

import frontmatter

from eole.core import UpdateMethod
from eole.github import GitHubRepository


def do_refresh(update_method, specs) -> None:
    if update_method == UpdateMethod.GITHUB:
        project = GitHubRepository(specs)
        for version in project.releases():
            print(version)


def refresh(product_file) -> None:
    product_id = os.path.splitext(os.path.basename(product_file))[0]
    print(f"Refreshing data for {product_id}")

    with open(product_file, "r") as f:
        product_data = frontmatter.load(f)
        specs = product_data["update"]["versions"]
        method_as_str = specs["method"]

        try:
            update_method = UpdateMethod[method_as_str]
            do_refresh(update_method, specs)
        except KeyError:
            print(f"Unknown method '{method_as_str}' for {product_id}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        refresh(f"products/{sys.argv[1]}.md")
    else:
        for file in glob("products/*.md"):
            refresh(file)
