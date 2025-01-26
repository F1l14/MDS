import pandas as pd

csv_columns = None

def build_r_tree(df):
    global csv_columns
    csv_columns = df.columns
    for index, row in df.iterrows():
        # print(row["review_date"], row["rating"], row["100g_USD"])
        # if index < 50:
        root.insert(
            Node(isgroup=False, members=None,
                 mbr=[float(row["review_date"]), float(row["review_date"]), float(row["rating"]),
                      float(row["rating"]),
                      float(row["100g_USD"]), float(row["100g_USD"])], data=row)
        )


def saveCSV(data):
    results_df = pd.DataFrame(columns=csv_columns)
    for item in data:
        results_df = pd.concat([results_df, item.data.to_frame().T])
    results_df.to_csv("archive/query_output.csv", index=False)


# ===========================================================================
nodeCounter = 0


def leastExpansionGroup(groupA, groupB, newMember):
    lEG = None
    leastExpansion = float('inf')
    for node in [groupA, groupB]:
        node.calcSpace()
        tempNode = Node(isgroup=False, members=node.members + [newMember])
        tempNode.mbrCalc()
        tempNode.calcSpace()

        expansion = tempNode.space - node.space
        if expansion < leastExpansion:
            lEG = node
            leastExpansion = expansion
    if (groupA.space != 0 and groupB.space == 0):
        lEG = groupB
    return lEG


def search(search_param, members):
    def containMbr(node_mbr, search_mbr, isgroup):

        if isgroup:
            #zero to four with step two
            for i in range(0, 6, 2):
                if node_mbr[i + 1] < search_mbr[i] or search_mbr[i + 1] < node_mbr[i]:
                    return False

                    # print("ok")
            return True

        else:

            for i in range(0, 6, 2):

                if not (search_mbr[i] <= node_mbr[i] and search_mbr[i + 1] >= node_mbr[i + 1]):
                    return False

                    # print("ok")

            return True

    nodes = []
    for node in members:

        if node.isgroup:
            if containMbr(node.mbr, search_param, node.isgroup):
                nodes += search(search_param, node.members)
        elif containMbr(node.mbr, search_param, node.isgroup):
            nodes.append(node)
    return nodes


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

    def mbrCompare(self, cMbr):
        self.mbr[0] = min(self.mbr[0], cMbr[0])
        self.mbr[1] = max(self.mbr[1], cMbr[1])
        self.mbr[2] = min(self.mbr[2], cMbr[2])
        self.mbr[3] = max(self.mbr[3], cMbr[3])
        self.mbr[4] = min(self.mbr[4], cMbr[4])
        self.mbr[5] = max(self.mbr[5], cMbr[5])

    def mbrCalc(self):
        if self.isgroup:
            # Ensure MBR starts with None or reset properly
            if not self.members:
                self.mbr = None
                return

            # Initialize MBR based on the first valid member
            self.mbr = self.members[0].mbr[:]

            for member in self.members:
                if not member.mbr:
                    raise ValueError(f"Member {member.name} does not have a valid MBR.")
                for i in range(6):
                    if i % 2 == 0:  # Min bounds
                        self.mbr[i] = min(self.mbr[i], member.mbr[i])
                    else:  # Max bounds
                        self.mbr[i] = max(self.mbr[i], member.mbr[i])

    def calcSpace(self):
        if not self.mbr:
            self.space = 0
        else:
            x = self.mbr[1] - self.mbr[0]
            y = self.mbr[3] - self.mbr[2]
            z = self.mbr[5] - self.mbr[4]
            self.space = x * y * z

    def insert(self, newMember):
        if self.hasGroup:
            # Find the best child node to insert into
            current = self
            while current.hasGroup:
                current.mbrCompare(newMember.mbr)
                nextnode = leastExpansionGroup(current.members[0], current.members[1], newMember)
                if current is None:
                    print("none")
                    break
                current = nextnode
            # Insert into the chosen group
            current.insert(newMember)
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

        def mbr_distance(mbr1, mbr2):
            x_dist = max(0, mbr1[0] - mbr2[1], mbr2[0] - mbr1[1])
            y_dist = max(0, mbr1[2] - mbr2[3], mbr2[2] - mbr1[3])
            z_dist = max(0, mbr1[4] - mbr2[5], mbr2[4] - mbr1[5])
            return x_dist + y_dist + z_dist

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

        for node in remain:
            group = leastExpansionGroup(groupA, groupB, node)
            group.insert(node)


root = Node(isgroup=False)
root.name = "root"
