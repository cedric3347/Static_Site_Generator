import unittest

from extract import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        # test no images in test
    def test_multiple_images(self):
        text = "this text has no images, just [a link](https://test_example.com)"
        self.assertListEqual([], extract_markdown_images(text))

        # test extract link
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

        # test multiple links in text
    def test_multiple_links(self):
        text = "Here are multiple links: [first](https://first.com) and [second](https://second.org)"
        expected = [("first", "https://first.com"), ("second", "https://second.org")]
        self.assertListEqual(expected, extract_markdown_links(text))

        # no links in text
    def test_no_links(self):
        text = "This text has no links, just ![an image](https://example.com/image.jpg)"
        self.assertListEqual([], extract_markdown_links(text))

        # links with speccial characters in URL
    def test_links_with_speciunittestal_chars(self):
        text = "Link with query params: [search](https://example.com/search?q=python&sort=latest)"
        expected = [("search", "https://example.com/search?q=python&sort=latest")]
        self.assertListEqual(expected, extract_markdown_links(text))

        # mixed content test
    def test_mixed_content(self):
        text = "This has a [link](https://link.com) and an ![image](https://image.com/pic.jpg) mixed together"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("link", "https://link.com")], link_matches)
        self.assertListEqual([("image", "https://image.com/pic.jpg")], image_matches)

        # empty alt text and link text
    def test_empty_text(self):
        text = "Empty link text: [](https://example.com) and empty alt text: ![](https://example.com/img.jpg)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com")], link_matches)
        self.assertListEqual([("", "https://example.com/img.jpg")], image_matches)


if __name__ == "__main__":
    unittest.main()