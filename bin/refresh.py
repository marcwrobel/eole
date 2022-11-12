#!/usr/bin/env python3

import os
from glob import glob

import frontmatter
from core import UpdateMethod
from github import GitHubProject


def do_refresh(update_method, specs):
    if update_method == UpdateMethod.MANUAL:
        print("Manual update, nothing to do")
    elif update_method == UpdateMethod.GITHUB:
        project = GitHubProject(specs)
        for version in project.releases():
            print(version)


def refresh(product_file):
    product_id = os.path.splitext(os.path.basename(product_file))[0]

    with open(product_file, "r") as f:
        product_data = frontmatter.load(f)
        specs = product_data["update"]["versions"]
        method_as_str = specs["method"]

        try:
            update_method = UpdateMethod[method_as_str]
            do_refresh(update_method, specs)
        except KeyError:
            print(f"Unknown method '{method_as_str}' for {product_id}")


# Main

for file in glob("products/*.md"):
    refresh(file)
