from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    CODE_TEXT = "italic"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"
    
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, textnode):
        if self.text != textnode.text:
            return False
        if self.text_type != textnode.text_type:
            return False
        if self.url != textnode.url:
            return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"