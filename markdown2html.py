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

    MD_INPUT_FILE_ITER = iter(MD_INPUT_FILE)

    for line in MD_INPUT_FILE_ITER:

        for hashtag_amount in range(1, 6 + 1):
            HEADING_LINE_START = "#" * hashtag_amount + " "

            if line.startswith(HEADING_LINE_START):

                REST_OF_LINE = line[hashtag_amount + 1:].strip()
                HTML_OUTPUT_FILE.write(f"<h{hashtag_amount}>{REST_OF_LINE}</h{hashtag_amount}>\n")

        UL_LINE_START = "- "

        if line.startswith(UL_LINE_START):

            # Write "<ul>", then
            # continue to iterate through the next 'line's
            # Using next(MD_INPUT_FILE_ITER),
            # until the lines beginning with 'UL_LINE_START' are over,
            # and we can then write "</ul>\n"

            HTML_OUTPUT_FILE.write("<ul>\n")

            while line.startswith(UL_LINE_START):
                
                HTML_OUTPUT_FILE.write("<li>" + line[len(UL_LINE_START):].strip() + "</li>\n")

                try:
                    line = next(MD_INPUT_FILE_ITER)
                except StopIteration:
                    break

            HTML_OUTPUT_FILE.write("</ul>\n")

    exit(0)
