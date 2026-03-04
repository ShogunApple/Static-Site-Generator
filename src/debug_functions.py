from test_node_maker import TestNodeMaker
from test_textnode import TestTextNode, TestRegex
import unittest

test = TestNodeMaker()
test2 = TestRegex()
test3 = TestTextNode()

#test2.test_extract_markdown_images()
#test.test_split_nodes_image()
test3.test_text_to_textnodes()
