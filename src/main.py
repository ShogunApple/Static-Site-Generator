from textnode import TextType, TextNode
from copystatic import copy_dir
from gencontent import generate_page, generate_pages_recursive
def main():
    copy_dir("static", "public")

    generate_pages_recursive("content", "template.html", "public")

main()