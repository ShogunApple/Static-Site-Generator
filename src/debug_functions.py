from test_node_maker import TestNodeMaker
from test_textnode import TestTextNode, TestRegex
from test_block_maker import TestBlockMaker
from gencontent import generate_page
import unittest

test = TestNodeMaker()
test2 = TestRegex()
test3 = TestTextNode()
test4 = TestBlockMaker()

generate_page("content/index.md", "template.html", "public/index.html")


#test2.test_extract_markdown_images()
#test.test_split_nodes_image()
#test3.test_text_to_textnodes()
#test4.test_block_to_block_type()
#test.test_paragraphs() 
#test.test_codeblock()
#test.test_combination()