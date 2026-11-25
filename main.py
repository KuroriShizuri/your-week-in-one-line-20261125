#!/usr/bin/env python3
"""Your week in one line: a week of wins and one apology, compressed.

The entry is a single sentence summing up a chaotic week — two bounties
won, production broken once, a cat apologised to — and a boss who still
wants more. This script guards the sentence against edits that would
break the competition's one-line, hundred-character limit, and writes it
out as entry.txt for the make.fun harness.

    python3 main.py              write entry.txt into MAKEFUN_OUTPUT_DIR
                                 (or the current directory when unset)
    python3 main.py --check      validate only, write nothing
    python3 main.py --self-test  validate, write, and verify the file

Standard library only; nothing is fetched from the network and the
output is fully deterministic.
"""

import argparse
import os
import sys

ENTRY = (
    "Won two bounties, broke prod once, apologized to a cat \u2014 "
    "and my boss still asked if there's more."
)

CHAR_LIMIT = 100
ENTRY_FILENAME = "entry.txt"


def abort(reason):
    sys.stderr.write("failure: %s\n" % reason)
    sys.exit(1)


def find_problems(text):
    """Collect every violated rule; an empty list means the text passes."""
    problems = []
    if text == "":
        problems.append("entry must not be empty")
    if len(text) > CHAR_LIMIT:
        problems.append(
            "entry is %d characters long, limit is %d"
            % (len(text), CHAR_LIMIT)
        )
    if "\n" in text:
        problems.append("entry must be exactly one line")
    if "\r" in text:
        problems.append("entry must not contain carriage returns")
    return problems


def check_or_abort(text):
    problems = find_problems(text)
    if problems:
        abort("; ".join(problems))


def output_path():
    directory = os.getenv("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, ENTRY_FILENAME)


def produce():
    """Write the entry, then prove the file on disk is exactly right."""
    check_or_abort(ENTRY)
    path = output_path()
    blob = (ENTRY + "\n").encode("utf-8")
    with open(path, "wb") as out:
        out.write(blob)
    with open(path, "rb") as back:
        stored = back.read()
    if stored != blob:
        abort("entry.txt bytes differ from the entry")
    if stored.decode("utf-8").rstrip("\n") != ENTRY:
        abort("entry.txt text differs from the entry")
    check_or_abort(stored.decode("utf-8").rstrip("\n"))
    print("entry written to %s (%d bytes)" % (path, len(blob)))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Validate and emit the one-line week summary."
    )
    parser.add_argument(
        "--check", action="store_true",
        help="validate the entry without writing any file",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="validate, write entry.txt, and verify what was written",
    )
    return parser.parse_args(argv)


def run(argv):
    args = parse_args(argv)
    if args.check:
        check_or_abort(ENTRY)
        print("check passed: %d characters, one line" % len(ENTRY))
        return 0
    produce()
    if args.self_test:
        print("self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
