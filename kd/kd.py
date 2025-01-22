import time
import pandas as pd
import matplotlib.pyplot as plt
class KDTreeNode:
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

def range_search(node, depth, columns_to_index, min_range, max_range):
    if node is None:
        return []

    # Check if the current point is within the range
    in_range = all(min_range[i] <= node.point[columns_to_index[i]] <= max_range[i] for i in range(len(columns_to_index)))

    results = []
    if in_range:
        results.append(node.point)

    axis = depth % len(columns_to_index)
    column = columns_to_index[axis]
    point_value = node.point[column]

    # Recursively search the left and right subtrees
    if min_range[axis] <= point_value:
        results.extend(range_search(node.left, depth + 1, columns_to_index, min_range, max_range))
    if max_range[axis] >= point_value:
        results.extend(range_search(node.right, depth + 1, columns_to_index, min_range, max_range))

    return results

def plot_times(df, columns_to_index, min_range, max_range):
    construction_times = []
    search_times = []
    sizes = []

    for i in range(1, 11):
        df_expanded = pd.concat([df] * i, ignore_index=True)
        sizes.append(len(df_expanded))

        start_time = time.time()
        kdtree = build_kdtree(df_expanded, columns_to_index)
        end_time = time.time()
        construction_times.append(end_time - start_time)

        start_time = time.time()
        range_search(kdtree, 0, columns_to_index, min_range, max_range)
        end_time = time.time()
        search_times.append(end_time - start_time)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, construction_times, marker='o')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('KD-Tree Construction Time vs Dataset Size')
    plt.grid(True)
    # plt.show(block=False)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, search_times, marker='o')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Range Search Time vs Dataset Size')
    plt.grid(True)
    plt.show(block=False)