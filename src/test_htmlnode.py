import unittest

from htmlnode import HTMLNode

from htmlnode import LeafNode

from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a paragraph", None, {"href": "https://example.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"' )
        
    def test_noprops(self):
        node = HTMLNode("p", "this is a paragraph", None, None)
        self.assertEqual(node.props_to_html(), "")
            
    def test_emptyprops(self):
        node = HTMLNode("p", "this is a paragraph", None, {})
        self.assertEqual(node.props_to_html(), "") 
                
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
                    
    def test_leaf_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "greeting"})
        self.assertEqual(node.to_html(), '<p class="greeting">Hello, world!</p>')
                        
    def test_leaf_without_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
                                
    def test_leaf_without_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_without_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError, msg = "no tag"):
            parent_node.to_html()
            
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", [])
        parent_node.children = None
        with self.assertRaises(ValueError, msg = "no children"):
            parent_node.to_html()
            
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ],
        )
        self.assertEqual(
        node.to_html(),
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )