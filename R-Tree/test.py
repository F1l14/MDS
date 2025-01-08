import math


# Define a Rectangle (Minimum Bounding Box)
class Rectangle:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def area(self):
        return (self.x_max - self.x_min) * (self.y_max - self.y_min)

    def intersect(self, other):
        """Check if two rectangles intersect"""
        return not (self.x_max < other.x_min or self.x_min > other.x_max or
                    self.y_max < other.y_min or self.y_min > other.y_max)

    def merge(self, other):
        """Return a new rectangle that bounds both rectangles"""
        return Rectangle(
            min(self.x_min, other.x_min),
            min(self.y_min, other.y_min),
            max(self.x_max, other.x_max),
            max(self.y_max, other.y_max)
        )


# Define a Node for the R-tree
class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.entries = []  # Each entry is a tuple (Rectangle, child_node or object)

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_bounds(self):
        """Returns the bounding box that covers all entries in the node"""
        bounds = None
        for rect, _ in self.entries:
            if bounds is None:
                bounds = rect
            else:
                bounds = bounds.merge(rect)
        return bounds


# Define the R-tree
class RTree:
    def __init__(self, max_entries=4, min_entries=2):
        self.max_entries = max_entries  # Maximum number of entries per node
        self.min_entries = min_entries  # Minimum number of entries per node
        self.root = Node(is_leaf=True)

    def insert(self, rect, obj):
        """Insert a new rectangle and object into the R-tree"""
        leaf = self._choose_leaf(self.root, rect)
        leaf.add_entry((rect, obj))

        # If the node exceeds the maximum entries, we need to split it
        if len(leaf.entries) > self.max_entries:
            self._split_node(leaf)

    def _choose_leaf(self, node, rect):
        """Recursively find the appropriate leaf node to insert the new rectangle"""
        if node.is_leaf:
            return node

        best_node = None
        best_increase = math.inf

        # Choose the node that will require the least increase in bounding box area
        for r, child_node in node.entries:
            increase = self._area_increase(r, rect)
            if increase < best_increase:
                best_increase = increase
                best_node = child_node

        return self._choose_leaf(best_node, rect)

    def _area_increase(self, existing_rect, new_rect):
        """Calculate the area increase when adding a new rectangle"""
        merged_rect = existing_rect.merge(new_rect)
        return merged_rect.area() - existing_rect.area()

    def _split_node(self, node):
        """Split a node into two and propagate the split upwards"""
        # Sort entries based on the area of their bounding boxes
        node.entries.sort(key=lambda entry: entry[0].area())

        # Split the node into two
        mid = len(node.entries) // 2
        left_entries = node.entries[:mid]
        right_entries = node.entries[mid:]

        left_node = Node(is_leaf=node.is_leaf)
        right_node = Node(is_leaf=node.is_leaf)

        for entry in left_entries:
            left_node.add_entry(entry)
        for entry in right_entries:
            right_node.add_entry(entry)

        # Create a new parent node if necessary
        if node == self.root:
            new_root = Node(is_leaf=False)
            new_root.add_entry((left_node.get_bounds(), left_node))
            new_root.add_entry((right_node.get_bounds(), right_node))
            self.root = new_root
        else:
            parent = self._choose_leaf(self.root, left_node.get_bounds())
            parent.add_entry((left_node.get_bounds(), left_node))
            parent.add_entry((right_node.get_bounds(), right_node))

    def query(self, rect):
        """Query the R-tree for objects that intersect with a given rectangle"""
        result = []
        self._query_node(self.root, rect, result)
        return result

    def _query_node(self, node, rect, result):
        """Recursively search the tree for intersecting rectangles"""
        if node.is_leaf:
            for r, obj in node.entries:
                if r.intersect(rect):
                    result.append(obj)
        else:
            for r, child_node in node.entries:
                if r.intersect(rect):
                    self._query_node(child_node, rect, result)


# Example of Usage:

# Create an R-tree instance
rtree = RTree(max_entries=4, min_entries=2)

# Insert some rectangles with associated objects (e.g., IDs or data)
rtree.insert(Rectangle(1, 1, 3, 3), "Object 1")
rtree.insert(Rectangle(2, 2, 4, 4), "Object 2")
rtree.insert(Rectangle(0, 0, 2, 2), "Object 3")
rtree.insert(Rectangle(5, 5, 7, 7), "Object 4")

# Query for rectangles intersecting with a given area
query_rect = Rectangle(1, 1, 3, 3)
result = rtree.query(query_rect)

print("Objects found in the query area:")
for obj in result:
    print(obj)
