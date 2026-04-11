import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(
            tag="p",
            value="hello",
            children=[child],
            props={"class": "text"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag='p', value='hello', children=[HTMLNode(tag='span', value='child', children=None, props=None)], props={'class': 'text'})",
        )


if __name__ == "__main__":
    unittest.main()