import unittest
from textnode import TextNode, TextType, extract_markdown_images, text_node_to_html, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.node = TextNode("This is a text node", TextType.BOLD)
        self.node2 = TextNode("This is a text node", TextType.BOLD)
        self.node3 = TextNode("This is also a text node", TextType.BOLD)
        self.node4 = TextNode("This is a text node", TextType.ITALIC)
        self.node5 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
    def test_eq(self):
        self.assertEqual(self.node, self.node2)

    def test_ne(self):
        self.assertNotEqual(self.node, self.node3)

    def test_ne_different_type(self):
        self.assertNotEqual(self.node, self.node4)

    def test_ne_different_url(self):
        self.assertNotEqual(self.node, self.node5)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_itelic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "This is a text node"})
    
class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is a markdown image ![alt text](https://example.com/image.png) and another one ![another alt text](https://example.com/another-image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt text", "https://example.com/image.png"), ("another alt text", "https://example.com/another-image.png")])
    def test_extract_markdown_links(self):
        text = "This is a markdown link [link text](https://example.com) and another one [another link text](https://example.com/another-link)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link text", "https://example.com"), ("another link text", "https://example.com/another-link")])



if __name__ == "__main__":
    unittest.main()