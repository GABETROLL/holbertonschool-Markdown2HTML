#!/usr/bin/python3
"""
Converts markdown to HTML.

Usage: ./markdown2html.py <MD input file> <HTML output file>
"""
from sys import argv, stderr, exit
from hashlib import md5


def decorated_line(line: str, inside_header: bool = False, start_line_index: int = 0):
    """
    Returns a new string like line,
    but with its mardown decorations ("**...**", "__...__")
    as their corresponding HTML tags (<b>...</b>, <em></em>)
    and these markdown decorations: "[[...]]", "((...))"
    as the MD5 of the content and the content without 'c's (case-sensitive)

    'inside_header' indicates if the line is part of a header,
    so that <em>'s can instead be <b>'s.

    'start_line_index' is the start of the line that needs to be processed,
    used for recursion.
    """

    result: str = ""
    line_index: int = start_line_index

    bold_opened: bool = False
    em_opened: bool = False

    decoration_stack: list[str] = []

    while line_index < len(line):
        if line.startswith("((", line_index):
            inner_result: str = decorated_line(line, inside_header=inside_header, start_line_index=line_index + 2)
            line_index += len(inner_result) + 2
            result += inner_result

        elif line.startswith("))", line_index):
            return result.replace("c", "")

        elif line.startswith("[[", line_index):
            inner_result: str = decorated_line(line, inside_header=inside_header, start_line_index=line_index + 2)
            line_index += len(inner_result) + 2
            result += inner_result

        elif line.startswith("]]", line_index):
            return md5(result)

        elif line.startswith("**", line_index):
            if bold_opened:
                result += "</b>"
            else:
                result += "<b>"

            bold_opened = not bold_opened

            line_index += 2
        
        elif line.startswith("__", line_index):
            EM_TAG = "em" if not inside_header else "b"
            if em_opened:
                result += f"</{EM_TAG}>"
            else:
                result += f"<{EM_TAG}>"

            em_opened = not em_opened

            line_index += 2
        
        else:
            result += line[line_index]
            line_index += 1

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

                    HTML_OUTPUT_FILE.write(f"<li>{DECORATED_REST_OF_LINE.strip()}</li>")
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
