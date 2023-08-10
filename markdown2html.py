#!/usr/bin/python3
"""
Converts markdown to HTML.

Usage: ./markdown2html.py <MD input file> <HTML output file>
"""
from sys import argv, stderr, exit


def decorate_line(line: str, html_output_file):
    """
    Returns a new string like line,
    but with its mardown decorations ("**...**", "__...__")
    as their corresponding HTML tags (<b>...</b>, <em></em>)

    Using a stack, to allow for nested decorations.
    
    INVALID OPENING AND CLOSING DECORATIONS BREAK THIS FUNCTION!!
    """
    decoration_stack = []
    index = 0

    result = line

    while index < len(line):
        for md, html in {"**": "b", "__": "em"}.items():
            if line.startswith(md, index):
                if decoration_stack == [] or decoration_stack[-1] != md:
                    decoration_stack.append(md)
                    result = result[:index] + f"<{html}>" + result[index + len(md):]
                else:
                    decoration_stack.pop()
                    result = result[:index] + f"</{html}>" + result[index + len(md):]
                index += 2
                break
        else:
            index += 1


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

    previous_line_type: str = ""

    for line in MD_INPUT_FILE_ITER:

        # Close opened tags, if any
        if previous_line_type == "p" and not line[:-1]:
            HTML_OUTPUT_FILE.write("</p>\n")
        elif previous_line_type == "ul" and not line.startswith("- "):
            HTML_OUTPUT_FILE.write("</ul>\n")
        elif previous_line_type == "ol" and not line.startswith("* "):
            HTML_OUTPUT_FILE.write("</ol>\n")

        if line.startswith("#"):

            for hashtag_amount in range(1, 6 + 1):
                HEADING_LINE_START = "#" * hashtag_amount + " "

                if line.startswith(HEADING_LINE_START):

                    REST_OF_LINE = line[hashtag_amount + 1:].strip()
                    HTML_OUTPUT_FILE.write(f"<h{hashtag_amount}>{REST_OF_LINE}</h{hashtag_amount}>\n")

                    previous_line_type = "h"
                    break
            else:
                if previous_line_type == "p":
                    HTML_OUTPUT_FILE.write("<br>")
                else:
                    HTML_OUTPUT_FILE.write("<p>")

                HTML_OUTPUT_FILE.write(line.strip())
                previous_line_type = "p"

        elif line.startswith("- ") or line.startswith("* "):

            for list_line_start, list_tag in {"- ": "ul", "* ": "ol"}.items():
                if line.startswith(list_line_start):

                    if previous_line_type != list_tag:
                        HTML_OUTPUT_FILE.write(f"<{list_tag}>\n{line.strip()}")

                    previous_line_type = list_tag
        elif line[:-1]:
            if previous_line_type == "p":
                HTML_OUTPUT_FILE.write("<br>")
            else:
                HTML_OUTPUT_FILE.write("<p>")

            HTML_OUTPUT_FILE.write(line.strip())
            previous_line_type = "p"

    exit(0)
