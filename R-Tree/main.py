import math


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
                if(self.mbr[0] > node.mbr[0]): self.mbr[0] = node.mbr[0]
                # ymin
                if(self.mbr[1] > node.mbr[1]): self.mbr[1] = node.mbr[1]
                # xmax
                if(self.mbr[2] < node.mbr[2]): self.mbr[2] = node.mbr[2]
                # ymax
                if(self.mbr[3] < node.mbr[3]): self.mbr[3] = node.mbr[3]



def centroidDistance( A,  B):
    # Centroids
    cenA = [((A.mbr[0]+A.mbr[2]))/2, ((A.mbr[1]+A.mbr[3]))/2]
    cenB = [((B.mbr[0]+B.mbr[2]))/2, ((B.mbr[1]+B.mbr[3]))/2]
    #Euclidean Distance
    DisAB = math.sqrt((cenA[0]-cenB[0])**2 + (cenA[1]-cenB[1])**2)
    return [DisAB, A, B]

def findIndex(list, target):
    for index, node in enumerate(list):
        if(node.name == target):
            return index


def insert(rtree, M, node):
    for group in rtree:
        if len(group.nodes) < M:
            print(len(group.nodes))
            group.nodes.append(node)
            group.mbrCalc()
        else:
            print("SPLIT")
            group.nodes.append(node)
            distances = []
            maxD=[]
            for i in range(len(group.nodes)-1):
                for j in range(i+1,len(group.nodes)):
                    distances.append(centroidDistance(group.nodes[i], group.nodes[j]))
                    if not maxD:
                        maxD = distances[len(distances) - 1]
                    elif maxD[0] < distances[len(distances) - 1][0]:
                        maxD = distances[len(distances) - 1]


            print("distances")
            for i in range(len(distances)):
                print(distances[i][1].name, distances[i][2].name, distances[i][0])
            print("=============")

            print("max is: ", maxD[0], maxD[1].name, maxD[2].name)

            nodeA =maxD[1]
            nodeB =maxD[2]

            groupA = Group([nodeA])
            groupB = Group([nodeB])

            group.nodes.remove(nodeA)
            group.nodes.remove(nodeB)



            rtree.append(groupA)
            rtree.append(groupB)
            rtree.remove(group)

def main():
    print("hello world")
    M = 2
    rtree = []
    root = Group([])
    rtree.append(root)

    A = Node("A", [1, 1, 3, 3])
    B = Node("B", [2, 2, 5, 5])
    C = Node("C", [4, 4, 6, 6])
    D = Node("D", [7, 1, 8, 3])

    insert(rtree, M, A)
    insert(rtree, M, B)
    insert(rtree, M, C)
    for data in rtree:
        data.print()


if __name__ == "__main__":
    main()
