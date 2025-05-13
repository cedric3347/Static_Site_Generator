import unittest

from textnode import TextNode, TextType


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
        node1 = TextNode("this is not the same", TextType.NORMAL)
        node2 = TextNode("this is not the same", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    # test url cases
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


if __name__ == "__main__":
    unittest.main()
