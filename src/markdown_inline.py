from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid Markdown, formatted section not closed")
            for index in range(len(sections)):
                if index % 2 == 0:
                    # at a text node index
                    if index == len(sections) - 1 and sections[index] == "":
                        # last index, and it's empty so it is skipped
                        continue
                    split_nodes.append(TextNode(sections[index], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(sections[index], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes