#!/usr/bin/env python3

from glob import glob
import os

import frontmatter

for product_file in glob("products/*.md"):
    product_name = os.path.splitext(os.path.basename(product_file))[0]
    with open(product_file, "r") as f:
        data = frontmatter.load(f)
        print(data["name"])
        print(data["method"])
