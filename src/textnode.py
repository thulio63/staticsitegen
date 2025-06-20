from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type # add delimiter here for simplified method calls?
        self.url = url
    
    def __eq__(self, textnode):
        if type(textnode) is str:
            if self.text != textnode:
                return False
        if self.text != textnode.text:
            return False
        if self.text_type != textnode.text_type:
            return False
        if self.url != textnode.url:
            return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.PLAIN:
                return LeafNode(value=text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
            case _:
                raise Exception

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    adjuster = len(delimiter) - 1 # accounts for multi-char delimiters
    for node in old_nodes:
        if delimiter in node.text:
            first_index = node.text.find(delimiter)
            second_index = node.text.find(delimiter, first_index + 1)
            back_node = TextNode(node.text, node.text_type, node.url)
            back_node.text = back_node.text[second_index + adjuster + 1:]
            mid_node = TextNode(node.text[first_index + adjuster + 1:second_index], text_type) # doesn't account for url
            node.text = node.text[:first_index]
            new_nodes.append(node)
            new_nodes.append(mid_node)
            new_nodes.append(back_node)
    
    return new_nodes

def extract_markdown_images(text):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result