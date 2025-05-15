


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    
    for block in blocks:
        stripped = block.strip()
        if stripped:
            clean_blocks.append(stripped)
    
    return clean_blocks