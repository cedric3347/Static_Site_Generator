import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    # test equal inputs
    def test_input_equal(self):
        node1 = TextNode("This is the end", TextType.ITALIC)
        node2 = TextNode("This is the end", TextType.ITALIC)
        self.assertEqual(node1, node2)

    # test when test inputs are not equal
    def test_input_not_equal_text(self):
        node1 = TextNode("this is the same", TextType.CODE)
        node2 = TextNode("this is not the same", TextType.CODE)
        self.assertNotEqual(node1, node2)

    # test if TextType are not equal
    def test_input_not_equal_texttype(self):
        node1 = TextNode("this is not the same", TextType.TEXT)
        node2 = TextNode("this is not the same", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_url_none_case(self):
        node1 = TextNode("link", TextType.LINK, "https://test.org")
        node2 = TextNode("link", TextType.LINK)
        self.assertNotEqual(node1, node2)
    
    def test_url_none_case2(self):
        node1 = TextNode("link", TextType.LINK, url=None)
        node2 = TextNode("link", TextType.LINK)
        self.assertEqual(node1, node2)

    def test_url_equal(self):
        node1 = TextNode("link", TextType.LINK, "https://test.org")
        node2 = TextNode("link", TextType.LINK, "https://test.org")
        self.assertEqual(node1, node2)

    def test_url_not_equal(self):
        node1 = TextNode("link", TextType.LINK, "https://equal.com")
        node2 = TextNode("link", TextType.LINK, "https://not_equal.com")
        self.assertNotEqual(node1, node2)


# test for all TextType enum
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")
    
    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
    
    def test_link(self):
        node = TextNode("test.org", TextType.LINK, "https://test.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "test.org")
        self.assertEqual(html_node.props["href"], "https://test.org")
    
    def test_image(self):
        node = TextNode("Alt Text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # empty string value
        self.assertEqual(html_node.props["src"], "image.png")
        self.assertEqual(html_node.props["alt"], "Alt Text")

if __name__ == "__main__":
    unittest.main()
