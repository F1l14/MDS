import time

class TreeNode:
    def __init__(self, key=None):
        self.key = key
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
            if last_node.key == x:
                print("The value you want to insert already exists.")  # Value already exists
                return
            else:
                # Tsakalidis method
                minValue = min(x, last_node.key)
                maxValue = max(x, last_node.key)

                last_node.key = minValue
                last_node.left = TreeNode(minValue)
                last_node.right = TreeNode(maxValue)  
    
    def search(self, x):
        return self._search_recursive(self.root, x)

    def _search_recursive(self, node, x):
        if node is None:
            return None  # If the node is None, return None

        elif x <= node.key:
            if node.left is None:
                return node  # If there's no left child, return current node
            return self._search_recursive(node.left, x)  # Continue searching left
        else:  # x > node.key
            if node.right is None:
                return node  # If there's no right child, return current node
            return self._search_recursive(node.right, x)  # Continue searching right

    # Function to visualize the leaf-oriented tree
    def display(self, node, prefix="", is_left=True):
        if node is not None:
            # Display the right child first
            self.display(node.right, prefix + ("|   " if is_left else "    "), False)
            # Print the current node
            print(prefix + ("└── " if not is_left else "┌── ") + str(node.key))
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
            print(current.key, end=" -> ")
            current = current.next
        print("None")


    # Function to export linked list values within a given range
    def range_search(self, lower, upper):
        current = self.head
        result = []
        
        while current:
            if lower <= current.key <= upper:
                result.append(current.key)
            current = current.next
        
        return result


# Example usage:
bst = BinarySearchTree()
bst.insert(10)
bst.insert(5)
bst.insert(20)
bst.insert(30)
bst.insert(9)
bst.insert(17)

# Display the tree structure
print("Binary Search Tree Structure:")
bst.display(bst.root)



# Start the timer 
start_time_load = time.time() 

# Create and display the linked list of leaves
bst.create_leaf_linked_list()
print("\nLinked List of Leaves:")
bst.display_linked_list()

# Export linked list values in the range [5, 17]
range_values = bst.range_search(5, 17)

# Stop the timer 
end_time_load = time.time()

# Calculate the elapsed time 
elapsed_time_load = end_time_load - start_time_load
print(f"Time taken for loading: {elapsed_time_load} seconds.\n")

# Display the result
print("\nValues in Range [5, 17]:")
print(range_values)
