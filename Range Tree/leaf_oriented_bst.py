'''
Πράξεις search και insert σε φυλλοπροσανατολισμενο δεντρο
σύμφωνα με τον αλγόριθμο στο βιβλίο του Τσακαλίδη (δες σελ.35)
'''


class TreeNode:
    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None


class LinkedListNode:
    def __init__(self, key=None):
        self.key = key
        self.next = None


class BinarySearchTree:
    def __init__(self):
        self.root = None     # root node
        self.head = None     # Head of the linked list
        self.current = None  # Pointer to the current node in the linked list

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
                                                                                                 