from node_maker import split_nodes_delimiter
from textnode import TextNode, TextType
import unittest

class TestNodeMaker(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        text1 = "This is **bold** text."
        text2 = "This is **bold** and **another bold** text."
        text3 = "This is **bold** and ~italic~ text."
        node1 = TextNode(text1, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)
        node3 = TextNode(text3, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        #for node in new_nodes:
            #print(node.__repr__())
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text.", TextType.TEXT))
    
    def test_split_nodes_delimiter_italic(self):
        text1 = "This is ~italic~ text."
        text2 = "This is ~italic~ and ~another italic~ text."
        text3 = "This is ~italic~ and **bold** text."
        node1 = TextNode(text1, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)
        node3 = TextNode(text3, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "~", TextType.ITALIC)
        #for node in new_nodes:
            #print(node.__repr__())
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" text.", TextType.TEXT))
    
    def test_split_nodes_delimiter_invalid_syntax(self):
        text1 = "This is **bold text."
        node1 = TextNode(text1, TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**", TextType.BOLD)
    
    def test_split_nodes_delimiter_no_delimiter(self):
        text1 = "This is bold text."
        node1 = TextNode(text1, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This is bold text.", TextType.TEXT))

