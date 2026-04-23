from enum import Enum

#make a BlockType Enum with the following values:
#paragraph, heading, code, quote, unordered_list, ordered_list
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#Outline:
#Headings start with #, ##, ###, ####, #####, ###### and a space
#Multiline code blocks start with ```\n and end with ```
#Every line in a quote block starts with >
#Every line in an unordered list starts with - and a space
#Every line in an ordered list starts with a number and a period and a space. Must start at 1 and increment by 1
#Else, its a paragraph

#psuedocode:
#takes a single block (a string)
#if string[0] == "#":                   heading
# for char in string[1:]
#  if char == " ": return heading
#  elif: char != "#": break

def block_to_block_type(block):
    if block.startswith("#"):
        count = 1
        for char in block[1:]:
            if char == " ":
                return BlockType.HEADING
            elif char != "#":
                break
            elif char == "#":
                count += 1
                if count > 6:
                    break
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        is_quote = True
        split = block.strip().split("\n")
        for line in split:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    if block.startswith("- "):
        is_unordered_list = True
        split = block.strip().split("\n")
        for line in split:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        current_num = 1
        split = block.strip().split("\n")
        is_ordered_list = True
        for line in split:
            if not line.startswith(f"{current_num}. "):
                is_ordered_list = False
                break
            current_num += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
#psuedocode
#.split("\n\n") the markdown into blocks
#make a new list stripped_strings = []
#for each string in the split markdown: strip = string.strip()
#if strip != "": stripped_strings.append(strip)
#return stripped_strings
def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    stripped_strings = []
    for string in split_markdown:
        strip = string.strip()
        if strip:
            stripped_strings.append(strip)
    return stripped_strings