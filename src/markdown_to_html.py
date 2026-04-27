from textnode import TextNode, TextType, text_node_to_html_node
from parentnode import ParentNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [code_node])])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if line.startswith("> "):
            stripped_lines.append(line[2:])
        else:
            stripped_lines.append(line[1:])
    text = " ".join(stripped_lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[2:]
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[line.find(". ") + 2 :]
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError("invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)