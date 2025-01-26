class Node:
    """Node for 3D Range Tree."""
    def __init__(self, points):
        self.points = points  # Points stored at this node
        self.left = None      # Left child
        self.right = None     # Right child
        self.secondary_tree = None  # Secondary tree (2D range tree)
        self.tertiary_tree = None   # Tertiary tree (1D range tree)

class RangeTree3D:
    """3D Range Tree implementation."""
    def __init__(self, points):
        self.root = self.build_primary_tree(sorted(points, key=lambda p: p[0]))

    def build_primary_tree(self, points):
        """Builds the primary tree based on x-coordinate."""
        if not points:
            return None

        mid = len(points) // 2
        root = Node(points)
        root.left = self.build_primary_tree(points[:mid])
        root.right = self.build_primary_tree(points[mid + 1:])
        root.secondary_tree = RangeTree2D(points)  # Build secondary tree
        return root

    def range_query(self, query_range):
        """Performs a 3D range query."""
        x_range, y_range, z_range = query_range[:2], query_range[2:4], query_range[4:]
        result = []
        self.query_primary(self.root, x_range, y_range, z_range, result)
        return result

    def query_primary(self, node, x_range, y_range, z_range, result):
        """Helper for querying the primary tree."""
        if not node:
            return
    
        x_min, x_max = x_range
        x_mid = node.points[len(node.points) // 2][0]
    
        if x_min <= x_mid <= x_max:
            # Query secondary tree and collect results
            node.secondary_tree.query_secondary(node.secondary_tree.root, x_range, y_range, z_range, result)
    
        if x_min < x_mid:
            self.query_primary(node.left, x_range, y_range, z_range, result)
        if x_max > x_mid:
            self.query_primary(node.right, x_range, y_range, z_range, result)


class RangeTree2D:
    """2D Range Tree for the secondary level."""
    def __init__(self, points):
        self.root = self.build_secondary_tree(sorted(points, key=lambda p: p[1]))

    def build_secondary_tree(self, points):
        """Builds the secondary tree based on y-coordinate."""
        if not points:
            return None

        mid = len(points) // 2
        root = Node(points)
        root.left = self.build_secondary_tree(points[:mid])
        root.right = self.build_secondary_tree(points[mid + 1:])
        root.tertiary_tree = RangeTree1D(points)  # Build tertiary tree
        return root

    def range_query(self, x_range, y_range, z_range):
        """Performs a 2D range query."""
        result = []
        self.query_secondary(self.root, x_range, y_range, z_range, result)
        return result

    def query_secondary(self, node, x_range, y_range, z_range, result):
        """Helper for querying the secondary tree."""
        if not node:
            return
    
        y_min, y_max = y_range
        y_mid = node.points[len(node.points) // 2][1]
    
        if y_min <= y_mid <= y_max:
            # Query tertiary tree and collect results
            node.tertiary_tree.query_tertiary(node.tertiary_tree.root, x_range, y_range, z_range, result)
    
        if y_min < y_mid:
            self.query_secondary(node.left, x_range, y_range, z_range, result)
        if y_max > y_mid:
            self.query_secondary(node.right, x_range, y_range, z_range, result)


class RangeTree1D:
    """1D Range Tree for the tertiary level (based on z-coordinate)."""
    def __init__(self, points):
        self.root = self.build_tertiary_tree(sorted(points, key=lambda p: p[2]))

    def build_tertiary_tree(self, points):
        """Builds the tertiary tree based on z-coordinate."""
        if not points:
            return None

        mid = len(points) // 2
        root = Node(points)  # Use the existing Node class
        root.left = self.build_tertiary_tree(points[:mid])
        root.right = self.build_tertiary_tree(points[mid + 1:])
        return root

    def range_query(self, x_range, y_range, z_range, result):
        """Performs a 1D range query."""
        self.query_tertiary(self.root, z_range, result)

    def query_tertiary(self, node, x_range, y_range, z_range, result):
        """Helper for querying the tertiary tree."""
        if not node:
            return

        z_min, z_max = z_range
        z_mid = node.points[len(node.points) // 2][2]

        if z_min <= z_mid <= z_max:
            # Collect points that fall within the range of every dimension
            self.collect_points(node.points, x_range, y_range, z_range, result)

        # Recursively search the left and right subtrees
        if z_min < z_mid:
            self.query_tertiary(node.left, x_range, y_range, z_range, result)
        if z_max > z_mid:
            self.query_tertiary(node.right, x_range, y_range, z_range, result)


    # Function at the tertiary level that checks the range validity for all dimensions and stores the valid points in the result[] 
    def collect_points(self, points, x_range, y_range, z_range, result):
        """Collect points that fall within the range of every dimension."""
        x_min, x_max = x_range
        y_min, y_max = y_range
        z_min, z_max = z_range
        
        for point in points:
            if x_min <= point[0] <= x_max and y_min <= point[1] <= y_max and z_min <= point[2] <= z_max:
                result.append(point)
