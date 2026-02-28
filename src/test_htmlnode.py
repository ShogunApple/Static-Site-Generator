import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMLNode("p", "Hello, World!", [], {"href": "https://example.com"})
        self.node2 = HTMLNode("a", "Hello, World!", [], {"href": "https://example.com"})
        self.node3 = HTMLNode("p", "Hello, Universe!", [], {"href": "https://example.com"})
        self.node4 = HTMLNode("p", "Hello, World!", [], {"href": "https://example.com", "class": "link"})
        self.node5 = HTMLNode("p", "Hello, World!", [], {"href": "https://example.com"})
    
    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), ' href="https://example.com"')
        self.assertEqual(self.node4.props_to_html(), ' href="https://example.com" class="link"')
        self.assertEqual(HTMLNode("div").props_to_html(), '')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )
    
    def test_to_html_nested_parents(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node1 = ParentNode("div", [child_node1])
        parent_node2 = ParentNode("section", [parent_node1, child_node2])
        self.assertEqual(
            parent_node2.to_html(),
            "<section><div><span>child1</span></div><span>child2</span></section>"
        )
    
    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>"
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()