import os
import sys
import pandas as pd
import time

import functions.functions as func
import kd.kd as kd
import octree.octree as octree
import rangetree.rangetree as rangetree
import RTree.r_tree as r_tree
import lsh.lsh as lsh

# Start the timer for loading
start_time_load = time.time()

# Load the dataset
file = "archive/simplified_coffee.csv"
dataset = pd.read_csv(file)

# Stop the timer for loading
end_time_load = time.time()

# Calculate the elapsed time for loading
elapsed_time_load = end_time_load - start_time_load
print(f"Time taken for loading: {elapsed_time_load} seconds.\n")

# Start the timer for preprocessing
start_time_preprocess = time.time()

# PREPROCESSING PHASE

# Convert dates into numbers
dataset['review_date'] = dataset['review_date'].apply(func.date_to_number)

# Find the min and max of the columns to be used in the indexing
min_review_date = dataset['review_date'].min()
max_review_date = dataset['review_date'].max()

min_rating = dataset['rating'].min()
max_rating = dataset['rating'].max()

min_100g_usd = dataset['100g_USD'].min()
max_100g_usd = dataset['100g_USD'].max()


# Stop the timer for preprocessing
end_time_preprocess = time.time()

# Calculate the elapsed time for preprocessing
elapsed_time_preprocess = end_time_preprocess - start_time_preprocess
print(f"Time taken for preprocessing: {elapsed_time_preprocess} seconds.\n")

tree = None

print("Select which Python file to run:")
print("1. KD-Tree")
print("2. Octree")
print("3. Range Search")
print("4. R-Tree")
print("5. Exit")

choice = input("Enter your choice: ")
start_time = time.time()
while choice not in ['1', '2', '3', '4', '5']:
    print("Invalid choice. Please select 1 - 5.")
    choice = input("Enter your choice: ")

if choice == '1':
    # KD-TREE CONSTRUCTION PHASE
    columns_to_index = ['review_date', 'rating', '100g_USD']
    tree = kd.build_kdtree(dataset, columns_to_index)

elif choice == '2':
    # Define the boundaries of the octree
    topFrontLeft = octree.Point(min_review_date, min_rating, min_100g_usd)
    botBackRight = octree.Point(max_review_date, max_rating, max_100g_usd)

    # Create the octree
    tree = octree.Octree(topFrontLeft, botBackRight)

    # Insert the dataset into the octree
    for index, row in dataset.iterrows():
        point = octree.Point(row['review_date'], row['rating'], row['100g_USD'])
        node = octree.Node(point, row)
        tree.insert(node)

elif choice == '3':
    # Extract points from the dataset
    points = [(row['review_date'], row['rating'], row['100g_USD']) for _, row in dataset.iterrows()]

    # Create the range tree
    tree = rangetree.RangeTree3D(points)

elif choice == '4':
    r_tree.build_r_tree(dataset)
    tree = r_tree

elif choice == '5':
    print("Exiting program.")
    sys.exit()
else:
    print("Invalid choice. Please select 1 - 5.")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken for tree construction: {elapsed_time} seconds.\n")

# QUERY PHASE
run_query = input("Would you like to run the query phase? (no for exit): ")
if (run_query == "no"):
    print("Exiting program.")
    sys.exit()

# Remind the user of the min and max values
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

results = None
# Start the timer for the range query
query_start_time = time.time()

if choice == '1':
    results = kd.range_search(tree, 0, columns_to_index, [min_x, min_y, min_z], [max_x, max_y, max_z])
    # Extract the data from the nodes
    query_data = [node for node in results]

    # Create a DataFrame from the query data
    query_df = pd.DataFrame(query_data)

    # Save the query results to a new CSV file
    query_df.to_csv("archive/query_output.csv", index=False)
    
elif choice == '2':
    results = tree.range_query(octree.Point(min_x, min_y, min_z), octree.Point(max_x, max_y, max_z))

    # Extract the data from the nodes
    query_data = [node.data for node in results]

    # Create a DataFrame from the query data
    query_df = pd.DataFrame(query_data)

    # Save the query results to a new CSV file
    query_df.to_csv("archive/query_output.csv", index=False)
    
elif choice == '3':
    # Perform the range query
    query_range = (min_x, max_x, min_y, max_y, min_z, max_z)
    results = tree.range_query(query_range)

    # Extract the data from the nodes
    query_data = [
        dataset.loc[(dataset['review_date'] == point[0]) &
                    (dataset['rating'] == point[1]) &
                    (dataset['100g_USD'] == point[2])]
        for point in results
    ]

    # Combine query results into a DataFrame
    query_df = pd.concat(query_data)

    # Remove duplicates
    # Keeps the first occurrence by default
    df_cleaned = query_df.drop_duplicates()

    # Save the query results to a new CSV file
    df_cleaned.to_csv("archive/query_output.csv", index=False)

elif choice == '4':
    results = tree.search([min_x, max_x, min_y, max_y, min_z, max_z], tree.root.members)
    tree.saveCSV(results)

query_end_time = time.time()
query_elapsed_time = query_end_time - query_start_time
print(f"Time taken for range query: {query_elapsed_time} seconds.\n")
print(f"Query results saved to archive/query_output.csv.\n")

# LSH PHASE OF THE QUERY

# Load the dataset
dataset = pd.read_csv("archive/query_output.csv")

run_lsh = input("Would you like to run the LSH phase of the query? (no for exit): ")
if (run_lsh == "no"):
    print("Exiting program.")
    sys.exit()

dataset['doc_id'] = dataset.index
doc_nr = dataset['doc_id'].max()
start_time = time.time()
# an array where the index i represent the document_id and the element shingling_list[i] the hashed shingles for document document_id
shingling_list = [None] * (doc_nr + 1)
shingling_size = 3 # shmantiko
signature_size = 50
bands_nr = 10

shingler_inst = lsh.shingler(shingling_size)
signer = lsh.minhashSigner(signature_size)

# produce hashed shinglings for all documents
for index, row in dataset.iterrows():
    doc = row['review']
    i = row['doc_id']

    shinglings = shingler_inst.get_hashed_shingles(shingler_inst.get_shingles(doc))
    shingling_list[i] = shinglings

end_time = time.time()
print("Shingles produced in:\t %.2f seconds." % (end_time - start_time))

start_time = time.time()
# produce a signature for each shingle set
signature_matrix = signer.compute_signature_matrix(shingling_list)
end_time = time.time()
print("Signature Matrix computed in:\t %.2f seconds." % (end_time - start_time))

# LSH time
lsh_instance = lsh.lsh(threshold= lsh.user_defined_threshold)
start_time = time.time()
lsh_similar_itemset = lsh_instance.get_similar_items(signature_matrix, bands_nr, signature_size)
end_time = time.time()
lsh_computation_time = end_time - start_time
print("LSH Similarity computed in:\t %.2f seconds.\nSimilar Elements Found: %d" %(lsh_computation_time, len(lsh_similar_itemset)))

# Jaccard Similarity for lsh similar documents
bfsc_instance = lsh.bfsc()
similarity_list = []  # List for similar

for pair in lsh_similar_itemset:
    doc1_id, doc2_id = pair
    set1 = set(shingling_list[doc1_id])
    set2 = set(shingling_list[doc2_id])

    # Jaccard Similarity with bfsc
    js = bfsc_instance.compare_shingles_set_js(set1, set2)
    similarity_list.append((doc1_id, doc2_id, js))

# Sort based on JS
similarity_list.sort(key=lambda x: x[2], reverse=True)

# User inputs N
N = int(input("Enter the number of top similar pairs to display: "))

print(f"\nTop {N} similar pairs:")
for i in range(min(N, len(similarity_list))):
    doc1_id, doc2_id, js = similarity_list[i]
    print(f"\nPair {i + 1}:")
    print("Document 1:")
    print(dataset.iloc[doc1_id])
    print("\nDocument 2:")
    print(dataset.iloc[doc2_id])
    print(f"Jaccard Similarity: {js:.4f}")


# Quality Check
compute_quality = input("\nWould you like to compute the LSH quality compared to exact Jaccard similarity? (no to exit): ").strip().lower()

if compute_quality == 'no':
    print("\nExiting program.")
    sys.exit()

print("\nComputing exact Jaccard Similarities for all document pairs (using raw reviews)...")

time1 = time.time()

exact_similarity_list_raw = []

# Jaccard Similarity for all reviews
for i in range(doc_nr + 1):
    for j in range(i + 1, doc_nr + 1):  # Reduce a few iteration loops i < j
        # split reviews
        set1 = set(dataset.iloc[i]['review'].lower().split())
        set2 = set(dataset.iloc[j]['review'].lower().split())

        # JS
        js = bfsc_instance.compare_shingles_set_js(set1, set2)
        exact_similarity_list_raw.append((i, j, js))

# Sort all documents based on JS
exact_similarity_list_raw.sort(key=lambda x: x[2], reverse=True)

time2 = time.time()

# Display N most similar
print(f"\nTop {N} similar pairs based on exact Jaccard Similarity (using raw reviews):")
for i in range(min(N, len(exact_similarity_list_raw))):
    doc1_id, doc2_id, js = exact_similarity_list_raw[i]
    print(f"\nPair {i + 1}:")
    print("Document 1:")
    print(dataset.iloc[doc1_id])
    print("\nDocument 2:")
    print(dataset.iloc[doc2_id])
    print(f"Jaccard Similarity: {js:.4f}")

total_time = time2-time1

print(f"\nTime taken to compute similarity for all documents: {total_time:.2f} seconds")

# Compare only N most similar
print("\nEvaluating the performance of LSH on displayed pairs...")

# Use only LSH N most simlar, not all
displayed_lsh_pairs = set(similarity_list[:min(N, len(similarity_list))])  
displayed_lsh_pairs = set((pair[0], pair[1]) for pair in displayed_lsh_pairs)

# Same 
displayed_exact_pairs = set(exact_similarity_list_raw[:min(N, len(exact_similarity_list_raw))]) 
displayed_exact_pairs = set((pair[0], pair[1]) for pair in displayed_exact_pairs)

# Find common pairs.
common_displayed_pairs = displayed_lsh_pairs.intersection(displayed_exact_pairs)
common_displayed_count = len(common_displayed_pairs)

# Calculate quality
quality = (common_displayed_count / len(displayed_lsh_pairs)) * 100 if displayed_lsh_pairs else 0
exact_displayed_coverage = (common_displayed_count / len(displayed_exact_pairs)) * 100 if displayed_exact_pairs else 0

# Print numbers
print(f"\nPerformance Metrics (For Displayed Pairs):")
print(f"Total pairs checking: {len(displayed_lsh_pairs)}")
print(f"Common pairs between LSH and exact method (Displayed): {common_displayed_count}")
print(f"LSH Quality (% of displayed LSH pairs found in exact method): {quality:.2f}%")
