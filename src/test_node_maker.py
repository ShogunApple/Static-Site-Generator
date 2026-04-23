from node_maker import markdown_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link
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
    
    #TESTING FOR THE WHOLE MARKDOWN TO HTML NODE FUNCTION
    #Test paragraphs DONE
    #Test code block DONE
    #Test headings DONE
    #Test blockquotes
    #Test unordered lists
    #test ordered lists
    #test unordered list with markdown in it
    #test ordered list with markdown in it
    #test a combination of all of the above in one markdown string
    #Test to make sure it works with empty lines and whitespace
    #Test to make sure it works with just an empty string
    #Test to make sure it works with just a string with whitespace
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
    def test_paragraph(self):
        md = """This is a paragraph with some text in it."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with some text in it.</p></div>",
        )
    def test_heading(self):
        md = """# This is a heading"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>",
        )
    def test_blockquote(self):
        md = """> This is a blockquote\n> with multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote\nwith multiple lines</blockquote></div>",
        )
    def test_unordered_list(self):
        md = """- This is an unordered list item\n- With multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list item</li><li>With multiple lines</li></ul></div>",
        )
    def test_ordered_list(self):
        md = """1. This is an ordered list item\n2. With multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list item</li><li>With multiple lines</li></ol></div>",
        )  
    def test_unordered_list_with_markdown(self):
        md = """- This is an unordered list item with **bold** text\n- With multiple lines and _italic_ text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list item with <b>bold</b> text</li><li>With multiple lines and <i>italic</i> text</li></ul></div>",
        )
    def test_ordered_list_with_markdown(self):
        md = """1. This is an ordered list item with **bold** text\n2. With multiple lines and _italic_ text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list item with <b>bold</b> text</li><li>With multiple lines and <i>italic</i> text</li></ol></div>",
        )
    def test_combination(self):
        md = """# This is a heading\n\nThis is a paragraph with some text in it.\n\n> This is a blockquote\n> with multiple lines\n\n- This is an unordered list item\n- With multiple lines\n\n1. This is an ordered list item\n2. With multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a paragraph with some text in it.</p><blockquote>This is a blockquote\nwith multiple lines</blockquote><ul><li>This is an unordered list item</li><li>With multiple lines</li></ul><ol><li>This is an ordered list item</li><li>With multiple lines</li></ol></div>",
        )
    def test_empty_string(self):
        md = ""
        node = markdown_to_html_node(md)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_whitespace_string(self):
        md = "   \n   "
        node = markdown_to_html_node(md)
        with self.assertRaises(ValueError):
            node.to_html(
        )
    
    
    



