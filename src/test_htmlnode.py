import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "hello world")
        node2 = HTMLNode("p", "hello world")
        self.assertEqual(str(node), str(node2))
        
    def test_None_children_props(self):
        node = HTMLNode("p", "hello world")
        node2 = HTMLNode("p", "hello world", None, None)
        self.assertEqual(str(node), str(node2))
        
    def test_props(self):
        node = HTMLNode("a", "hello world", None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("a", "hello world", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        
    def test_props_print(self):
        node = HTMLNode("a", "hello world", None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), node2)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Hello, world!</a>")
        
    def test_value_not_None(self):
        node = LeafNode()
        self.assertRaises(TypeError, node)

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("i", "italic child")
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><i>italic child</i></div>")
        
    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode("i", "italic grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node_2 = ParentNode("span", [grandchild_node_2])
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span><span><i>italic grandchild</i></span></div>")
        
    def test_to_html_missing_grandchild(self):
        grandchild_node_2 = LeafNode("i", "italic grandchild")
        child_node = ParentNode("span", [])
        child_node_2 = ParentNode("span", [grandchild_node_2])
        parent_node = ParentNode("div", [child_node, child_node_2])
        with self.assertRaisesRegex(ValueError, "No children found"):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
