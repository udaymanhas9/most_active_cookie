#!/usr/bin/env python3
"""CLI entry point for the most active cookie finder."""

import argparse
import logging
import sys
from datetime import datetime

from cookie_log import CookieLog
from counter import CookieCounter

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s [%(module)s]: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args. Returns namespace with 'file' and 'date'."""
    parser = argparse.ArgumentParser(
        description="Find the most active cookie for a specific day."
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Path to the cookie log CSV file"
    )
    parser.add_argument(
        "-d", "--date", required=True, help="Date to query in YYYY-MM-DD format (UTC)"
    )
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    """Find and print most active cookie(s) for a given date."""
    parsed = parse_args(args)

    try:
        datetime.strptime(parsed.date, "%Y-%m-%d")
    except ValueError:
        logger.error("bad date '%s' — want YYYY-MM-DD [cli:date]", parsed.date)
        sys.exit(1)

    try:
        log = CookieLog(parsed.file)
    except FileNotFoundError:
        logger.error("file not found: %s [cli:file]", parsed.file)
        sys.exit(1)

    cookies = log.get_cookies_for_date(parsed.date)
    result = CookieCounter(cookies).most_active()

    for cookie in result:
        print(cookie)


if __name__ == "__main__":
    main()
