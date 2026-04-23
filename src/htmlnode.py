class HTMLNode:
    def __init__(self, tag: str, value: str = "", children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    def to_html(self):
        raise NotImplementedError("not implemented yet")
    def props_to_html(self):
        if not self.props:
            return ""
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string
    def __repr__(self):
        return(f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return string
    
    def __repr__(self):
        return(f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, "", children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("The Child must have a value")
        string = f"<{self.tag}{self.props_to_html()}>"
        string2 = (child.to_html() for child in self.children)
        string += "".join(string2)
        string += f"</{self.tag}>"
        return string
