class KDTreeNode:
    """A node in the KD-tree."""
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kdtree(df, columns_to_index, depth=0):
    if len(df) == 0:
        return None

    # Determine the axis (column index) based on the depth
    axis = depth % len(columns_to_index)
    column = columns_to_index[axis]

    # Sort the DataFrame by the current column
    sorted_df = df.sort_values(by=column).reset_index(drop=True)
    median_idx = len(sorted_df) // 2

    # Select the median point
    median_point = sorted_df.iloc[median_idx]

    # Build the left and right subtrees recursively
    left_tree = build_kdtree(sorted_df.iloc[:median_idx], columns_to_index, depth + 1)
    right_tree = build_kdtree(sorted_df.iloc[median_idx + 1:], columns_to_index, depth + 1)

    # Return the current node
    return KDTreeNode(median_point, left_tree, right_tree)

def print_kdtree(node, depth=0):
    """Prints the KD-tree in a readable format."""
    if node is None:
        return
    indent = ' ' * (depth * 4)
    print(f"{indent}Depth {depth}: {node.point[['rating', '100g_USD', 'review_date']].tolist()}")
    print_kdtree(node.left, depth + 1)
    print_kdtree(node.right, depth + 1)