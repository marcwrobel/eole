#!/usr/bin/env python3
"""Main script, used to refresh Eole data.

Typical usage example::

    ./refresh.py -d /path/to/endoflife.date
    ./refresh.py -d /path/to/endoflife.date quarkus
    ./refresh.py -h
"""
import logging
import os
from glob import glob

import frontmatter

from eole.endoflife import FrontMatter, UpdateMethod
from eole.infrastucture import parse_args, set_up_logging

log = logging.getLogger(__name__)


def do_refresh_product(identifier, metadata):
    method = metadata.update_method()

    if method == UpdateMethod.unspecified:
        log.info("skipping %s : update method not specified", identifier)
    elif method == UpdateMethod.manual:
        log.info("skipping %s : update method set to manual", identifier)
    elif method == UpdateMethod.unsupported:
        log.warning(
            "skipping %s : update method '%s' is not supported",
            identifier,
            method,
        )


def refresh_product(path) -> None:
    identifier = os.path.splitext(os.path.basename(path))[0]
    log.info("Refreshing data for %s", identifier)

    try:
        with open(path, "r") as f:
            metadata = FrontMatter(frontmatter.load(f))
            do_refresh_product(identifier, metadata)
    except Exception as e:
        log.error("Could not refresh %s: %s", identifier, e)


args = parse_args()
set_up_logging(logging.DEBUG if args.verbose else logging.INFO)

if __name__ == "__main__":
    if len(args.products) > 0:
        for product in args.products:
            refresh_product(f"{args.dir}/products/{product}.md")
    else:
        for product_file in sorted(glob(f"{args.dir}/products/*.md")):
            refresh_product(product_file)
