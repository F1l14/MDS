import os

print("Select which Python file to run:")
print("1. Octree")
print("2. KD-Tree")

choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    os.system('python main.py')
elif choice == '2':
    os.system('python kd_main.py')
else:
    print("Invalid choice. Please select 1 or 2.")
