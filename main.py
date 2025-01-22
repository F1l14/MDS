import pandas as pd
import time
import os
from rangetree import rangetree as range_tree  # Assuming you save the above code in `range_tree_3d.py`
import functions.functions as func  # For date_to_number and get_valid_input
import lsh.lsh as lsh


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
