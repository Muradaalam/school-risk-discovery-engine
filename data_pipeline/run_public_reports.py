#this code is AI generated

import argparse
import json
from pathlib import Path

from data_pipeline.acquisition.public_news import collect
from data_pipeline.prioritization.report_queue import build_report_queue


def run(curated_csv, raw_dir, urls_file=None, seed=True, feeds=False, limit=50):
    raw = Path(raw_dir)
    raw.mkdir(parents=True, exist_ok=True)
    scraped = raw / "scraped_public_reports.jsonl"

    scraping = collect(scraped, include_seed=seed, urls_file=urls_file, skip_feeds=not feeds)
    ranking = build_report_queue(
        curated_csv, scraped, raw / "scraped_report_review.csv",
        raw / "report_school_priorities.csv", raw / "report_top50.csv", limit=limit
    )
    return {"scraping": scraping, "recommendations": ranking}


def main():
    parser = argparse.ArgumentParser(description="Scrape public reports and rank inspection candidates")
    parser.add_argument("--curated", default="data_pipeline/examples/reports_pilot.csv")
    parser.add_argument("--raw-dir", default="data_pipeline/raw")
    parser.add_argument("--urls-file", help="New Akashvani/PIB URLs, one per line")
    parser.add_argument("--no-seed", action="store_true")
    parser.add_argument("--enable-feeds", action="store_true", help="Try unverified RSS endpoints")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    print(json.dumps(run(args.curated, args.raw_dir, args.urls_file,
                         not args.no_seed, args.enable_feeds, args.limit), indent=2))


if __name__ == "__main__":
    main()
