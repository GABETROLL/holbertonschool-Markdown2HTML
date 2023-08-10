#!/usr/bin/python3
"""
Converts markdown to HTML.

Usage: ./markdown2html.py <MD input file> <HTML output file>
"""
from sys import argv, stderr, exit


if __name__ == "__main__":
    assert argv

    if len(argv) < 3:
        print(f"Usage: {argv[0]} README.md README.html", file=stderr)
        exit(1)

    MD_INPUT_FILE_NAME = argv[1]
    HTML_OUTPUT_FILE_NAME = argv[2]

    try:
        MD_INPUT_FILE = open(MD_INPUT_FILE_NAME)
    except FileNotFoundError:
        print(f"Missing {MD_INPUT_FILE_NAME}", file=stderr)
        exit(1)

    HTML_OUTPUT_FILE = open(HTML_OUTPUT_FILE_NAME, "w")

    for line in MD_INPUT_FILE:
        for hashtag_amount in range(1, 6 + 1):
            HEADING_LINE_START = "#" * hashtag_amount + " "

            if line.startswith(HEADING_LINE_START):

                REST_OF_LINE = line[hashtag_amount + 1:].strip()
                HTML_OUTPUT_FILE.write(f"<h{hashtag_amount}>{REST_OF_LINE}</h{hashtag_amount}>")

    exit(0)
