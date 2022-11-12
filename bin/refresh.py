#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py
"""

import os
from glob import glob

import frontmatter
from core import UpdateMethod
from github import GitHubRepository


def save(product_id, json) -> None:
    with open(f"data/{product_id}.json", "w") as f:
        f.write(json)


def do_refresh(product_id, update_method, specs) -> None:
    if update_method == UpdateMethod.MANUAL:
        print(f"{product_id} is set to {update_method} method, nothing to do")
    elif update_method == UpdateMethod.GITHUB:
        print(f"Updating {product_id} with {update_method} method.")
        project = GitHubRepository(specs)
        save(product_id, project.json())


def refresh(product_file) -> None:
    product_id = os.path.splitext(os.path.basename(product_file))[0]

    with open(product_file, "r") as f:
        product_data = frontmatter.load(f)
        specs = product_data["update"]["versions"]
        method_as_str = specs["method"]

        try:
            update_method = UpdateMethod[method_as_str]
            do_refresh(product_id, update_method, specs)
        except KeyError:
            print(f"Unknown method '{method_as_str}' for {product_id}")


for file in glob("products/*.md"):
    refresh(file)
