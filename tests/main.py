#!/usr/bin/python3
"""
Test case
"""
import os
import random
import string
import time
from bs4 import BeautifulSoup

def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


fn_md = "{}.md".format(random_string())
fn_html = "{}.html".format(random_string())

# remove initial MD file
if os.path.exists(fn_md):
    os.remove(fn_md)

# remove initial HTML file
if os.path.exists(fn_html):
    os.remove(fn_html)

# create MD file
c = """
Hello Holberton

How are you?
Fine and you?
"""
with open(fn_md, 'w') as f:
    f.write(c)

# run
os.system("./markdown2html.py {} {}".format(fn_md, fn_html))
time.sleep(1)

result = [
    { 'name': 'p', 'value': "Hello Holberton" },
    { 'name': 'p', 'children': [
        { 'value': "How are you?" },
        { 'name': 'br' },
        { 'value': "Fine and you?" }
        ]
    }
]

# parse HTML file
with open(fn_html, "r") as f:
    root = BeautifulSoup(f.read(), 'html.parser')
    all_tags = root.find_all(recursive=False)
    if len(all_tags) == 0:
        print("No tag found")
        exit(1)
    if len(all_tags) != len(result):
        print("Too many tags: {}".format(all_tags))
        exit(1)
    
    for tag in all_tags:
        r_tag = result[0]
        if tag.name != r_tag['name']:
            print("Wrong name: {} instead of {}".format(tag.name, r_tag['name']))
            exit(1)
        
        r_tag_children = r_tag.get('children')
        if r_tag_children is not None:
            for tag_child in tag.children:
                r_tag_child = r_tag_children[0]
                if tag_child.name != r_tag_child.get('name'):
                    print("Wrong name: {} instead of {}".format(tag_child.name, r_tag_child.get('name')))
                    exit(1)
                s_tag_child = tag_child.string
                if s_tag_child is None:
                    s_tag_child = ""
                s_tag_child = s_tag_child.strip()
                if s_tag_child != r_tag_child.get('value', ""):
                    print("Wrong content: {} instead of {}".format(s_tag_child, r_tag_child.get('value', "")))
                    exit(1)
                del r_tag_children[0]

            if len(r_tag_children) != 0:
                print("Some children tags are not found: {}".format(r_tag_children))
                exit(1)
        else:
            s_tag = tag.string.strip()
            if s_tag != r_tag['value']:
                print("Wrong content: {} instead of {}".format(s_tag, r_tag['value']))
                exit(1)

        del result[0]
    
    if len(result) != 0:
        print("Some tags are not found: {}".format(result))
        exit(1)

    print("OK", end="")

# delete files
if os.path.exists(fn_md):
    os.remove(fn_md)
if os.path.exists(fn_html):
    os.remove(fn_html)
