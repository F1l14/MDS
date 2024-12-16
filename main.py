import pandas as pd
import re, hashlib, math, time
from random import randint, seed
seed(1093460)

user_defined_threshold = 0.5

class hashFamily:
    def __init__(self, i):
        self.resultSize = 8  # how many bytes we want back
        self.maxLen = 20  # how long can our i be (in decimal)
        self.salt = str(i).zfill(self.maxLen)[-self.maxLen:]

    def get_hash_value(self, el_to_hash):
        return int(
            hashlib.sha1(str(el_to_hash).encode('utf-8') + self.salt.encode('utf-8')).hexdigest()[-self.resultSize:],
            16)


class shingler:
    def __init__(self, k):

        if k > 0:
            self.k = int(k)
        else:
            self.k = 10

    # inner class utility
    def process_doc(self, document):
        return re.sub("( )+|(\n)+", " ", document).lower()

    def get_shingles(self, document):
        shingles = set()
        document = self.process_doc(document)
        for i in range(0, len(document) - self.k + 1):
            shingles.add(document[i:i + self.k])
        return shingles

    def get_k(self):
        return self.k

    # return sorted hash
    def get_hashed_shingles(self, shingles_set):
        hash_function = hashFamily(0)
        return sorted({hash_function.get_hash_value(s) for s in shingles_set})


class minhashSigner:
    def __init__(self, sig_size):
        self.sig_size = sig_size
        self.hash_functions = [hashFamily(randint(0, 10000000000)) for i in range(0, sig_size)]

    def compute_set_signature(self, set_):
        set_sig = []
        for h_funct in self.hash_functions:
            min_hash = math.inf
            for el in set_:
                h = h_funct.get_hash_value(el)
                if h < min_hash:
                    min_hash = h

            set_sig.append(min_hash)

        return set_sig

    # return a list of lists that can be seen as the signature matrix
    def compute_signature_matrix(self, set_list):
        signatures = []
        for s in set_list:
            signatures.append(self.compute_set_signature(s))

        return signatures


class lsh:
    def __init__(self, threshold= user_defined_threshold):
        self.threshold = threshold

    def get_signature_matrix_bands(self, sig_matrix, bands_nr, sign_len):
        # bands_nr = b
        # sign_len = n
        r = int(sign_len / bands_nr)  # number of rows in each band
        bands = {}  # {band_nr: [col_1,col_2,...]} where col_1 is all the values of Sig(S_i) for band b.
        for i in range(0, bands_nr):
            bands[i] = []

        # put Subsets of the columns of signature matrix into the appropriate bucket and cosider a column
        # as a unique block so that we can hash the entire column.
        # Basically a band is a list of element, where each element is a subset of a signature of a given set.
        for signature in sig_matrix:

            for i in range(0, bands_nr):
                idx = i * r
                bands[i].append(' '.join(str(x) for x in signature[idx:idx + r]))

        return bands

    # band is a list
    # construct a dictionary {hash(band_column): doc_id that produced this hash}
    def get_band_buckets(self, band, hash_funct):
        buckets = {}
        for doc_id in range(0, len(band)):
            value = hash_funct.get_hash_value(band[doc_id])
            if value not in buckets:
                buckets[value] = [doc_id]
            else:
                buckets[value].append(doc_id)

        return buckets

    def get_candidates_list(self, buckets):
        candidates = set()
        # buckets is a dictionary containing key=bucket, value= list of doc_ids that hashed to bucket
        for bucket, candidate_list in buckets.items():
            if len(candidate_list) > 1:
                for i in range(0, len(candidate_list) - 1):
                    for j in range(i + 1, len(candidate_list)):
                        pair = tuple(sorted((candidate_list[i], candidate_list[j])))
                        candidates.add(pair)

        return candidates  # ie a set of couples, each couple is a candidate pair

    def check_candidates(self, candidates_list, threshold, sigs):
        similar_docs = set()  # set of tuples
        # similar_pair is a couple containing doc_ids of documents that hashed to same bucket
        for similar_pair in candidates_list:
            # for all the pairs of document in the list check similarity of their signatures
            doc_id_1 = similar_pair[0]
            doc_id_2 = similar_pair[1]
            signature_1 = set(
                sigs[doc_id_1])  # get the i-th column from signature matrix where i is doc_id in the collision list
            signature_2 = set(sigs[doc_id_2])
            js = len(signature_1.intersection(signature_2)) / len(signature_1.union(signature_2))

            if js >= threshold:
                similar_docs.add(tuple(sorted((doc_id_1, doc_id_2))))

        return similar_docs

    def get_similar_items(self, sig_matrix, bands_nr, sign_len):
        similar_docs = set()
        # divide signature matrix into bands
        bands = lsh_instance.get_signature_matrix_bands(sig_matrix, bands_nr, sign_len)

        # for all the bands
        for band_id, elements in bands.items():
            # produce the buckets for the given band (band_id) with a random hash function
            buckets = lsh_instance.get_band_buckets(elements, hash_funct=hashFamily(randint(0, 10000000000)))
            # Get all the candidate pairs
            candidates = lsh_instance.get_candidates_list(buckets)
            # Check all candidate pairs' signatures
            for sim_tuple in lsh_instance.check_candidates(candidates, self.threshold, sig_matrix):
                similar_docs.add(sim_tuple)

        return similar_docs  # return all the similar signatures that respect the threshold


class bfsc():
    def compare_shingles_set_js(self, set1, set2):
        return len(set1.intersection(set2))/len(set1.union(set2))

### MAIN ###

print("Loading dataset...")
dataset = pd.read_csv("simplified_coffee.csv", sep=",")
dataset['doc_id'] = dataset.index
doc_nr = dataset['doc_id'].max()
print("Dataset loaded correctly.")
print("Producing Shingles...")
start_time = time.time()
# an array where the index i represent the document_id and the element shingling_list[i] the hashed shingles for document document_id
shingling_list = [None] * (doc_nr + 1)
shingling_size = 3 # shmantiko
signature_size = 50
bands_nr = 10

shingler_inst = shingler(shingling_size)
signer = minhashSigner(signature_size)

# produce hashed shinglings for all documents
for index, row in dataset.iterrows():
    doc = row['review']
    i = row['doc_id']

    shinglings = shingler_inst.get_hashed_shingles(shingler_inst.get_shingles(doc))
    shingling_list[i] = shinglings

end_time = time.time()
print("Shingles produced in:\t %.2f seconds." % (end_time - start_time))

start_time = time.time()
print("Computing signature matrix...")
# produce a signature for each shingle set
signature_matrix = signer.compute_signature_matrix(shingling_list)
end_time = time.time()
print("Signature Matrix computed in:\t %.2f seconds." % (end_time - start_time))

# Υπολογισμός των υποψήφιων εγγραφών με το LSH
lsh_instance = lsh(threshold= user_defined_threshold)
start_time = time.time()
print("Computing LSH similarity...")
lsh_similar_itemset = lsh_instance.get_similar_items(signature_matrix, bands_nr, signature_size)
end_time = time.time()
lsh_computation_time = end_time - start_time
print("LSH Similarity computed in:\t %.2f seconds.\nSimilar Elements Found: %d" %(lsh_computation_time, len(lsh_similar_itemset)))

# Υπολογισμός Jaccard Similarity για όλες τις ζεύξεις
bfsc_instance = bfsc()
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