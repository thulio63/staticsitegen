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

def split_nodes_image(old_nodes):
    # \![alt text](image.jpg)
    new_nodes = []
    index_lists = []
    for node in old_nodes:
        all_links = extract_markdown_images(node.text) # all images found
        # indexes of brackets and parentheses put in list, appended to index_lists
        for tup in all_links:
            first = node.text.find(tup[0]) - 1
            end = node.text.find(tup[0]) + len(tup[0])
            second = node.text.find(tup[1]) - 1
            last = node.text.find(tup[1]) + len(tup[1])
            index_lists.append([first, end, second, last])
        # checks before first link to find preceding text
        preceding = node.text[:index_lists[0][0] - 1]
        if preceding != "":
            #print(f"preceding: {preceding}")
            new_nodes.append(TextNode(preceding, TextType.PLAIN))
        # adds links and text between links
        for num in range(len(index_lists)):
            new_nodes.append(TextNode(node.text[index_lists[num][0] + 1:index_lists[num][1]], TextType.IMAGE, node.text[index_lists[num][2] + 1:index_lists[num][3]]))
            # adds middle text if there are more links to come
            if num < len(index_lists) - 1:
                intermediate = node.text[index_lists[num][3]+1:index_lists[num+1][0] - 1]
                if intermediate != "":
                    new_nodes.append(TextNode(intermediate, TextType.PLAIN))
        # checks after final link to find following text
        following = node.text[index_lists[len(index_lists)-1][3]+1:]
        if following != "":
            #print(f"following: {following}")
            new_nodes.append(TextNode(following, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes):
    # [title](https://www.example.com)
    new_nodes = []
    index_lists = []
    for node in old_nodes:
        all_links = extract_markdown_links(node.text) # all links found
        # indexes of brackets and parentheses put in list, appended to index_lists
        for tup in all_links:
            first = node.text.find(tup[0]) - 1
            end = node.text.find(tup[0]) + len(tup[0])
            second = node.text.find(tup[1]) - 1
            last = node.text.find(tup[1]) + len(tup[1])
            index_lists.append([first, end, second, last])
        # checks before first link to find preceding text
        preceding = node.text[:index_lists[0][0]]
        if preceding != "":
            #print(f"preceding: {preceding}")
            new_nodes.append(TextNode(preceding, TextType.PLAIN))
        # adds links and text between links
        for num in range(len(index_lists)):
            new_nodes.append(TextNode(node.text[index_lists[num][0] + 1:index_lists[num][1]], TextType.LINK, node.text[index_lists[num][2] + 1:index_lists[num][3]]))
            # adds middle text if there are more links to come
            if num < len(index_lists) - 1:
                intermediate = node.text[index_lists[num][3]+1:index_lists[num+1][0]]
                if intermediate != "":
                    new_nodes.append(TextNode(intermediate, TextType.PLAIN))
        # checks after final link to find following text
        following = node.text[index_lists[len(index_lists)-1][3]+1:]
        if following != "":
            #print(f"following: {following}")
            new_nodes.append(TextNode(following, TextType.PLAIN))
    return new_nodes