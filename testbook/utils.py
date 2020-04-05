
def get_cell_index(nb, tag):
    """Get cell index from the cell tag
    
    Arguments:
        nb {dict} -- Notebook
        tag {str} -- tag
    
    Returns:
        int -- cell index
    """
    for idx, cell in enumerate(nb['cells']):
        metadata = cell['metadata']
        if "tags" in metadata and tag in metadata['tags']:
            return idx