class RangeTree4D:
    def __init__(self, points):
        """
        Initializes the 4D range tree.
        points: A list of points where each point is a tuple (x, y, z, w).
        """
        self.tree = self.build_tree(points)

    def build_tree(self, points, depth=0):
        """
        Recursively builds the range tree.
        points: List of points.
        depth:  Current depth in the tree.
        """
        if not points:
            return None
        
        # Determine the dimension to split on (cycling through 4 dimensions)
        axis = depth % 4
        
        # Sort points by the current axis and find the median
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2
        median_point = points[mid]
        
        # Recursively build left and right subtrees
        return {
            'point': median_point,
            'left': self.build_tree(points[:mid], depth + 1),
            'right': self.build_tree(points[mid + 1:], depth + 1)
        }
    
    def range_query(self, node, query_range, depth=0):
        """
        Performs a range query on the tree.
        node: the root node of the previously constructed tree.
        query_range: List of ranges [(x_min, x_max), (y_min, y_max), (z_min, z_max), (w_min,w_max)].
        depth: Current depth in the tree.
        """
        if not node:
            return []
        
        axis = depth % 4
        point = node['point']
        in_range = all(query_range[i][0] <= point[i] <= query_range[i][1] for i in range(4))
        result = [point] if in_range else []
        
        # Traverse the left and right subtrees based on the current axis
        if query_range[axis][0] <= point[axis]:
            result += self.range_query(node['left'], query_range, depth + 1)
        if query_range[axis][1] >= point[axis]:
            result += self.range_query(node['right'], query_range, depth + 1)
        
        return result







# Example Usage
if __name__ == "__main__":
    # Example points: (price, rating, year, country_code)
    points = [
        (4.5, 95, 2020, 1), 
        (6.0, 96, 2021, 2), 
        (5.0, 94, 2019, 1), 
        (4.8, 97, 2020, 3),
        (7.0, 98, 2021, 1)
    ]
    
    # Build the 4D range tree
    tree = RangeTree4D(points)
    
    # Define the query range [(x_min, x_max), (y_min, y_max), (z_min, z_max), (w_min, w_max)]
    query_range = [(4.0, 6.0), (94, 96), (2019, 2021), (1, 2)]
    
    # Perform the query
    results = tree.range_query(tree.tree, query_range)
    print("Points within range:", results)