import time

class TreeNode:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None
        self.next = None  # Pointer for linked list

class BinarySearchTree:
    def __init__(self):
        self.root = None     # root node
        self.head = None     # Head of the linked list

    def insert(self, x):
        if self.root is None:
            self.root = TreeNode(x)  # Create the root if the tree is empty
        else:
            last_node = self.search(x)  # Get the last node visited during search
            '''
            if last_node.point[0] == x[0]:
                print("The value you want to insert already exists.")  # Value already exists
                return
            else:
            '''
            # Tsakalidis method
            minTuple = min(x, last_node.point, key=lambda t: t)
            maxTuple = max(x, last_node.point, key=lambda t: t)

            last_node.point = minTuple
            last_node.left = TreeNode(minTuple)
            last_node.right = TreeNode(maxTuple)  
    
    def search(self, x):
        return self._search_recursive(self.root, x)

    def search(self, x):
        return self._search_recursive(self.root, x)


    def _search_recursive(self, node, x):
        if node is None:
            return None  # If the node is None, return None
        elif x[0] <= node.point[0]:
            if node.left is None:
                return node  # If there's no left child, return current node
            return self._search_recursive(node.left, x)  # Continue searching left
        else:  # x > node.point[0]
            if node.right is None:
                return node  # If there's no right child, return current node
            return self._search_recursive(node.right, x)  # Continue searching right



    # Function to visualize the leaf-oriented tree
    def display(self, node, prefix="", is_left=True):
        if node is not None:
            # Display the right child first
            self.display(node.right, prefix + ("|   " if is_left else "    "), False)
            # Print the current node
            print(prefix + ("└── " if not is_left else "┌── ") + str(node.point))
            # Display the left child
            self.display(node.left, prefix + ("    " if is_left else "|   "), True)


    
    # Function to create a linked list of leaf nodes
    def create_leaf_linked_list(self):
        self.head = None  # Reset the linked list
        self._create_leaf_linked_list_recursive(self.root)

    def _create_leaf_linked_list_recursive(self, node):
        if node is None:
            return

        # If the node is a leaf, add it to the linked list
        if node.left is None and node.right is None:
            if self.head is None:
                self.head = node  # First leaf node
            else:
                # Find the last leaf node and append the new one
                current = self.head
                while current.next:
                    current = current.next
                current.next = node

        # Recur for left and right subtrees
        self._create_leaf_linked_list_recursive(node.left)
        self._create_leaf_linked_list_recursive(node.right)

    # Function to display the linked list of leaves
    def display_linked_list(self):
        current = self.head
        while current:
            print(current.point, end=" -> ")
            current = current.next
        print("None")


    # Function to export linked list values within a given range
    def range_search(self, lower, upper):
        current = self.head
        result = []
        
        while current:
            if lower <= current.point[0] <= upper:
                result.append(current.point)
            current = current.next
        
        return result



'''
def _search_recursive(self, node, x):
    if node is None:
        return None  # If the node is None, return None

    # Continue searching left or right based on the first value of the tuple
    if x[0] < node.point[0]:
        if node.left is None:
            return node  # Stop at the leftmost node
        return self._search_recursive(node.left, x)
    elif x[0] > node.point[0]:
        if node.right is None:
            return node  # Stop at the rightmost node
        return self._search_recursive(node.right, x)
    else:
        # If first value matches, continue down the tree to the leaf node
        if node.left is None and node.right is None:
            return node  # We've reached a leaf node
        if node.right:
            return self._search_recursive(node.right, x)  # Search right to reach the leaf
        return self._search_recursive(node.left, x)  # Continue to left if right is None
'''
