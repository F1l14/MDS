import time
import pandas as pd
from lsh import shingler, minhashSigner, lsh  # Import the required classes

# Load CSV
df = pd.read_csv('archive/simplified_coffee.csv')

# Initialize Parameters
k = 3  # Shingle length
sig_size = 50  # Number of hash functions
bands_nr = 20  # Number of bands
threshold = 0.3  # Similarity threshold


# Start the timer
start_time = time.time()


# Step 1: Create Shingler and MinHashSigner
shingler_instance = shingler(k)
minhash_instance = minhashSigner(sig_size)

# Step 2: Process documents into shingles
shingles_list = []
for review in df['review']:
    shingles_list.append(shingler_instance.get_shingles(review))

# Step 3: Compute MinHash signatures
signatures = minhash_instance.compute_signature_matrix(shingles_list)

# Step 4: Apply LSH to find similar documents
lsh_instance = lsh(threshold)
similar_recs = lsh_instance.get_similar_items(signatures, bands_nr, sig_size)


# Stop the timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time


# Step 5: Print Results
print("Similar Records:")
for rec1, rec2 in similar_recs:
    print(f"Record {rec1+1} and Record {rec2+1}")


print(f"\nTime taken for the entire process: {elapsed_time:.2f} seconds")
