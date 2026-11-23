#!/usr/bin/env python3
"""Entry program for the one-line gadget roast.

It reads the single roast line from entry.txt, sitting beside this script,
and writes it verbatim to the output file the competition expects. Paths
are derived from this file's own directory and the documented environment
variables; the caller's working directory is never consulted.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRY_PATH = os.path.join(BASE_DIR, "entry.txt")


def resolve_output():
    """Pick the output path: ENTRY_OUTPUT wins, then the output dir vars."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for key in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(key)
        if directory:
            return os.path.join(directory, "entry.txt")
    return os.path.join("/output", "entry.txt")


GADGET_WORDS = (
    "printer", "phone", "laptop", "tablet", "watch", "headphone", "earbud",
    "speaker", "camera", "mouse", "keyboard", "monitor", "router", "wifi",
    "charger", "remote", "fridge", "microwave", "vacuum", "toaster", "car",
    "app", "laptop", "computer", "screen", "battery",
)


def validate(payload):
    """Gate check: entry.txt must be one line, 1-200 characters."""
    line = payload.decode("utf-8").strip()
    if not line:
        raise ValueError("entry.txt is empty")
    if len(line) > 200 or "\n" in line:
        raise ValueError("entry.txt must hold a single line of 1-200 characters")
    lowered = line.lower()
    if not any(word in lowered for word in GADGET_WORDS):
        raise ValueError("the roast line must name a gadget or app")
    return payload


def run():
    with open(ENTRY_PATH, "rb") as source:
        data = validate(source.read())
    output = resolve_output()
    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "wb") as sink:
        sink.write(data)
    # The grader's scorer must be able to read the output, regardless of
    # the caller's umask: make it readable by everyone.
    os.chmod(output, 0o644)


if __name__ == "__main__":
    run()
