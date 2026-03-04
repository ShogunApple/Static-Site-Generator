from node_maker import split_nodes_delimiter, split_nodes_image, split_nodes_link
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
    
    #Tests to run:
    #Test to make sure it splits an image correctly DONE
    #Test to make sure it splits a link correctly DONE
    #Run a test with multiple images DONE
    #Run a test with multiple links DONE
    #Run a test with empty text DONE
    #Run a test with empty text and a link or image DONE
    #Run a test with multiple of the same image or link
    
    def test_split_nodes_images(self):
        node1 = TextNode("This is a markdown image ![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes[0], TextNode("This is a markdown image ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
    
    def test_split_nodes_links(self):
        node1 = TextNode("This is a markdown link [link text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node1])
        self.assertEqual(new_nodes[0], TextNode("This is a markdown link ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link text", TextType.LINK, "https://example.com"))
    
    def test_split_nodes_multiple_images(self):
        node1 = TextNode("This is a markdown image ![alt text](https://example.com/image.png) This is another markdown image ![alt text2](https://example.com/image2.png) and some more text!", TextType.TEXT)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes[0], TextNode("This is a markdown image ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
        self.assertEqual(new_nodes[2], TextNode(" This is another markdown image ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("alt text2", TextType.IMAGE, "https://example.com/image2.png"))
        self.assertEqual(new_nodes[4], TextNode(" and some more text!", TextType.TEXT))
    
    def test_split_nodes_multiple_links(self):
        node1 = TextNode("This is a markdown link [link text](https://example.com) This is another markdown link [link text2](https://example.com/link2) and some more text!", TextType.TEXT)
        new_nodes = split_nodes_link([node1])
        self.assertEqual(new_nodes[0], TextNode("This is a markdown link ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link text", TextType.LINK, "https://example.com"))
        self.assertEqual(new_nodes[2], TextNode(" This is another markdown link ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("link text2", TextType.LINK, "https://example.com/link2"))
        self.assertEqual(new_nodes[4], TextNode(" and some more text!", TextType.TEXT))
    
    def test_split_nodes_empty_text(self):
        node1 = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes[0], node1)
    
    def test_split_nodes_empty_text_with_image(self):
        node1 = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes[0], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
    
    def test_split_nodes_empty_text_with_link(self):
        node1 = TextNode("[link text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node1])
        self.assertEqual(new_nodes[0], TextNode("link text", TextType.LINK, "https://example.com"))
    
    def test_split_nodes_multiple_same_images(self):
        node1 = TextNode("This is a markdown image ![alt text](https://example.com/image.png) This is another markdown image ![alt text](https://example.com/image.png) and some more text!", TextType.TEXT)
        new_nodes = split_nodes_image([node1])
        self.assertEqual(new_nodes[0], TextNode("This is a markdown image ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
        self.assertEqual(new_nodes[2], TextNode(" This is another markdown image ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"))
        self.assertEqual(new_nodes[4], TextNode(" and some more text!", TextType.TEXT))
    
    



