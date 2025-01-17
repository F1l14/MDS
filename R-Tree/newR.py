from ftplib import print_line

import pandas as pd
import time


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
    for index, row in df.iterrows():
        print(row["review_date"], row["rating"], row["100g_USD"])


# ===========================================================================
nodeCounter = 0


class Node:
    def __init__(self, isgroup=False, members=None, mbr=None, data=None):
        global nodeCounter
        nodeCounter += 1
        self.name = nodeCounter
        self.isgroup = isgroup
        self.members = members if members is not None else []
        self.maxMembers = 4
        self.space = 0
        # [ xmin, xmax, ymin, ymax, zmin, zmax ]
        self.mbr = mbr

        self.mbrCalc()
        self.data = data
        self.hasGroup = False

    def print_ascii(self, level=0):
        indent = '│   ' * level + ('├── ' if level > 0 else '')
        node_type = "Group" if self.isgroup else "Leaf"
        print(f"{indent}Node {self.name} ({node_type}) MBR: {self.mbr}")
        if self.members:
            for member in self.members:
                member.print_ascii(level + 1)

    # def mbrCalcSingular(self):
    #     # Updated for clarity and efficiency
    #     if self.members:
    #         self.mbr = [float('inf'), float('-inf'), float('inf'), float('-inf'), float('inf'), float('-inf')]
    #         for member in self.members:
    #             for i in range(6):
    #                 if i % 2 == 0:  # Min bounds
    #                     self.mbr[i] = min(self.mbr[i], member.mbr[i])
    #                 else:  # Max bounds
    #                     self.mbr[i] = max(self.mbr[i], member.mbr[i])

    def mbrCalc(self):
        if self.isgroup:
            if self.members:
                # self.mbr = [float('inf'), float('-inf'), float('inf'), float('-inf'), float('inf'), float('-inf')]
                if self.mbr is None:
                    self.mbr = self.members[0].mbr[:]

                for member in self.members:
                    for i in range(6):
                        if i % 2 == 0:  # Min bounds
                            try:
                                self.mbr[i] = min(self.mbr[i], member.mbr[i])
                            except AttributeError:
                                print(self.name, self.mbr, self.members)

                        else:  # Max bounds
                            self.mbr[i] = max(self.mbr[i], member.mbr[i])

    # Update the insert method to fix group transformation logic
    def insert(self, newMember):
        if newMember.name == "A":
            print("inserting:", newMember.name, newMember.mbr)
        if self.hasGroup:
            # Find the best child node to insert into
            leastExpansionGroup = None
            leastExpansion = float('inf')

            for node in self.members:
                if node.isgroup:
                    node.insert(newMember)
                    self.mbrCalc()
                    return
            self.calcSpace()
            for node in self.members:

                tempNode = Node(isgroup=False, members=node.members + [newMember])
                tempNode.mbrCalc()
                tempNode.calcSpace()

                expansion = tempNode.space - node.space
                if expansion < leastExpansion:
                    leastExpansionGroup = node
                    leastExpansion = expansion

            # Insert into the chosen group
            leastExpansionGroup.insert(newMember)
            self.mbrCalc()
        else:
            # Insert into the current leaf node
            if len(self.members) < self.maxMembers:
                self.members.append(newMember)
            else:
                self.members.append(newMember)
                self.quadraticSplit()
            self.mbrCalc()

    def quadraticSplit(self):
        from itertools import combinations
        # Fixed quadratic split logic
        # print("==================================")
        # self.print_ascii()

        def mbr_distance(mbr1, mbr2):
            x_dist = max(0, mbr1[0] - mbr2[1], mbr2[0] - mbr1[1])
            y_dist = max(0, mbr1[2] - mbr2[3], mbr2[2] - mbr1[3])
            z_dist = max(0, mbr1[4] - mbr2[5], mbr2[4] - mbr1[5])
            return x_dist + y_dist + z_dist


        # print("============")
        # for node in self.members:
        #     print(node.name, node.mbr)
        # print("============")

        pairs = list(combinations(self.members, 2))
        seedA, seedB = max(pairs, key=lambda pair: mbr_distance(pair[0].mbr, pair[1].mbr))

        groupA = Node(isgroup=True, members=[seedA])
        groupB = Node(isgroup=True, members=[seedB])

        self.members.remove(seedA)
        self.members.remove(seedB)
        groupA.mbrCalc()
        groupB.mbrCalc()

        remain = self.members[:]

        self.isgroup = True
        self.hasGroup = True
        self.members = [groupA, groupB]
        self.mbrCalc()
        global root
        for node in remain:
            self.insert(node)
        # self.print_ascii()
        # print("==================================")

    def calcSpace(self):
        if not self.mbr:
            self.space = 0
        else:
            x = self.mbr[1] - self.mbr[0]
            y = self.mbr[3] - self.mbr[2]
            z = self.mbr[5] - self.mbr[4]
            self.space = x * y * z

    def search(self, search_param):
        def containMbr(node_mbr, search_mbr, isgroup):
            # print("search: ", search_mbr)
            # print("current: ", node_mbr)
            if isgroup:
                for i in range(0, 4, 2):
                    if node_mbr[i+1] < search_mbr[i] or search_mbr[i+1] < node_mbr[i]:
                        return False
                    else:
                        print("ok")
                        return True

            else:

                for i in range(0, 4, 2):

                    if search_mbr[i] > node_mbr[i] or search_param[i + 1] < node_mbr[i + 1]:
                        return False
                    else:
                        print("ok")
                        return True

        nodes = []
        for node in self.members:
            print("checking: ", node.name, search_param, node.mbr, node.isgroup)
            if node.isgroup:
                if containMbr(node.mbr, search_param, node.isgroup):
                    nodes += node.search(search_param)
            elif containMbr(node.mbr, search_param, node.isgroup):
                nodes.append(node)
        # print("nodes: ", len(nodes))
        # for node in nodes:
        #     print(node.name)
        return nodes


root = Node(isgroup=False)
root.name = "root"


def main():
    start_time = time.time()

    # A = Node(isgroup=False, mbr=[1, 3, 1, 3, 1, 3])
    # B = Node(isgroup=False, mbr=[2, 4, 2, 4, 2, 4])
    # C = Node(isgroup=False, mbr=[3, 5, 1, 3, 1, 3])
    # D = Node(isgroup=False, mbr=[6, 8, 1, 3, 1, 3])
    # E = Node(isgroup=False, mbr=[1, 3, 4, 6, 1, 3])
    # F = Node(isgroup=False, mbr=[2, 4, 5, 7, 2, 4])
    # G = Node(isgroup=False, mbr=[4, 6, 4, 6, 1, 3])
    # H = Node(isgroup=False, mbr=[5, 7, 5, 7, 2, 4])

    A = Node(isgroup=False, mbr=[1, 1, 3, 3, 10, 10])
    B = Node(isgroup=False, mbr=[2, 2, 4, 4, 1, 1])
    C = Node(isgroup=False, mbr=[5, 5, 1, 1, 0, 0])
    D = Node(isgroup=False, mbr=[6, 6, 1, 1, 2, 2])
    E = Node(isgroup=False, mbr=[8, 8, 4, 4, 2, 2])
    F = Node(isgroup=False, mbr=[2, 4, 5, 7, 0, 0])
    G = Node(isgroup=False, mbr=[4, 6, 4, 6, 0, 0])
    H = Node(isgroup=False, mbr=[5, 7, 5, 7, 0, 0])

    A.name = "A"
    B.name = "B"
    C.name = "C"
    D.name = "D"
    E.name = "E"
    F.name = "F"
    G.name = "G"
    H.name = "H"

    node_list = [A, B, C, D, E, F, G, H]
    for node in node_list:
        root.insert(node)
        # print("INSERTING: ", node.name, node.mbr)
        # root.print_ascii()
        # print("========================================")
    root.insert(D)
    root.print_ascii()
    end_time = time.time()
    time_taken = end_time - start_time
    print(time_taken)

    searchTime = time.time()
    result = root.search([1, 8, 1, 7, 0, 10])
    searchTimeEnd = time.time()
    searchFinal = searchTime - searchTimeEnd

    print("SEARCH TIME: ", searchFinal)
    print("search results: ")
    for item in result:
        print(str(item.name) + ", ", end="")


if __name__ == "__main__":
    main()
