from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes: list, delimiter, text_type: TextType):
    """Splits list of nodes into new nodes using provided delimiter"""
    new_nodes = []
    adjuster = len(delimiter) - 1 # accounts for multi-char delimiters

    # call recursively on last node to ensure we don't skip text that needs to be adjusted
    for node in old_nodes:
        if delimiter in node.text and node.text_type == TextType.PLAIN:
            first_index = node.text.find(delimiter)
            second_index = node.text.find(delimiter, first_index + 1)
            back_node = TextNode(node.text, node.text_type, node.url)
            back_node.text = back_node.text[second_index + adjuster + 1:]
            mid_node = TextNode(node.text[first_index + adjuster + 1:second_index], text_type)
            node.text = node.text[:first_index]
            new_nodes.append(node)
            new_nodes.append(mid_node)
            new_nodes += split_nodes_delimiter([back_node], delimiter, text_type)
            #new_nodes.append(back_node)
        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text: str):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text: str):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes: list):
    """Splits list of nodes into new nodes surrounding md images"""
    # \![alt text](image.jpg)
    new_nodes = []
    index_lists = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            all_images = extract_markdown_images(node.text) # all images found
            if len(all_images) == 0:
                new_nodes.append(node)
                continue
            # for link in all_images:
            #     file_path = str(link[1])
            #     if file_path[0] == '/':
            #         index = all_images.index(link)
            #         new_tup = (link[0], f".{file_path}")
            #         all_images[index] = new_tup
            #         #link[1][0] = f".{link[1][0]}"
            #print(all_images)
            # indexes of brackets and parentheses put in list, appended to index_lists
            for tup in all_images:
                first = node.text.find(tup[0]) - 1
                end = node.text.find(tup[0]) + len(tup[0])
                second = node.text.find(tup[1]) - 1
                last = node.text.find(tup[1]) + len(tup[1])
                index_lists.append([first, end, second, last])
            #print(index_lists)
            # checks before first link to find preceding text
            preceding = node.text[:index_lists[0][0] - 1]
            if preceding != "":
                #print(f"preceding: {preceding}")
                new_nodes.append(TextNode(preceding, TextType.PLAIN))
            # adds links and text between links
            for num in range(len(index_lists)):
                #print(node.text[index_lists[num][0] + 1:index_lists[num][1]])
                #print(node.text[index_lists[num][2] + 1:index_lists[num][3]])
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
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes: list):
    """Splits list of nodes into new nodes surrounding md links"""
    # [title](https://www.example.com)
    new_nodes = []
    index_lists = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            all_links = extract_markdown_links(node.text) # all links found
            if len(all_links) == 0:
                new_nodes.append(node)
                continue
            #print(all_links)
            # indexes of brackets and parentheses put in list, appended to index_lists
            for tup in all_links:
                first = node.text.find(tup[0]) - 1
                end = node.text.find(tup[0]) + len(tup[0])
                # assumes correct format
                second = end + 1 #node.text.find(tup[1]) - 1
                last = second + len(tup[1]) + 1 #node.text.find(tup[1]) + len(tup[1])
                index_lists.append([first, end, second, last])
                #print(node.text[first],node.text[end],node.text[second],node.text[last])
            #print(index_lists)
            # checks before first link to find preceding text
            preceding = node.text[:index_lists[0][0]]
            if preceding != "":
                #print(f"preceding: {preceding}")
                new_nodes.append(TextNode(preceding, TextType.PLAIN))
            # adds links and text between links
            for num in range(len(index_lists)):
                #print(node.text[index_lists[num][0] + 1:index_lists[num][1]])
                #print(node.text[index_lists[num][2] + 1:index_lists[num][3]])
                new_nodes.append(TextNode(node.text[index_lists[num][0] + 1:index_lists[num][1]], TextType.LINK, node.text[index_lists[num][2] + 1:index_lists[num][3]]))
                # adds middle text if there are more links to come
                if num < len(index_lists) - 1:
                    intermediate = node.text[index_lists[num][3]+1:index_lists[num+1][0]]
                    #print(f"*{intermediate}*")
                    if intermediate != "":
                        new_nodes.append(TextNode(intermediate, TextType.PLAIN))
                # checks after final link to find following text
                elif num == len(index_lists) - 1:
                    following = node.text[index_lists[num][3]+1:]
                    #print(f"*{following}*")
                    if following != "":
                        #print(f"following: {following}")
                        new_nodes.append(TextNode(following, TextType.PLAIN))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text:str):
    """Splits text into list of nodes"""
    code_split = split_nodes_delimiter([TextNode(text, TextType.PLAIN)], "`", TextType.CODE)
    bold_split = split_nodes_delimiter(code_split, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    image_split = split_nodes_image(italic_split)
    link_split = split_nodes_link(image_split)
    return link_split

def markdown_to_blocks(markdown):
    """Splits md text into list of blocks of text"""
    list_of_blocks = markdown.split("\n\n")
    # gets rid of empty blocks
    while "" in list_of_blocks:
        list_of_blocks.remove("")
    # strips blocks
    new_list = []
    for block in list_of_blocks:
        new_list.append(block.strip())
    return new_list

def block_to_block_type(block: str):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        # sets flags
        quote = True
        unordered = True
        ordered = True
        block_lines = block.splitlines()
        for line in block_lines:
            if ordered:
                match = re.match(r'(\d\.)', line)
            # checks if lines start with '>'
            if line.startswith('>') and quote:
                unordered = False
                ordered = False
                continue
            # checks if lines start with '- '
            elif line.startswith('- ') and unordered:
                quote = False
                ordered = False
                continue
            # checks if lines start with number and period
            elif match is not None and ordered:
                unordered = False
                quote = False
                continue
            # if block does not fully meet criteria for any type
            else:
                ordered = False
                unordered = False
                quote = False
                break
        if quote:    
            return BlockType.QUOTE    
        elif unordered:    
            return BlockType.UNORDERED_LIST
        elif ordered:    
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown: str):
    #html_node = ParentNode("html") may have to do last, work bottom-up
    all_nodes = []
    blocks = markdown_to_blocks(markdown)
    #print(blocks)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING: 
                #<h#>
                children = []
                # will this fuck up with two headings on adjacent lines?
                # assuming heading isn't styled, 
                # FUCK
                heading_text = text_to_textnodes(block)
                head_type = block.count('#')
                inline_nodes = []
                for node in heading_text:
                    node.text = node.text[head_type + 1:]
                    inline_nodes.append(TextNode.text_node_to_html_node(node))
                children.append(ParentNode(f"h{head_type}", inline_nodes))
                    
                    
                heading_node = ParentNode(f"h{head_type}", children)
                all_nodes.append(heading_node)
            case BlockType.CODE:
                #<pre><code>
                # use repr here!!!!
                raw_text = fr"{block}"
                raw_text = raw_text.replace("```", "")
                code_node = LeafNode("code", raw_text)
                preformatted = ParentNode("pre", [code_node])
                all_nodes.append(preformatted)
            case BlockType.QUOTE: # revisit with method used for lists, breaking down nodes
                #<blockquote><p>
                # add cite here boyo!!!!!
                # creates list to pass to blockquote node
                children = []
                # splits md into '> ' lines
                old_lines = block.splitlines()
                # creates new list without md symbols
                lines = []
                for line in old_lines:
                    # accounts for empty line without space
                    if line == ">":
                        lines.append("")
                        continue
                    lines.append(line.replace("> ", ""))
                # remove blanks at beginning and end
                while lines[len(lines)-1] == "":
                    lines.pop()
                while lines[0] == "":
                    lines.pop(0)
                # no p breaks
                if "" not in lines:
                    text = ""
                    for lin in lines:
                        text += f"{lin} "
                    children.append(LeafNode("p", text[:-1]))
                # find p breaks and create multiple children
                else:
                    breakers = [i for i,x in enumerate(lines) if not x]
                    breakers.insert(0, 0)
                    breakers.append(len(lines))
                    for i in range(len(breakers)-1):
                        text = ""
                        for to_add in range(breakers[i], breakers[i+1]):
                            if lines[to_add] == "":
                                continue
                            text += f"{lines[to_add]} "
                        children.append(LeafNode("p", text[:-1]))
                # creates blockquote node to add to div node
                block_node = ParentNode("blockquote", children)
                all_nodes.append(block_node)
            case BlockType.UNORDERED_LIST: # does not accept indents, need to implement
                #<ul><li></li><li></li>
                # breaks list items into seperate lines, where they can be changed into nodes
                old_lines = block.splitlines()
                #print(old_lines)
                new_lines = []
                # splits by -, replaces with blanks as flags
                for line in old_lines:
                    for sub_line in line.split("- "):
                        # appends blanks for flags
                        if sub_line == "":
                            new_lines.append(sub_line)
                            continue              
                        # breaks line into nodes
                        sub_nodes = text_to_textnodes(sub_line)
                        # convert textnodes to htmlnodes
                        html_nodes = []
                        for text_node in sub_nodes:
                            html_nodes.append(TextNode.text_node_to_html_node(text_node))
                        #print(html_nodes)
                        # adds nodes to list, convert plain to text in next step
                        for node in html_nodes:
                            new_lines.append(node)
                children = []
                
                # adds blank to end of list as flag
                new_lines.append("")
                kids = []
                #print(new_lines)
                
                # skips first blank, all blanks after mark new li node
                for strip in range(1 ,len(new_lines)):
                    # encountered blank, resets kids
                    if new_lines[strip] == "":
                        children.append(ParentNode("li", kids))
                        kids = []
                    # adds node to kids
                    else:
                        kids.append(new_lines[strip])
                ul_node = ParentNode("ul", children)
                all_nodes.append(ul_node)
            case BlockType.ORDERED_LIST:
                #<ol><li></li><li></li>
                # breaks list items into seperate lines, where they can be changed into nodes
                old_lines = block.splitlines()
                #print(old_lines)
                children = []
                for line in old_lines:
                    # breaks lines apart by number
                    splits = re.split(r'(\d\.)', line)
                    #print(splits)
                    # converts text into node
                    text_node = text_to_textnodes(splits[2][1:])
                    # finds inline styling
                    if len(text_node) > 1:
                        inline_nodes = []
                        for node in text_node:
                            inline_nodes.append(TextNode.text_node_to_html_node(node))
                        
                        children.append(ParentNode("li", inline_nodes))
                        continue
                    # converts singular text node into html node
                    html_node = TextNode.text_node_to_html_node(text_node[0])
                    #print(html_node)
                    children.append(LeafNode("li", html_node.to_html()))
                #print(children)

                ol_node = ParentNode("ol", children)
                all_nodes.append(ol_node)
            case BlockType.PARAGRAPH:
                #<p>    
                edit_block = block.replace("\n", " ")     
                children = []  
                text_nodes = text_to_textnodes(edit_block)
                for node in text_nodes:
                    children.append(TextNode.text_node_to_html_node(node))
                paragraph_node = ParentNode("p", children)
                all_nodes.append(paragraph_node)
            case _:
                raise Exception("Could not find Block Type")
    parent = ParentNode("div", all_nodes)
    #print(parent)
    return parent