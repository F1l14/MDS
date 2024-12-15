import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'kd'))

from kd import *


import pandas as pd

file = "Data/simplified_coffee.csv"

df = pd.read_csv(file)

# Convert 'review_date' to datetime format
# df['review_date_comp'] = pd.to_datetime(df['review_date'], format='%B %Y').dt.strftime('%Y%m').astype(int)

# Convert the date to a timestamp (number of seconds since epoch)
# df['review_date_comp'] = pd.to_datetime(df['review_date']).apply(lambda x: int(x.timestamp()))

# One-hot encode the 'country' column
# df = pd.get_dummies(df, columns=['origin'], drop_first=True)


columns_to_index = ['rating', '100g_USD', 'review_date']

# Build the KDTree
root = build_kdtree(df, columns_to_index)

# print_kdtree(root)

print(validate_kdtree(root, columns_to_index))