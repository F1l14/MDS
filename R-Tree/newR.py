import pandas as pd

# ===========================================================================
def mapMonths(df):
    month_mapping = {
        'January': "1", 'February': "2", 'March': "3", 'April': "4",
        'May':"5", 'June': "6", 'July': "7", 'August': "8",
        'September': "9", 'October': "10", 'November': "11", 'December': "12"
    }
    df["month_name"] =df["review_date"].str.split(' ').str[0]
    df["year"] = df["review_date"].str.split(' ').str[1]
    df["review_date"] = df["month_name"].map(month_mapping) + df["year"]
    return df

def parseCSV(path):
    df = pd.read_csv(path)
    df = mapMonths(df)
    # print(df[["review_date", "rating","100g_USD"]].head())
    for index, row in df.iterrows():
        print(row["review_date"], row["rating"], row["100g_USD"])

# parseCSV("coffee_analysis.csv")

# ===========================================================================