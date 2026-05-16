#!/usr/bin/env python3
"""json_query – safely extract data from JSON via JMESPath.

Author: TopherBot <topherbot@proton.me>
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import jmespath

# ---------------------------------------------------------------------------
# Helper functions – clear naming, robust error handling
# ---------------------------------------------------------------------------

def read_input(source: str) -> str:
    """Read JSON content from *source*.

    *source* can be a path to a file or '-' to indicate STDIN.
    Returns the raw text.
    Raises SystemExit with appropriate code on failure.
    """
    if source == "-":
        try:
            return sys.stdin.read()
        except Exception as exc:
            sys.stderr.write(f"[Error] Failed to read from STDIN: {exc}\n")
            sys.exit(4)
    else:
        path = Path(source)
        if not path.is_file():
            sys.stderr.write(f"[Error] Input file '{source}' does not exist.\n")
            sys.exit(1)
        try:
            return path.read_text(encoding="utf-8")
        except Exception as exc:
            sys.stderr.write(f"[Error] Could not read '{source}': {exc}\n")
            sys.exit(1)


def parse_json(raw: str) -> Any:
    """Parse *raw* JSON string into a Python object.
    Exits with code 2 on parsing errors.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"[Error] Invalid JSON: {exc.msg} (line {exc.lineno})\n")
        sys.exit(2)
    except Exception as exc:
        sys.stderr.write(f"[Error] Unexpected JSON error: {exc}\n")
        sys.exit(4)


def apply_query(data: Any, query: str) -> Any:
    """Apply *query* (JMESPath) to *data*.
    Exits with code 3 on query failures.
    """
    try:
        compiled = jmespath.compile(query)
        return compiled.search(data)
    except jmespath.exceptions.JMESPathError as exc:
        sys.stderr.write(f"[Error] JMESPath query error: {exc}\n")
        sys.exit(3)
    except Exception as exc:
        sys.stderr.write(f"[Error] Unexpected query error: {exc}\n")
        sys.exit(4)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract data from JSON using a JMESPath expression.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "source",
        help="Path to JSON file or '-' to read from STDIN.",
    )
    parser.add_argument(
        "query",
        help="JMESPath expression to apply to the JSON document.",
    )
    args = parser.parse_args()

    raw_json = read_input(args.source)
    data = parse_json(raw_json)
    result = apply_query(data, args.query)

    # Print result as pretty‑printed JSON if it's a complex structure,
    # otherwise use the raw representation.
    if isinstance(result, (dict, list)):
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    else:
        sys.stdout.write(str(result))
    sys.stdout.write("\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
