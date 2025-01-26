# Octree implementation based on GeeksforGeeks Quadtree implementation (https://www.geeksforgeeks.org/quad-tree/)

# Point in 3D space
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Object stored in the Octree
class Node:
    def __init__(self, pos, data):
        self.pos = pos  # Point object
        self.data = data

# Main Octree Class
class Octree:
    def __init__(self, topFrontLeft, botBackRight):
        self.topFrontLeft = topFrontLeft  # Point representing the top-front-left corner
        self.botBackRight = botBackRight  # Point representing the bottom-back-right corner
        self.root = None  # Root node of the subtree
        self.children = [None] * 8  # Eight child octants

    # Insert a node into the Octree
    def insert(self, node):

        # Ignore empty nodes
        if node is None:
            return

        # Ignore out of bounds nodes
        if not self.inBoundary(node.pos):
            return

        # If the current octant has no root node, insert the node here
        if self.root is None:
            self.root = node
            return

        # Compute the midpoints of the current octant
        midX = (self.topFrontLeft.x + self.botBackRight.x) / 2
        midY = (self.topFrontLeft.y + self.botBackRight.y) / 2
        midZ = (self.topFrontLeft.z + self.botBackRight.z) / 2

        # Determine which child octant the node belongs to
        xyz = [False, False, False]
        if node.pos.x > midX: 
            xyz[0] = True
        if node.pos.y > midY:
            xyz[1] = True
        if node.pos.z > midZ:
            xyz[2] = True

        # Computes child index
        index = self.child_index(xyz)

        # Create the child octant if it doesn't exist
        if self.children[index] is None:
            newTopFrontLeft = Point(
                midX if xyz[0] else self.topFrontLeft.x,
                midY if xyz[1] else self.topFrontLeft.y,
                midZ if xyz[2] else self.topFrontLeft.z
            )
            newBotBackRight = Point(
                self.botBackRight.x if xyz[0] else midX,
                self.botBackRight.y if xyz[1] else midY,
                self.botBackRight.z if xyz[2] else midZ
            )
            self.children[index] = Octree(newTopFrontLeft, newBotBackRight)

        # Recursively insert into the correct child
        self.children[index].insert(node)

    # Check if current octant contains the point
    def inBoundary(self, p):
        return (self.topFrontLeft.x <= p.x <= self.botBackRight.x and
                self.topFrontLeft.y <= p.y <= self.botBackRight.y and
                self.topFrontLeft.z <= p.z <= self.botBackRight.z)

    # Perform a range query within the cube
    def range_query(self, top_front_left, bot_back_right):
        result = []

        # If the current octant does not overlap with the query cube, return an empty list
        if not self.overlaps(top_front_left, bot_back_right):
            return result

        # If this octant has a root, check if it's inside the query cube
        if self.root is not None:
            if (top_front_left.x <= self.root.pos.x <= bot_back_right.x and
                top_front_left.y <= self.root.pos.y <= bot_back_right.y and
                top_front_left.z <= self.root.pos.z <= bot_back_right.z):
                result.append(self.root)

        # Recursively check all child octants
        for child in self.children:
            if child:
                result.extend(child.range_query(top_front_left, bot_back_right))

        return result

    # Helper method to check if two cubes overlap
    def overlaps(self, top_front_left, bot_back_right):
        return not (self.botBackRight.x < top_front_left.x or
                    self.topFrontLeft.x > bot_back_right.x or 
                    self.botBackRight.y < top_front_left.y or
                    self.topFrontLeft.y > bot_back_right.y or
                    self.botBackRight.z < top_front_left.z or
                    self.topFrontLeft.z > bot_back_right.z)
    
    # Helper method to compute the index of the child octant
    def child_index(self, binary_array):
        # Reverse the array
        reversed_array = binary_array[::-1]
        
        # Convert the reversed array to binary digits and join them as a binary string
        binary_string = ''.join(str(int(value)) for value in reversed_array)
        
        # Convert the binary string to a decimal integer
        decimal_value = int(binary_string, 2)

        return decimal_value
