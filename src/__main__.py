"""Command line interface of ResumeLens.

    python -m src analyze data/sample_resumes/wednesday_addams.txt --format html --out report.html
    python -m src diagrams
"""
import argparse
import sys

from src.pipeline import run_pipeline
from src.stage4_grammar import ProfileValidationError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m src", description="ResumeLens resume screening")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="screen one text resume against the four profiles")
    analyze.add_argument("resume", help="path of a plain text resume")
    analyze.add_argument("--format", choices=("html", "markdown"), default="markdown")
    analyze.add_argument("--out", help="write the visualization to this file instead of printing it")

    sub.add_parser("diagrams", help="regenerate docs/stage2-transducers.md and docs/stage3-automata.md")

    args = parser.parse_args(argv)
    if args.command == "diagrams":
        from src import diagrams
        diagrams.main()
        return 0

    with open(args.resume, encoding="utf-8") as f:
        text = f.read()
    try:
        output = run_pipeline(text, output=args.format)
    except ProfileValidationError as error:
        print(f"Invalid candidate profile: {error}", file=sys.stderr)
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote {args.out}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
