"""
Converts markdown to HTML.

Usage: ./markdown2html.py <MD input file> <HTML output file>
"""
from sys import argv, stderr, exit

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: {argv[0]} README.md README.html", file=stderr)
        exit(1)

    MD_INPUT_FILE_NAME = argv[1]
    HTML_OUTPUT_FILE_NAME = argv[2]

    try:
        MD_INPUT_FILE = open(MD_INPUT_FILE_NAME)
    except FileNotFoundError:
        print(f"Missing {MD_INPUT_FILE_NAME}", stderr)
        exit(1)

    HTML_OUTPUT_FILE = open(HTML_OUTPUT_FILE_NAME, "w")

    exit(0)
