from textnode import TextType, TextNode
from copystatic import copy_dir
from gencontent import generate_page, generate_pages_recursive
import sys
def main():
    basepath = ""
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_dir("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

main()