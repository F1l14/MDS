import pandas as pd
import time
import os
import functions.functions as func
import lsh.lsh as lsh
from kd import *

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

# Stop the timer for preprocessing
end_time_preprocess = time.time()

# Calculate the elapsed time for preprocessing
elapsed_time_preprocess = end_time_preprocess - start_time_preprocess
print(f"Time taken for preprocessing: {elapsed_time_preprocess} seconds.\n")

# Start the timer for KD-Tree construction
start_time_kdtree = time.time()

# KD-TREE CONSTRUCTION PHASE
columns_to_index = ['review_date', 'rating', '100g_USD']
root = build_kdtree(dataset, columns_to_index)

# Stop the timer for KD-Tree construction
end_time_kdtree = time.time()

# Calculate the elapsed time for KD-Tree construction
elapsed_time_kdtree = end_time_kdtree - start_time_kdtree
print(f"Time taken for KD-Tree construction: {elapsed_time_kdtree} seconds.\n")


# QUERY PHASE

# Remind the user of the min and max values
min_review_date = dataset['review_date'].min()
max_review_date = dataset['review_date'].max()
min_rating = dataset['rating'].min()
max_rating = dataset['rating'].max()
min_100g_usd = dataset['100g_USD'].min()
max_100g_usd = dataset['100g_USD'].max()

print(f"Review Date: min = {min_review_date}, max = {max_review_date}")
print(f"Rating: min = {min_rating}, max = {max_rating}")
print(f"100g USD: min = {min_100g_usd}, max = {max_100g_usd}.\n")

# Ask the user to define the box for the range query
min_x = int(input(f"Enter min review_date as YYYYMM (between {min_review_date} and {max_review_date}): "))
max_x = int(input(f"Enter max review_date as YYYYMM (between {min_review_date} and {max_review_date}): "))
min_y = float(input(f"Enter min rating (between {min_rating} and {max_rating}): "))
max_y = float(input(f"Enter max rating (between {min_rating} and {max_rating}): "))
min_z = float(input(f"Enter min 100g_USD (between {min_100g_usd} and {max_100g_usd}): "))
max_z = float(input(f"Enter max 100g_USD (between {min_100g_usd} and {max_100g_usd}): "))

# Start the timer for the range query
query_start_time = time.time()

# Perform the range query
min_range = [min_x, min_y, min_z]
max_range = [max_x, max_y, max_z]
range_query_result = range_search(root, 0, columns_to_index, min_range, max_range)

# Stop the timer for the range query
query_end_time = time.time()

# Extract the data from the nodes
query_data = [node for node in range_query_result]

# Create a DataFrame from the query data
query_df = pd.DataFrame(query_data)

# Save the query results to a new CSV file
query_df.to_csv("archive/query_output.csv", index=False)

# Print the nodes returned by the query
print("Nodes returned by the query:")
for node in range_query_result:
    print(node)


# LSH PHASE OF THE QUERY

# Load the dataset
dataset = pd.read_csv("archive/query_output.csv")

# Delete the file
os.remove("archive/query_output.csv")

run_lsh = input("Would you like to run the LSH phase of the query? (no for exit): ")
if (run_lsh == "no"):
    print("Exiting program.")
    exit()

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

# Υπολογισμός των υποψήφιων εγγραφών με το LSH
lsh_instance = lsh.lsh(threshold= lsh.user_defined_threshold)
start_time = time.time()
lsh_similar_itemset = lsh_instance.get_similar_items(signature_matrix, bands_nr, signature_size)
end_time = time.time()
lsh_computation_time = end_time - start_time
print("LSH Similarity computed in:\t %.2f seconds.\nSimilar Elements Found: %d" %(lsh_computation_time, len(lsh_similar_itemset)))

# Υπολογισμός Jaccard Similarity για όλες τις ζεύξεις
bfsc_instance = lsh.bfsc()
similarity_list = []  # Θα κρατήσουμε όλες τις ζεύξεις με τις αντίστοιχες τιμές Jaccard Similarity

for pair in lsh_similar_itemset:
    doc1_id, doc2_id = pair
    set1 = set(shingling_list[doc1_id])
    set2 = set(shingling_list[doc2_id])

    # Υπολογισμός Jaccard Similarity
    js = bfsc_instance.compare_shingles_set_js(set1, set2)
    similarity_list.append((doc1_id, doc2_id, js))

# Ταξινόμηση των ζεύξεων κατά φθίνουσα σειρά ομοιότητας
similarity_list.sort(key=lambda x: x[2], reverse=True)

# Ζητάμε από τον χρήστη πόσες εγγραφές θέλει να δει
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


# Ρωτάμε τον χρήστη αν θέλει να υπολογίσει το quality
compute_quality = input("\nWould you like to compute the LSH quality compared to exact Jaccard similarity? (no to exit): ").strip().lower()

if compute_quality == 'no':
    print("\nExiting program.")
    exit()

print("\nComputing exact Jaccard Similarities for all document pairs (using raw reviews)...")

time1 = time.time()

exact_similarity_list_raw = []

# Υπολογισμός Jaccard Similarity για κάθε ζεύγος εγγράφων χρησιμοποιώντας τα ίδια τα reviews
for i in range(doc_nr + 1):
    for j in range(i + 1, doc_nr + 1):  # Αποφυγή επαναλήψεων, δουλεύουμε μόνο με i < j
        # Διαχωρισμός των reviews σε μοναδικές λέξεις
        set1 = set(dataset.iloc[i]['review'].lower().split())
        set2 = set(dataset.iloc[j]['review'].lower().split())

        # Υπολογισμός Jaccard Similarity
        js = bfsc_instance.compare_shingles_set_js(set1, set2)
        exact_similarity_list_raw.append((i, j, js))

# Ταξινόμηση των ζεύξεων κατά φθίνουσα σειρά Jaccard Similarity
exact_similarity_list_raw.sort(key=lambda x: x[2], reverse=True)

time2 = time.time()

# Εμφάνιση των Ν πιο όμοιων ζεύξεων
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

# Σύγκριση μόνο για τα εκτυπωμένα ζεύγη
print("\nEvaluating the performance of LSH on displayed pairs...")

# Περιορισμός των LSH ζευγών στα κορυφαία N
displayed_lsh_pairs = set(similarity_list[:min(N, len(similarity_list))])  # Ζεύγη που εκτυπώθηκαν από το LSH (Top N ή λιγότερα)
displayed_lsh_pairs = set((pair[0], pair[1]) for pair in displayed_lsh_pairs)

# Περιορισμός των ακριβών ζευγών στα κορυφαία N
displayed_exact_pairs = set(exact_similarity_list_raw[:min(N, len(exact_similarity_list_raw))])  # Ζεύγη που εκτυπώθηκαν από την ακριβή μέθοδο
displayed_exact_pairs = set((pair[0], pair[1]) for pair in displayed_exact_pairs)

# Εύρεση κοινών ζευγών μεταξύ των δύο μεθόδων (εκτυπωμένα)
common_displayed_pairs = displayed_lsh_pairs.intersection(displayed_exact_pairs)
common_displayed_count = len(common_displayed_pairs)

# Υπολογισμός ποσοστού επικάλυψης
quality = (common_displayed_count / len(displayed_lsh_pairs)) * 100 if displayed_lsh_pairs else 0
exact_displayed_coverage = (common_displayed_count / len(displayed_exact_pairs)) * 100 if displayed_exact_pairs else 0

# Εμφάνιση αποτελεσμάτων
print(f"\nPerformance Metrics (For Displayed Pairs):")
print(f"Total pairs checking: {len(displayed_lsh_pairs)}")
print(f"Common pairs between LSH and exact method (Displayed): {common_displayed_count}")
print(f"LSH Quality (% of displayed LSH pairs found in exact method): {quality:.2f}%")
