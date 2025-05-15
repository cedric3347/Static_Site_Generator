import unittest
from markdown_inline import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


# test for split images/links
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_empty_nodes(self):
        # Test with an empty list of nodes
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)

    def test_split_image_non_text_node(self):
        # Test with a node that's not a TEXT type
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_empty_nodes(self):
        # Test with an empty list of nodes
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_split_link_non_text_node(self):
        # Test with a node that's not a TEXT type
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_link_single(self):
        # Test with a single link with no surrounding text
        node = TextNode(
            "[boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot.dev", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_split_multiple_nodes(self):
    # Test with multiple nodes in the input list
        nodes = [
            TextNode("Text with a [link](https://example.com)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More text with ![image](https://example.com/img.jpg)", TextType.TEXT)
        ]
        new_link_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("Bold text", TextType.BOLD),
                TextNode("More text with ![image](https://example.com/img.jpg)", TextType.TEXT)
            ],
            new_link_nodes
        )
        
        new_image_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text with a [link](https://example.com)", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("More text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg")
            ],
            new_image_nodes
        )
    
    def test_split_link_no_links(self):
    # Test a text node with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image_no_images(self):
        # Test a text node with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nested_formatting(self):
        # Test text with links that contain special characters
        node = TextNode(
            "Check out [**bold link**](https://example.com) and [*italic link*](https://example.org)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("**bold link**", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("*italic link*", TextType.LINK, "https://example.org")
            ],
            new_nodes
        )


# test for text_to_textnodes(text) function

    def test_text_to_textnodes_simple(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_with_formatting(self):
        text = "Text with **bold** and _italic_"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 4)
        

    def test_text_to_textnodes_with_links_and_images(self):
        # Test with the example from the assignment
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)


    def test_unmatched_delimiters(self):
        text = "This has **bold but no closing delimiter"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)
    
    def test_urls_with_special_chars(self):
        text = "[Link](https://example.com?param=value&another=test)"
        nodes = text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
