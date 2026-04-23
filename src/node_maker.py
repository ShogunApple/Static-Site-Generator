from textnode import TextType, TextNode, extract_markdown_images, extract_markdown_links, text_node_to_html
from htmlnode import LeafNode, ParentNode
from block_maker import markdown_to_blocks, block_to_block_type, BlockType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Invalid markdown syntax")
            for i in range(0, len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

#Replanning:
# I have text that looks like: "This is a markdown image ![alt text](https://example.com/image.png) This is another markdown image ![alt text2](https://example.com/image2.png) and some more text!"
# I want to split this into three nodes:
# TextNode("This is a markdown image ", TextType.TEXT)
# TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
# TextNode(" and some more text", TextType.TEXT)
# First thing I need to do is seperate the text into parts. 
# if I use redex on the whole string, I will get a list of tuples with each alt text and string. The len of the resulting list is the number of images
# It will look like: images = [("alt text", "https://example.com/image.png"), ("alt text2", "https://example.com/image2.png")]
# If I do .split(immages[0][0], 1)) I would end up with just the the text before the first image, which i can turn into a text node
# i should save that .split into a variable called split1. It would be a list with 2 elements, the text before the first link, then the rest of it

# as long as my redex returns not None, If i split the text by redex[0]+[1] with maxsplit 1, I am going to get the text before the first image, then the text after.
# I should repeat this for each tuple in the redex list, splitting the second half of the string each time. At the end I check if the second half of the split is empty, if it is I am done.


def split_nodes_image(old_nodes):
    #get my list of nodes that I want to run through. Each is a text node with text that may or may not contain markdown images
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:   
        #first i need to get the redex to find out if there is anything inside the text
            images = extract_markdown_images(node.text)
            if images == []:
                new_nodes.append(node)
            else:
                #now I know that there are images. So I start splitting the text
                current_text = node.text
                #for each tuple in the images list, split the string by both the alt text and url with a maxsplit of 1.
                for image in images:
                    new_text = current_text.split(f"![{image[0]}]({image[1]})", 1)
                    if new_text[0] != "":
                        new_nodes.append(TextNode(new_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    current_text = new_text[1]
                #at the end of the loop, there is either some remaining text at the end, our current_text is an empty string
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if links == []:
                new_nodes.append(node)
            else:
                current_text = node.text
                for link in links:
                    new_text = current_text.split(f"[{link[0]}]({link[1]})", 1)
                    if new_text[0] != "":
                        new_nodes.append(TextNode(new_text[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    current_text = new_text[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

#First we need to convert our string into a text node
#Then we go by calling any of our splitting functions. It will return a list of nodos, with any of its type being converted.
#Repeat for each type, ignoring any node that isnt TextType.TEXT
def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = [text_node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_delimiter([node], "_", TextType.ITALIC))
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_delimiter([node], "`", TextType.CODE))
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_image([node]))
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_link([node]))
        else:
            new_nodes.append(node)
    return new_nodes
# make a parent node that is your div. Its children will be the blocks.
#Split markdown into block with markdown_to_blocks
#each block is basically a paragraph that will have text markdown in it.
#the type of block will be defined
#loop over each block:
#   get type of block with block_to_block_type
#   make a parent node with the tag of the block type. all of the text will be in the children.
#   for each block, run text_to_textnodes to get a list of all the text nodes with correct types.
#   Loop over the list from text_to_textnodes
#       turn them all into leaf_nodes, and add them as children to the parent node. Use a helper function for this.
#   add the parent node to the big div parent node.
# at the end return the big div.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        parent_block = block_to_html_node(block)
        parent_nodes.append(parent_block)
    return ParentNode("div", parent_nodes)

#Helper function that takes a block and turn it into a parent node depending on the block type.
#uses helper functions for each block type
def block_to_html_node(block):
    result = block_to_block_type(block)
    if result == BlockType.PARAGRAPH:
        return block_to_paragraph_node(block)
    elif result == BlockType.HEADING:
        return block_to_heading_node(block)
    elif result == BlockType.CODE:
        return block_to_code_node(block)
    elif result == BlockType.QUOTE:
        return block_to_quote_node(block)
    elif result == BlockType.UNORDERED_LIST:
        return block_to_unordered_list_node(block)
    elif result == BlockType.ORDERED_LIST:
        return block_to_ordered_list_node(block)

def block_to_paragraph_node(block):
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p", children)

def block_to_heading_node(block):
    count = len(block) - len(block.lstrip("#"))
    block = block.strip("#").strip()
    children = text_to_children(block)
    return ParentNode(f"h{count}", children)

def block_to_code_node(block):
    block = block.removeprefix("```\n").removesuffix("```")
    child = LeafNode(None, block)
    return ParentNode("pre", [ParentNode("code", [child])])

def block_to_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        line = line.lstrip(">").strip()
        new_lines.append(line)
    block = "\n".join(new_lines)
    children = text_to_children(block)
    return ParentNode("blockquote", children)

def block_to_unordered_list_node(block):
    split_list = block.split("\n")
    list_nodes = []
    for line in split_list:
        line = line.strip("-").strip()
        children = text_to_children(line)
        list_nodes.append(ParentNode("li", children))
    return ParentNode("ul", list_nodes)

def block_to_ordered_list_node(block):
    split_list = block.split("\n")
    list_nodes = []
    for line in split_list:
        line = line.split(". ",1)[1]
        children = text_to_children(line)
        list_nodes.append(ParentNode("li", children))
    return ParentNode("ol", list_nodes)

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_nodes.append(text_node_to_html(node))
    return html_nodes