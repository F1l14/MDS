from pickle import FALSE
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
        if self.members and not self.mbr:
            self.mbrCalc()
        self.data = data

    def print_ascii(self, level=0):
        indent = '│   ' * level + ('├── ' if level > 0 else '')
        node_type = "Group" if self.isgroup else "Leaf"
        print(f"{indent}Node {self.name} ({node_type}) MBR: {self.mbr}")
        if self.members:
            for member in self.members:
                member.print_ascii(level + 1)

    def mbrCalcSingular(self):
        if self.members:
            for member in self.members:
                if self.mbr is None:
                    self.mbr = member.mbr[:]
                else:
                    self.mbr[0] = min(self.mbr[0], member.mbr[0])
                    self.mbr[1] = max(self.mbr[1], member.mbr[1])
                    self.mbr[2] = min(self.mbr[2], member.mbr[2])
                    self.mbr[3] = max(self.mbr[3], member.mbr[3])
                    self.mbr[4] = min(self.mbr[4], member.mbr[4])
                    self.mbr[5] = max(self.mbr[5], member.mbr[5])

    def mbrCalc(self):
        if not self.members:
            return
        self.mbr = self.members[0].mbr[:]
        for member in self.members[1:]:
            for i in range(6):
                if i % 2 == 0:  # Min bounds
                    self.mbr[i] = min(self.mbr[i], member.mbr[i])
                else:  # Max bounds
                    self.mbr[i] = max(self.mbr[i], member.mbr[i])

    # Update the insert method to fix group transformation logic
    def insert(self, newMember):
        if self.isgroup:
            # Find the best child node to insert into
            leastExpansionGroup = None
            leastExpansion = float('inf')

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

        # Step 1: Find the pair of nodes that maximizes the distance
        def mbr_distance(mbr1, mbr2):
            x_dist = max(0, mbr1[0] - mbr2[1], mbr2[0] - mbr1[1])
            y_dist = max(0, mbr1[2] - mbr2[3], mbr2[2] - mbr1[3])
            z_dist = max(0, mbr1[4] - mbr2[5], mbr2[4] - mbr1[5])
            return x_dist + y_dist + z_dist

        # Find the pair of members that maximizes the distance between their MBRs
        pairs = list(combinations(self.members, 2))
        seedA, seedB = max(pairs, key=lambda pair: mbr_distance(pair[0].mbr, pair[1].mbr))

        # Step 2: Create two new groups with the seeds
        groupA = Node(isgroup=False, members=[seedA])
        groupB = Node(isgroup=False, members=[seedB])

        # Remove seeds from the current members
        self.members.remove(seedA)
        self.members.remove(seedB)

        # Step 3: Assign remaining nodes to groups
        while self.members:
            candidate = self.members.pop()
            groupA.mbrCalc()
            groupB.mbrCalc()

            # Calculate area expansion for both groups
            groupA_with_candidate = Node(isgroup=False, members=groupA.members + [candidate])
            groupA_with_candidate.mbrCalc()
            groupA_with_candidate.calcSpace()

            groupB_with_candidate = Node(isgroup=False, members=groupB.members + [candidate])
            groupB_with_candidate.mbrCalc()
            groupB_with_candidate.calcSpace()

            # Assign candidate to the group with less area expansion
            if groupA_with_candidate.space < groupB_with_candidate.space:
                groupA.members.append(candidate)
            else:
                groupB.members.append(candidate)

        # Step 4: Update current node to become a group node
        self.isgroup = True
        self.members = [groupA, groupB]
        self.mbrCalc()

        # Ensure newly created groups are properly labeled and MBRs updated
        for group in self.members:
            group.isgroup = True
            group.mbrCalc()

    def calcSpace(self):
        if not self.mbr:
            self.space = 0
        else:
            x = self.mbr[1] - self.mbr[0]
            y = self.mbr[3] - self.mbr[2]
            z = self.mbr[5] - self.mbr[4]
            self.space = x * y * z


def main():
    start_time  = time.time()
    root = Node(isgroup=False)
    root.name = "root"

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
    # F = Node(isgroup=False, mbr=[2, 4, 5, 7, 0, 0])
    # G = Node(isgroup=False, mbr=[4, 6, 4, 6, 0, 0])
    # H = Node(isgroup=False, mbr=[5, 7, 5, 7, 0, 0])

    A.name = "A"
    B.name = "B"
    C.name = "C"
    D.name = "D"
    E.name = "E"
    # F.name = "F"
    # G.name = "G"
    # H.name = "H"

    root.insert(A)
    root.insert(B)
    root.insert(C)
    root.insert(D)
    root.insert(E)

    root.insert(D)
    root.insert(D)
    # root.insert(F)
    # root.insert(G)
    # root.insert(H)

    root.print_ascii()
    end_time = time.time()
    time_taken = end_time - start_time
    print(time_taken)
if __name__ == "__main__":
    main()

