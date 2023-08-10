#!/usr/bin/python3
"""
Converts markdown to HTML.

Usage: ./markdown2html.py <MD input file> <HTML output file>
"""
from sys import argv, stderr, exit


def decorated_line(line: str, inside_header: bool = False):
    """
    Returns a new string like line,
    but with its mardown decorations ("**...**", "__...__")
    as their corresponding HTML tags (<b>...</b>, <em></em>)

    Using a stack, to allow for nested decorations.

    If 'inside_header' is True, the 'em's will be 'b's instead.

    INVALID OPENING AND CLOSING DECORATIONS BREAK THIS FUNCTION!!
    """
    decoration_stack = []
    input_index = 0

    result = ""

    MD_TO_HTML_DECORATIONS = {"**": "b", "__": "em" if not inside_header else "b"}

    while input_index < len(line):
        for md, html in MD_TO_HTML_DECORATIONS.items():
            if line.startswith(md, input_index):
                if decoration_stack == [] or decoration_stack[-1] != md:
                    decoration_stack.append(md)
                    result += f"<{html}>"
                else:
                    decoration_stack.pop()
                    result += f"</{html}>"
                input_index += 2
                break
        else:
            result += line[input_index]
            input_index += 1

    return result


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

    previous_line_type: str = ""

    for line in MD_INPUT_FILE:

        # Close opened tags, if any
        if previous_line_type == "p" and not line[:-1]:
            HTML_OUTPUT_FILE.write("</p>")
        elif previous_line_type == "ul" and not line.startswith("- "):
            HTML_OUTPUT_FILE.write("</ul>")
        elif previous_line_type == "ol" and not line.startswith("* "):
            HTML_OUTPUT_FILE.write("</ol>")

        if line.startswith("#"):

            for hashtag_amount in range(1, 6 + 1):
                HEADING_LINE_START = "#" * hashtag_amount + " "

                if line.startswith(HEADING_LINE_START):

                    REST_OF_LINE = line[hashtag_amount + 1:].strip()
                    DECORATED_LINE = decorated_line(REST_OF_LINE, inside_header=True)
                    #        ("__...__" used inside of a MD heading ^ should output bold in HTML)
                    HTML_OUTPUT_FILE.write(f"<h{hashtag_amount}>{DECORATED_LINE}</h{hashtag_amount}>")

                    previous_line_type = "h"
                    break
            else:
                if previous_line_type == "p":
                    HTML_OUTPUT_FILE.write("<br>")
                else:
                    HTML_OUTPUT_FILE.write("<p>")

                DECORATED_LINE = decorated_line(REST_OF_LINE)
                HTML_OUTPUT_FILE.write(DECORATED_LINE)
                previous_line_type = "p"

        elif line.startswith("- ") or line.startswith("* "):

            for list_line_start, list_tag in {"- ": "ul", "* ": "ol"}.items():
                if line.startswith(list_line_start):

                    if previous_line_type != list_tag:
                        HTML_OUTPUT_FILE.write(f"<{list_tag}>")
                    
                    REST_OF_LINE = line[len(list_line_start):]
                    DECORATED_REST_OF_LINE = decorated_line(REST_OF_LINE)

                    HTML_OUTPUT_FILE.write(f"</li>{DECORATED_REST_OF_LINE.strip()}</li>")
                    previous_line_type = list_tag
                    break
        elif line.strip():
            if previous_line_type == "p":
                HTML_OUTPUT_FILE.write("<br>")
            else:
                HTML_OUTPUT_FILE.write("<p>")

            DECORATED_LINE = decorated_line(line)
            HTML_OUTPUT_FILE.write(DECORATED_LINE)
            previous_line_type = "p"
        else:
            previous_line_type = ""

    # Close opened tags, if any
    if previous_line_type == "p":
        HTML_OUTPUT_FILE.write("</p>\n")
    elif previous_line_type == "ul":
        HTML_OUTPUT_FILE.write("</ul>\n")
    elif previous_line_type == "ol":
        HTML_OUTPUT_FILE.write("</ol>\n")

    exit(0)
