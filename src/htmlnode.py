class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes must implement to_html()")

    def props_to_html(self):
        if not self.props:
            return ""

        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )