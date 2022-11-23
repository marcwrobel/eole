import argparse
import logging
from datetime import datetime, timezone


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
