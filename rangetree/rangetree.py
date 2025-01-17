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
        self._query_primary(self.root, x_range, y_range, z_range, result)
        return result

    def _query_primary(self, node, x_range, y_range, z_range, result):
        """Helper for querying the primary tree."""
        if not node:
            return

        x_min, x_max = x_range
        if x_min <= node.points[len(node.points) // 2][0] <= x_max:
            # Query secondary tree
            result.extend(node.secondary_tree.range_query(y_range, z_range))
        
        if x_min < node.points[len(node.points) // 2][0]:
            self._query_primary(node.left, x_range, y_range, z_range, result)
        if x_max > node.points[len(node.points) // 2][0]:
            self._query_primary(node.right, x_range, y_range, z_range, result)

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

    def range_query(self, y_range, z_range):
        """Performs a 2D range query."""
        result = []
        self._query_secondary(self.root, y_range, z_range, result)
        return result

    def _query_secondary(self, node, y_range, z_range, result):
        """Helper for querying the secondary tree."""
        if not node:
            return

        y_min, y_max = y_range
        if y_min <= node.points[len(node.points) // 2][1] <= y_max:
            # Query tertiary tree
            result.extend(node.tertiary_tree.range_query(z_range))
        
        if y_min < node.points[len(node.points) // 2][1]:
            self._query_secondary(node.left, y_range, z_range, result)
        if y_max > node.points[len(node.points) // 2][1]:
            self._query_secondary(node.right, y_range, z_range, result)

class RangeTree1D:
    """1D Range Tree for the tertiary level."""
    def __init__(self, points):
        self.points = sorted(points, key=lambda p: p[2])

    def range_query(self, z_range):
        """Performs a 1D range query."""
        z_min, z_max = z_range
        return [point for point in self.points if z_min <= point[2] <= z_max]
