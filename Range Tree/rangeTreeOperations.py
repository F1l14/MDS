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
        depth: Current depth in the tree.
        """
        if not points:
            return None
        
        axis = depth % 4
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2
        median_point = points[mid]
        
        return {
            'point': median_point,
            'left': self.build_tree(points[:mid], depth + 1),
            'right': self.build_tree(points[mid + 1:], depth + 1)
        }
    
    def range_query(self, node, query_range, depth=0):
        """
        Performs a range query on the tree.
        node: Current node in the tree.
        query_range: List of ranges [(x_min, x_max), (y_min, y_max), (z_min, z_max), (w_min, w_max)].
        depth: Current depth in the tree.
        """
        if not node:
            return []
        
        axis = depth % 4
        point = node['point']
        in_range = all(query_range[i][0] <= point[i] <= query_range[i][1] for i in range(4))
        result = [point] if in_range else []
        
        if query_range[axis][0] <= point[axis]:
            result += self.range_query(node['left'], query_range, depth + 1)
        if query_range[axis][1] >= point[axis]:
            result += self.range_query(node['right'], query_range, depth + 1)
        
        return result

    def insert(self, point):
        """
        Inserts a new point into the range tree.
        point: A tuple (x, y, z, w) representing the new point.
        """
        def insert_recursive(node, depth):
            if not node:
                return {'point': point, 'left': None, 'right': None}
            
            axis = depth % 4
            if point[axis] <= node['point'][axis]:
                node['left'] = insert_recursive(node['left'], depth + 1)
            else:
                node['right'] = insert_recursive(node['right'], depth + 1)
            return node
        
        self.tree = insert_recursive(self.tree, 0)

    def delete(self, point):
        """
        Deletes a point from the range tree.
        point: A tuple (x, y, z, w) representing the point to delete.
        """
        def find_min(node, axis, depth):
            if not node:
                return None
            
            current_axis = depth % 4
            if current_axis == axis:
                if not node['left']:
                    return node
                return find_min(node['left'], axis, depth + 1)
            
            left_min = find_min(node['left'], axis, depth + 1)
            right_min = find_min(node['right'], axis, depth + 1)
            candidates = [n for n in (node, left_min, right_min) if n]
            return min(candidates, key=lambda n: n['point'][axis])

        def delete_recursive(node, depth):
            if not node:
                return None
            
            axis = depth % 4
            if node['point'] == point:
                if node['right']:
                    min_node = find_min(node['right'], axis, depth + 1)
                    node['point'] = min_node['point']
                    node['right'] = delete_recursive(node['right'], depth + 1)
                elif node['left']:
                    return node['left']
                else:
                    return None
            elif point[axis] <= node['point'][axis]:
                node['left'] = delete_recursive(node['left'], depth + 1)
            else:
                node['right'] = delete_recursive(node['right'], depth + 1)
            return node
        
        self.tree = delete_recursive(self.tree, 0)

    def update(self, old_point, new_point):
        """
        Updates a point in the range tree by deleting the old point and inserting the new one.
        old_point: The point to be updated.
        new_point: The new point to replace the old one.
        """
        self.delete(old_point)
        self.insert(new_point)







/*
# Example Usage
if __name__ == "__main__":
    points = [
        (4.5, 95, 2020, 1), 
        (6.0, 96, 2021, 2), 
        (5.0, 94, 2019, 1), 
        (4.8, 97, 2020, 3),
        (7.0, 98, 2021, 1)
    ]
    
    tree = RangeTree4D(points)
    
    # Insert a new point
    tree.insert((5.5, 96, 2020, 2))
    
    # Delete an existing point
    tree.delete((4.8, 97, 2020, 3))
    
    # Update an existing point
    tree.update((5.0, 94, 2019, 1), (4.9, 95, 2019, 1))
    
    # Perform a range query
    query_range = [(4.0, 6.0), (94, 96), (2019, 2021), (1, 2)]
    results = tree.range_query(tree.tree, query_range)
    print("Points within range:", results)
*/
