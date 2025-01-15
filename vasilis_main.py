import pandas as pd
from kd import *


file = "Data/simplified_coffee.csv"

df = pd.read_csv(file)

# Convert 'review_date' to datetime format
df['review_date_comp'] = pd.to_datetime(df['review_date'], format='%B %Y').dt.strftime('%Y%m').astype(int)

columns_to_index = ['review_date_comp', 'rating', '100g_USD']

# Build the KDTree
root = build_kdtree(df, columns_to_index)

# Validate the KDTree
print(validate_kdtree(root, columns_to_index))

# Define the range for the search
min_range = [201901]
max_range = [202112]

# Perform the range search
results = range_search(root, 0, columns_to_index, min_range, max_range)

# Check if results are empty
if not results:
    print("No results found.")
else:
    # Convert results to a DataFrame for cleaner output
    results_df = pd.DataFrame(results)

    # Print the specified columns from the results
    print(results_df[['review_date', 'rating', '100g_USD']])