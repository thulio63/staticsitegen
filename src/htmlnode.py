class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""
        for key in list(self.props.keys()):
            string += f" {key}=\"{self.props[key]}\""
        return string
    
    
class ParentNode(HTMLNode):
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag found")
        if self.children is None or self.children == []:
            raise ValueError("No children found")
        child_text = ""
        for kid in self.children:
            child_text += kid.to_html()
        return f"<{self.tag}>{child_text}</{self.tag}>"
    
class LeafNode(HTMLNode):
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value)
        self.tag = tag
        self.props = props
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        propstring = ""
        if isinstance(self.props, dict):
            propstring = self.props_to_html()
        
        string = f"<{self.tag}{propstring}>{self.value}</{self.tag}>"
        return string
    
    def props_to_html(self):
        return super().props_to_html()