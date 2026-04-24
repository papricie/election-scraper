import argparse
import csv
import logging
from pathlib import Path

from scraper.logic import get_municipality_links, parse_obec
from scraper.utils import validate_url

LOGGER = logging.getLogger(__name__)

BASE_FIELDS = [
    "Kód obce",
    "Název obce",
    "Voliči v seznamu",
    "Vydané obálky",
    "Platné hlasy",
]


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def build_header(rows):
    extras = []
    for row in rows:
        for key in row:
            if key not in BASE_FIELDS and key not in extras:
                extras.append(key)
    return BASE_FIELDS + sorted(extras)


def write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    configure_logging()
    parser = argparse.ArgumentParser(
        description="Scrape Czech election results and save them to CSV."
    )
    parser.add_argument("district_url", help="URL of the district page on volby.cz")
    parser.add_argument("output_file", help="CSV output filename")
    args = parser.parse_args(argv)

    if not validate_url(args.district_url):
        LOGGER.error(
            "Invalid URL. Use a volby.cz district URL starting with https://www.volby.cz/pls/ps2017nss/."
        )
        raise SystemExit(1)

    district_url = args.district_url
    output_file = Path(args.output_file)

    LOGGER.info("Loading district page...")
    municipality_links = get_municipality_links(district_url)

    if not municipality_links:
        LOGGER.error("No municipalities found on the provided page.")
        raise SystemExit(1)

    LOGGER.info("Found %d municipalities.", len(municipality_links))

    rows = []
    for index, (url, name) in enumerate(municipality_links, start=1):
        LOGGER.info("Processing %d/%d: %s", index, len(municipality_links), name)
        municipality_data = parse_obec(url, name)
        rows.append(municipality_data)

    header = build_header(rows)
    write_csv(output_file, header, rows)
    LOGGER.info("Done. Results saved to %s", output_file)
