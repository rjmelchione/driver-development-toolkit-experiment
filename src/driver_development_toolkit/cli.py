"""Command-line entry point for coaching report generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from driver_development_toolkit.analysis import AnalysisConfig, analyze_session
from driver_development_toolkit.ingestion import reader_for_path
from driver_development_toolkit.reporting import render_markdown_report
from driver_development_toolkit.synthetic import demo_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an iRacing coaching report.")
    parser.add_argument("telemetry_path", nargs="?", help="Path to a normalized JSON fixture or future .ibt file.")
    parser.add_argument("--demo", action="store_true", help="Generate a report from built-in synthetic telemetry.")
    parser.add_argument("--output", "-o", help="Optional report output path. Prints to stdout when omitted.")
    parser.add_argument(
        "--max-opportunities",
        type=int,
        help="Limit the number of ranked opportunities in the report.",
    )
    parser.add_argument(
        "--no-consistency",
        action="store_true",
        help="Exclude lap-to-lap consistency opportunities.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.demo:
        session = demo_session()
    elif args.telemetry_path:
        path = Path(args.telemetry_path)
        reader = reader_for_path(path)
        session = reader.read(path)
    else:
        parser.error("provide a telemetry path or use --demo")

    config = AnalysisConfig(
        include_consistency=not args.no_consistency,
        max_opportunities=args.max_opportunities,
    )
    opportunities = analyze_session(session, config=config)
    report = render_markdown_report(session, opportunities)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
