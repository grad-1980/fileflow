from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .io import FileReader
from .pipeline import Pipeline
from .errors import FileFlowError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fileflow",
        description="Process a file through a configurable pipeline of processors.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Run pipeline on an input file",
    )
    run_parser.add_argument(
        "input",
        help="Path to input file",
    )
    run_parser.add_argument(
        "--out",
        dest="output",
        default=None,
        help="Path to output file (if omitted, prints to stdout)",
    )
    run_parser.add_argument(
        "--strip",
        action="store_true",
        help="Strip whitespace on each line",
    )
    run_parser.add_argument(
        "--lower",
        action="store_true",
        help="Convert the content to lowercase",
    )
    run_parser.add_argument(
        "--replace",
        nargs=2,
        metavar=("OLD", "NEW"),
        default=None,
        help="Replace substring OLD with NEW",
    )
    run_parser.add_argument(
        "--drop-empty",
        action="store_true",
        help="Drop empty lines",
    )
    run_parser.add_argument(
        "--grep",
        metavar="SUBSTR",
        default=None,
        help="Keep only lines that contain SUBSTR",
    )
    run_parser.add_argument(
        "--head",
        metavar="N",
        type=int,
        default=None,
        help="Keep only the first N lines",
    )
    run_parser.add_argument(
        "--tail",
        metavar="N",
        type=int,
        default=None,
        help="Keep only the last N lines",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            with FileReader(args.input) as file:
                pipeline = Pipeline()
                if args.strip:
                    from .processors import StripProcessor
                    pipeline.add(StripProcessor())

                if args.lower:
                    from .processors import LowercaseProcessor
                    pipeline.add(LowercaseProcessor())

                if args.replace is not None:
                    old, new = args.replace
                    from .processors import ReplaceProcessor
                    pipeline.add(ReplaceProcessor(old, new))

                if args.drop_empty:
                    from .processors import DropEmptyProcessor
                    pipeline.add(DropEmptyProcessor())

                if args.grep is not None:
                    from .processors import GrepProcessor
                    pipeline.add(GrepProcessor(args.grep))

                if args.head is not None:
                    if args.head <= 0:
                        parser.error("--head N: N must be a positive integer")
                    from .processors import HeadProcessor
                    pipeline.add(HeadProcessor(args.head))

                if args.tail is not None:
                    if args.tail <= 0:
                        parser.error("--tail N: N must be a positive integer")
                    from .processors import TailProcessor
                    pipeline.add(TailProcessor(args.tail))


                result, report = pipeline.run_with_report(file)

                print(
                    f"Steps: {', '.join(report.steps) if report.steps else '-'} | "
                    f"Chars: {report.chars_before} -> {report.chars_after}",
                    file=sys.stderr,
                )

            if args.output:
                out_path = Path(args.output)
                out_path.write_text(result.content, encoding="utf-8")
            else:
                # stdout
                sys.stdout.write(result.content)
                if result.content and not result.content.endswith("\n"):
                    sys.stdout.write("\n")

            return 0

        # На всякий случай (хотя required=True уже гарантирует команду)
        parser.error("Unknown command")

    except FileFlowError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"Error: file not found: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
