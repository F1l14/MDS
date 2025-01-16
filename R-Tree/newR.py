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
nodeCounter = 0


class Node:
    def __init__(self, isgroup=False, members=None, mbr=None):
        global nodeCounter
        nodeCounter += 1
        self.name = nodeCounter
        self.isgroup = isgroup
        self.members = members
        self.maxMembers = 4
        # [ xmin , xmax, ymin, ymax, zmin, zmax ]
        self.mbr = mbr
        if self.members is not None and self.mbr is None:
            self.mbrCalc()

        # used for quadratic split
        self.space = None

    def print(self):
        if self.isgroup:
            state = "Group"
        else:
            state = "Leaf"

        print("Node: ", str(self.name), state)
        print("MBR: ", end="")
        if self.mbr is not None:
            print(self.mbr, end="")
        print(" ")
        print("Members: ", end="")
        if self.members is not None:
            for member in self.members:
                print(str(member.name) + ", ", end="")
        print(" ")

    def printWhole(self):
        self.print()
        if self.isgroup:
            if self.members is not None:
                for member in self.members:
                    member.printWhole()




    def mbrCalcSingular(self):
        if self.members is not None:
            last_member = self.members[-1]
            if self.mbr is None:
                self.mbr = last_member.mbr
            else:
                # xmin
                if self.mbr[0] > last_member.mbr[0]:
                    self.mbr[0] = last_member.mbr[0]
                # xmax
                if self.mbr[1] < last_member.mbr[1]:
                    self.mbr[1] = last_member.mbr[1]

                # ymin
                if self.mbr[2] > last_member.mbr[2]:
                    self.mbr[2] = last_member.mbr[2]
                # ymax
                if self.mbr[3] < last_member.mbr[3]:
                    self.mbr[3] = last_member.mbr[3]

                # zmin
                if self.mbr[4] > last_member.mbr[4]:
                    self.mbr[4] = last_member.mbr[4]
                # zmax
                if self.mbr[5] < last_member.mbr[5]:
                    self.mbr[5] = last_member.mbr[5]

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
            if self.mbr[0] > node.mbr[0]:
                self.mbr[0] = node.mbr[0]
            # xmax
            if self.mbr[1] < node.mbr[1]:
                self.mbr[1] = node.mbr[1]

            # ymin
            if self.mbr[2] > node.mbr[2]:
                self.mbr[2] = node.mbr[2]
            # ymax
            if self.mbr[3] < node.mbr[3]:
                self.mbr[3] = node.mbr[3]

            # zmin
            if self.mbr[4] > node.mbr[4]:
                self.mbr[4] = node.mbr[4]
            # zmax
            if self.mbr[5] < node.mbr[5]:
                self.mbr[5] = node.mbr[5]

    def insert(self, newMember):
        if self.isgroup:
            leastExpansionGroup = None
            lestExpansion = 0

            for node in self.members:
                x, y, z = 0, 0, 0
                # x axis
                if newMember.mbr[0] < node.mbr[0]:
                    x += node.mbr[0] - newMember.mbr[0]
                if newMember.mbr[1] > node.mbr[1]:
                    x += newMember.mbr[1] - node.mbr[1]
                # y axis
                if newMember.mbr[2] < node.mbr[2]:
                    y += node.mbr[2] - newMember.mbr[2]
                if newMember.mbr[3] > node.mbr[3]:
                    y += newMember.mbr[3] - node.mbr[3]
                # z axis
                if newMember.mbr[4] < node.mbr[4]:
                    z += node.mbr[4] - newMember.mbr[4]
                if newMember.mbr[5] > node.mbr[5]:
                    z += newMember.mbr[5] - node.mbr[5]
                currentExpansion = x + y + z

                if leastExpansionGroup is None:
                    leastExpansionGroup = node
                    lestExpansion = currentExpansion
                elif currentExpansion < lestExpansion:
                    leastExpansionGroup = node
                    lestExpansion = currentExpansion
            leastExpansionGroup.members.append(newMember)
            leastExpansionGroup.mbrCalcSingular()

        elif self.members is None:
            self.members = [newMember]
            self.mbrCalcSingular()
        elif len(self.members) < self.maxMembers:
            self.members.append(newMember)
            self.mbrCalcSingular()
        else:
            print("SPLIT")
            self.quadraticSplit()

    def calcSpace(self):
        x = self.mbr[1] - self.mbr[0]
        y = self.mbr[3] - self.mbr[2]
        z = self.mbr[5] - self.mbr[4]
        self.space = x * y * z

    def quadraticSplit(self):
        tempNodes = []
        maxPair = None
        for i in range(len(self.members) - 2):
            temp = Node(isgroup=False, members=[self.members[i], self.members[i + 1]])
            temp.calcSpace()
            tempNodes.append(temp)
        for node in tempNodes:
            node.calcSpace()
            if maxPair is None:
                maxPair = node
            elif maxPair.space < node.space:
                maxPair = node
        splitA = Node(isgroup=False, members=[maxPair.members[0]])
        splitA.name = maxPair.members[0].name
        splitB = Node(isgroup=False, members=[maxPair.members[1]])
        splitB.name = maxPair.members[1].name
        self.members.remove(maxPair.members[0])
        self.members.remove(maxPair.members[1])
        self.isgroup = True
        remain = self.members
        self.members = []
        self.members.append(splitA)
        self.members.append(splitB)
        for node in remain:
            self.insert(node)


def printlines():
    print("\n=============================\n")


def main():
    # Node1 = Node(False, [], [1, -2, 5, 6, 3, 4])
    # Node2 = Node(False, [], [5, 10, 5, 6, 3, 4])
    #
    # root = Node(True, [Node1, Node2], [1, 2, 3, 3, 3, 4])
    # root.print()
    #
    # Node3 = Node(False, [], [5, 10, 5, 6, 1, 11])
    # root.insert(Node3)
    # root.print()

    root = Node(isgroup=False)
    root.name = "root"

    A = Node(isgroup=False, mbr=[1, 3, 1, 3, 1, 3, ])
    B = Node(isgroup=False, mbr=[2, 4, 2, 4, 2, 4, ])
    C = Node(isgroup=False, mbr=[3, 5, 1, 3, 1, 3, ])
    D = Node(isgroup=False, mbr=[6, 8, 1, 3, 1, 3, ])
    E = Node(isgroup=False, mbr=[1, 3, 4, 6, 1, 3, ])
    F = Node(isgroup=False, mbr=[2, 4, 5, 7, 2, 4, ])
    G = Node(isgroup=False, mbr=[4, 6, 4, 6, 1, 3, ])
    H = Node(isgroup=False, mbr=[5, 7, 5, 7, 2, 4, ])


    A.name = "A"
    B.name = "B"
    C.name = "C"
    D.name = "D"
    E.name = "E"
    F.name = "F"
    G.name = "G"
    H.name = "H"

    root.insert(A)
    # root.print()
    # printlines()
    root.insert(B)
    # root.print()
    # printlines()
    root.insert(C)
    # root.print()
    # printlines()
    root.insert(D)
    # root.print()
    # printlines()
    root.insert(E)
    root.printWhole()
    printlines()
    # root.insert(F)
    # root.print()
    # printlines()
    # root.insert(G)
    # root.print()
    # printlines()
    # root.insert(H)
    # root.print()
    # printlines()


if __name__ == "__main__":
    main()
