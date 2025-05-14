class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_list = []
        for key, value in self.props.items():
            props_list.append(f' {key}="{value}"')
        return "".join(props_list)

    def __repr__(self):
        return (f"HTMLNode(\n"
                f"    tag={repr(self.tag)},\n"
                f"    value={repr(self.value)},\n"
                f"    children={repr(self.children)},\n"
                f"    props={repr(self.props)}\n"
                f")")
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # checks for a value
        if self.value == None:
            raise ValueError

        # checks for None value/return raw string
        if self.tag is None:
            return self.value
    
        html = f"<{self.tag}"

        # if props exist 
        if self.props:
            for prop_name, prop_value in self.props.items():
                html += f' {prop_name}="{prop_value}"'
        
        # Close opening tag, add value, and add closing tag
        html += f">{self.value}</{self.tag}>"
        
        return html


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag Missing")
        
        if self.children == None or self.children == []:
            raise ValueError("Children Missing")

        children_html_list = []

        for child in self.children:
            children_html_list.append(child.to_html())
        
        children_html = "".join(children_html_list)

        return f'<{self.tag}>{children_html}</{self.tag}>'