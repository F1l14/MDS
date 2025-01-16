import math
from tokenize import group

groupnum = 0


def NewGroupNum():
    global groupnum
    groupnum += 1
    return groupnum


class Entity:
    def __init__(self, groups):
        self.name = NewGroupNum()
        self.groups = groups
        self.left = None
        self.right = None
        self.father = None

    def print(self):
        print("ENTITY:", self.name)
        print("\tFATHER:", self.father)
        print("\tLEFT:", self.left)
        print("\tRIGHT:", self.right)


class Node:
    def __init__(self, name, mbr):
        self.name = name
        self.mbr = mbr

    def print(self):
        print(self.name, self.mbr)


class Group:
    def __init__(self, nodes):
        self.nodes = nodes
        self.mbr = []

    def print(self):
        print(self.__class__.__name__)
        for node in self.nodes:
            node.print()
        print("MBR: ", self.mbr)

    def mbrCalc(self):
        if not self.mbr:
            self.mbr = self.nodes[0].mbr
        else:
            for node in self.nodes:
                # xmin
                if (self.mbr[0] > node.mbr[0]): self.mbr[0] = node.mbr[0]
                # ymin
                if (self.mbr[1] > node.mbr[1]): self.mbr[1] = node.mbr[1]
                # xmax
                if (self.mbr[2] < node.mbr[2]): self.mbr[2] = node.mbr[2]
                # ymax
                if (self.mbr[3] < node.mbr[3]): self.mbr[3] = node.mbr[3]


def centroidDistance(A, B):
    # Centroids
    cenA = [((A.mbr[0] + A.mbr[2])) / 2, ((A.mbr[1] + A.mbr[3])) / 2]
    cenB = [((B.mbr[0] + B.mbr[2])) / 2, ((B.mbr[1] + B.mbr[3])) / 2]
    #Euclidean Distance
    DisAB = math.sqrt((cenA[0] - cenB[0]) ** 2 + (cenA[1] - cenB[1]) ** 2)
    return [DisAB, A, B]

def generalCentroidDistance(mbrA, mbrB):
    # Centroids
    cenA = [(mbrA[0] + mbrA[2]) / 2, (mbrA[1] + mbrA[3]) / 2]
    cenB = [(mbrB[0] + mbrB[2]) / 2, (mbrB[1] + mbrB[3]) / 2]
    # Euclidean Distance
    DisAB = math.sqrt((cenA[0] - cenB[0]) ** 2 + (cenA[1] - cenB[1]) ** 2)
    return DisAB

def findIndex(list, target):
    for index, node in enumerate(list):
        if (node.name == target):
            return index


def findGroup(entity, node):
    minDistance = []
    curDistance = []
    for group in entity.groups:
        if not minDistance:
            minDistance = [generalCentroidDistance(group.mbr, node.mbr),group]
        else:
            curDistance = generalCentroidDistance(group.mbr, node.mbr)
            if minDistance[0] < curDistance:
                minDistance = [curDistance, group]
    return minDistance[1]




def insert(entity, M, node):
    # find group with least mbr expansion
    group = findGroup(entity, node)
    if len(group.nodes) < M:
        group.nodes.append(node)
        group.mbrCalc()
        return
    else:

        nodeD = []
        minD = None
        for i in range(len(group.nodes)):
            nodeD.append(centroidDistance(group.nodes[i], node))
            if minD is None:
                minD = nodeD[len(nodeD) - 1]
            elif minD[0] > nodeD[len(nodeD) - 1][0]:
                minD = nodeD[len(nodeD) - 1]





    for group in rtree:
        if len(group.nodes) < M:
            # if no nodes in group


    else:
        print("SPLIT")
        group.nodes.append(node)
        distances = []
        maxD = []
        for i in range(len(group.nodes) - 1):
            for j in range(i + 1, len(group.nodes)):
                distances.append(centroidDistance(group.nodes[i], group.nodes[j]))
                if not maxD:
                    maxD = distances[len(distances) - 1]
                elif maxD[0] < distances[len(distances) - 1][0]:
                    maxD = distances[len(distances) - 1]

        # print("distances")
        for i in range(len(distances)):
            print(distances[i][1].name, distances[i][2].name, distances[i][0])

        # print("max is: ", maxD[0], maxD[1].name, maxD[2].name)

        group.nodes.remove(maxD[1])
        group.nodes.remove(maxD[2])
        print(group.nodes)
        print(maxD)
        groupA = Group([maxD[1]])
        groupB = Group([maxD[2]])
        entity.groups.remove(group)
        entity.groups.append(groupA)
        entity.groups.append(groupB)

        for remainingNode in group.nodes:
            insert(rtree, M, remainingNode)

        return


#            ============================


def main():
M = 2
rootEntity = Entity(Group([]))

A = Node("A", [1, 1, 3, 3])
B = Node("B", [2, 2, 5, 5])
C = Node("C", [4, 4, 6, 6])
D = Node("D", [7, 1, 8, 3])

insert(rootEntity, M, A)
insert(rootEntity, M, B)
insert(rootEntity, M, C)

print("HELLO WORLD")
for entity in rtree:
    entity.print()


if __name__ == "__main__":
main()
