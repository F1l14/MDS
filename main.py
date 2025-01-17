import pandas as pd
import time
import os
from rangetree import rangetree as range_tree  # Assuming you save the above code in `range_tree_3d.py`
import functions.functions as func  # For date_to_number and get_valid_input

# Start the timer for loading
start_time_load = time.time()

# Load the dataset
dataset = pd.read_csv("archive/simplified_coffee.csv")

# Stop the timer for loading
end_time_load = time.time()

# Calculate the elapsed time for loading
elapsed_time_load = end_time_load - start_time_load
print(f"Time taken for loading: {elapsed_time_load} seconds.\n")

# Start the timer for preprocessing
start_time_preprocess = time.time()

# Convert dates into numbers
dataset['review_date'] = dataset['review_date'].apply(func.date_to_number)

# Stop the timer for preprocessing
end_time_preprocess = time.time()

# Calculate the elapsed time for preprocessing
elapsed_time_preprocess = end_time_preprocess - start_time_preprocess
print(f"Time taken for preprocessing: {elapsed_time_preprocess} seconds.\n")

# Start the timer for range tree construction
start_time_range_tree = time.time()

# Extract points from the dataset
points = [(row['review_date'], row['rating'], row['100g_USD']) for _, row in dataset.iterrows()]

# Create the range tree
range_tree = range_tree.RangeTree3D(points)

# Stop the timer for range tree construction
end_time_range_tree = time.time()

# Calculate the elapsed time for range tree construction
elapsed_time_range_tree = end_time_range_tree - start_time_range_tree
print(f"Time taken for range tree construction: {elapsed_time_range_tree} seconds.\n")

# Remind the user of the min and max values
min_review_date, max_review_date = dataset['review_date'].min(), dataset['review_date'].max()
min_rating, max_rating = dataset['rating'].min(), dataset['rating'].max()
min_100g_usd, max_100g_usd = dataset['100g_USD'].min(), dataset['100g_USD'].max()

print(f"Review Date: min = {min_review_date}, max = {max_review_date}")
print(f"Rating: min = {min_rating}, max = {max_rating}")
print(f"100g USD: min = {min_100g_usd}, max = {max_100g_usd}.\n")

# Ask the user to define the box for the range query
print("Define the box for the range query:")
min_x = func.get_valid_input("Enter min review_date as YYYYMM: ", min_review_date, max_review_date)
max_x = func.get_valid_input("Enter max review_date as YYYYMM: ", min_review_date, max_review_date)
min_y = func.get_valid_input("Enter min rating: ", min_rating, max_rating)
max_y = func.get_valid_input("Enter max rating: ", min_rating, max_rating)
min_z = func.get_valid_input("Enter min 100g_USD: ", min_100g_usd, max_100g_usd)
max_z = func.get_valid_input("Enter max 100g_USD: ", min_100g_usd, max_100g_usd)

# Start the timer for the range query
query_start_time = time.time()

# Perform the range query
query_range = (min_x, max_x, min_y, max_y, min_z, max_z)
query_results = range_tree.range_query(query_range)

# Stop the timer for the range query
query_end_time = time.time()

# Calculate the elapsed time for the completion of the query
elapsed_time_query = query_end_time - query_start_time
print(f"Time taken for query completion: {elapsed_time_query} seconds.\n")

# Extract the data from the nodes
query_data = [
    dataset.loc[(dataset['review_date'] == point[0]) &
                (dataset['rating'] == point[1]) &
                (dataset['100g_USD'] == point[2])]
    for point in query_results
]

# Combine query results into a DataFrame
query_df = pd.concat(query_data)

# Remove duplicates
# Keeps the first occurrence by default
df_cleaned = query_df.drop_duplicates()

# Save the query results to a new CSV file
df_cleaned.to_csv("archive/query_output.csv", index=False)

# Print the nodes returned by the query
print("Nodes returned by the query:")
for _, row in query_df.iterrows():
    print(row)
    print("\n")
