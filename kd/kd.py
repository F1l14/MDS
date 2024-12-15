import pandas as pd

class KDTreeNode:
    """A node in the KD-tree."""
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kdtree(df, columns_to_index, depth=0):
    if len(df) == 0:
        return None
    
    if "review_date" in columns_to_index:
        if 'review_date_comp' not in df.columns:
            df['review_date_comp'] = pd.to_datetime(df['review_date'], format='%B %Y').dt.strftime('%Y%m').astype(int)
            columns_to_index[columns_to_index.index('review_date')] = "review_date_comp"

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

def validate_kdtree(node, columns_to_index, depth=0, min_bounds=None, max_bounds=None):
    """Validates if the given tree is a proper KD-tree."""
    if node is None:
        return True

    # Determine the axis (column index) based on the depth
    axis = depth % len(columns_to_index)
    column = columns_to_index[axis]

    # Get the current point's value for the splitting axis
    point_value = node.point[column]

    # Initialize bounds if they are None
    if min_bounds is None:
        min_bounds = [None] * len(columns_to_index)
    if max_bounds is None:
        max_bounds = [None] * len(columns_to_index)

    # Debugging output for current state
    # print(f"Depth {depth}: Validating node with point {node.point[['rating', '100g_USD', 'review_date_comp']].tolist()}")
    # print(f"    Axis {axis} - Column: '{column}', Point Value: {point_value}")
    # print(f"    Current min_bounds: {min_bounds}")
    # print(f"    Current max_bounds: {max_bounds}")

    # Check bounds for the current node
    if min_bounds[axis] is not None and point_value < min_bounds[axis]:
        print(f"    Validation failed: Point {point_value} < min_bounds[{axis}] {min_bounds[axis]}")
        return False
    if max_bounds[axis] is not None and point_value > max_bounds[axis]:
        print(f"    Validation failed: Point {point_value} > max_bounds[{axis}] {max_bounds[axis]}")
        return False

    # Set new min and max bounds for the next level
    new_min_bounds = min_bounds.copy()
    new_max_bounds = max_bounds.copy()
    
    new_min_bounds[axis] = point_value
    new_max_bounds[axis] = point_value

    # Debugging output for new bounds
    # print(f"    Updated min_bounds for next level: {new_min_bounds}")
    # print(f"    Updated max_bounds for next level: {new_max_bounds}")

    # Validate left and right subtrees with updated bounds
    left_valid = validate_kdtree(node.left, columns_to_index, depth + 1, min_bounds, new_max_bounds)
    right_valid = validate_kdtree(node.right, columns_to_index, depth + 1, new_min_bounds, max_bounds)

    return left_valid and right_valid
