from pickle import FALSE

import pandas as pd
import self


# ===========================================================================
def mapMonths(df):
    month_mapping = {
        'January': "1", 'February': "2", 'March': "3", 'April': "4",
        'May': "5", 'June': "6", 'July': "7", 'August': "8",
        'September': "9", 'October': "10", 'November': "11", 'December': "12"
    }
    df["month_name"] = df["review_date"].str.split(' ').str[0]
    df["year"] = df["review_date"].str.split(' ').str[1]
    df["review_date"] = df["year"] + df["month_name"].map(month_mapping)
    return df


def parseCSV(path):
    df = pd.read_csv(path)
    df = mapMonths(df)
    # print(df[["review_date", "rating", "100g_USD"]].head())
    for index, row in df.iterrows():
        print(row["review_date"], row["rating"], row["100g_USD"])


# PRINT CSV DATA
# parseCSV("coffee_analysis.csv")

# ===========================================================================
nodeCounter =0
class Node:
    def __init__(self, isgroup=False, members=None, mbr=None):
        global nodeCounter
        nodeCounter += 1
        self.name = nodeCounter
        self.isgroup = isgroup
        self.members = members
        # [ xmin , xmax, ymin, ymax, zmin, zmax ]
        self.mbr = mbr
        self.mbrCalc()

    def print(self):
        if self.isgroup:
            state = "Group"
        else:
            state = "Leaf"
        print("Node: " + str(self.name) + " " + state)
        print("MBR: " + str(self.mbr))
        print("Members:", end="")
        for member in self.members:
            print(" Node:"+str(member.name) + ", ", end="")
        print("\n")

    def mbrCalc(self):
        if not self.mbr:
            if self.members is not None:
                self.mbr = self.members[0].mbr

        # safety check
        if self.mbr[0] > self.mbr[1]:
            # multiple assignment swap
            self.mbr[0], self.mbr[1] = self.mbr[1], self.mbr[0]
        if self.mbr[2] > self.mbr[3]:
            self.mbr[2], self.mbr[3] = self.mbr[3], self.mbr[2]
        if self.mbr[4] > self.mbr[5]:
            self.mbr[4], self.mbr[5] = self.mbr[5], self.mbr[4]

        # mbr calculation
        for node in self.members:
            # xmin
            if (self.mbr[0] > node.mbr[0]): self.mbr[0] = node.mbr[0]
            # xmax
            if (self.mbr[1] < node.mbr[1]): self.mbr[1] = node.mbr[1]

            # ymin
            if (self.mbr[2] > node.mbr[2]): self.mbr[2] = node.mbr[2]
            # ymax
            if (self.mbr[3] < node.mbr[3]): self.mbr[3] = node.mbr[3]

            # zmin
            if (self.mbr[4] > node.mbr[4]): self.mbr[4] = node.mbr[4]
            # zmax
            if (self.mbr[5] < node.mbr[5]): self.mbr[5] = node.mbr[5]







def main():
    Node1 = Node(False, [], [1, -2, 5, 6, 3, 4])
    Node2 = Node(False, [], [5, 10, 5, 6, 3, 4])

    root = Node(True, [Node1, Node2], [1, 2, 3, 3, 3, 4])
    root.print()
    Node1.print()
    Node2.print()


if __name__ == "__main__":
    main()
