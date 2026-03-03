from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):       
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html(text_node):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
        return node
    elif text_node.text_type == TextType.BOLD:
        node = LeafNode("b", text_node.text)
        return node
    elif text_node.text_type == TextType.ITALIC:
        node = LeafNode("i", text_node.text)
        return node
    elif text_node.text_type == TextType.CODE:
        node = LeafNode("code", text_node.text)
        return node
    elif text_node.text_type == TextType.LINK:
        node = LeafNode("a", text_node.text, {"href": text_node.url})
        return node
    elif text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        return node
    else:
        raise Exception("Invalid text type")

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches