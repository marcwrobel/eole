#!/usr/bin/env python3

from glob import glob
import os

import frontmatter

from github import GitHubProject
from core import UpdateMethod

for product_file in glob("products/*.md"):
    product_id = os.path.splitext(os.path.basename(product_file))[0]
    with open(product_file, "r") as f:
        data = frontmatter.load(f)
        specs = data["update"]["versions"]
        method = specs["method"]

        try:
            update_method = UpdateMethod[method]

            if update_method == UpdateMethod.MANUAL:
                print("Manual update, nothing to do")
            elif update_method == UpdateMethod.GITHUB:
                project = GitHubProject(specs)
                for version in project.releases():
                    print(version)
        except KeyError:
            print(f"Unknown method '{method}'")
