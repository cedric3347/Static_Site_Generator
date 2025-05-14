import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_empty(self):
        # test with no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        # test with a single property
        node = HTMLNode(props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
        
    def test_props_to_html_multiple_props(self):
        # test with multiple properties
        node = HTMLNode(props={
            "href": "https://www.example.com",
            "target": "_blank"
        })
        
        # check for both possible orders of properties in a dictionary
        result = node.props_to_html()
        possible_outputs = [
            ' href="https://www.example.com" target="_blank"',
            ' target="_blank" href="https://www.example.com"'
        ]
        self.assertIn(result, possible_outputs)

    def test_node_initialization(self):
        # test that all parameters are stored correctly
        node = HTMLNode("div", "content", ["child1", "child2"], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "container"})

    def test_default_values(self):
        # test defualt values
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_props_to_html_raises_error(self):
        # makes sure props_to_html raises error
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html() 
 
    def test_repr_method(self):
        # test __repr__
        node = HTMLNode("p", "Hello", None, {"class": "greeting"})
        repr_str = repr(node)
        self.assertIn("tag='p'", repr_str)
        self.assertIn("value='Hello'", repr_str)
        self.assertIn("children=None", repr_str)
        self.assertIn("props={'class': 'greeting'}", repr_str)

    def test_leaf_to_html_p(self):
        # test leafNode conversions 
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        # test link tag 
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')    

    def test_leaf_to_html_no_tag(self):
        # test None case
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_no_value(self):
        # test ValueError
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()    
    
    def test_leaf_to_html_multiple_props(self):
        # test multiple properties
        node = LeafNode("input", "", {"type": "text", "id": "username", "name": "username"})
        self.assertEqual(node.to_html(), '<input type="text" id="username" name="username"></input>')

if __name__== "__main__":
    unittest.main()