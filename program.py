import os
import sys

print("Select which Python file to run:")
print("1. KD-Tree")
print("2. Octree")
print("3. Range Search")
print("4. R-Tree")
print("5. Exit")

choice = input("Enter your choice: ")

if choice == '1':
    os.system('python kd_tree_main.py')

elif choice == '2':
    os.system('python octree_main.py')

elif choice == '3':
    os.system('python rangetree/rangetree.py')

elif choice == '4':
    # os.system('python r_tree_main.py')
    print("Not yet implemented.")

elif choice == '5':
    print("Exiting program.")
    sys.exit()
else:
    print("Invalid choice. Please select 1 - 5.")