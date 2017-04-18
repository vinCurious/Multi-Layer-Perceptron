"""
Filename: trainDT.py
author: Ameya Nayak, Vinay More, Saurabh Wani
"""


import collections
import math
import sys
import matplotlib.pylab as plt

#import matplotlib.pylab as plt

class Node:
    #initialize
    def __init__(self, freq):
        self.left = None
        self.right = None
        self.attribute = -1
        self.threshold = -1
        self.isLeaf = False
        self.decision = None
        self.freq = freq
        self.leftSamples = []
        self.rightSamples = []
        self.chi = 0
        self.chiPruned = False

    def makeLeaf(self,decision):
        self.isLeaf = True
        self.decision = decision

    #set chi squared value
    def chis(self,chi):
        self.chi = chi

    #add left child
    def addLeft(self,left):
        self.left = left
        
    #add right child
    def addRight(self,right):
        self.right = right

    #add split attribute and threshold
    def addThreshold(self, attribute, threshold):
        self.attribute = attribute
        self.threshold = threshold
        
    #write nodes to a file
    def printNode(self, m):
        m.write("\nAttribute = " + str(self.attribute))
        m.write("\nThreshold = " + str(self.threshold))
        m.write("\nLeaf =" + str(self.isLeaf))
        m.write("\nDecision = " + str(self.decision))
        if self.isLeaf == False:
            m.write("\nRight of "+ str(self.attribute) + " = " + str(self.threshold))
            self.right.printNode(m)
            m.write("\nLeft of" + str(self.attribute) + " = " + str(self.threshold))
            self.left.printNode(m)

    #prunes decision tree
    def pruneTree(self):
        if(self.chi<=7.815):
            self.makeLeaf(max(self.freq, key=self.freq.get))
        if self.right!=None:
            self.right.pruneTree()
        if self.left!=None:
            self.left.pruneTree()

    #classifies the given sample
    def getDecision(self,test):
        if self.isLeaf:
            return self.decision
        else:
            if test[self.attribute] > self.threshold:
                return self.right.getDecision(test)
            else:
                return self.left.getDecision(test)

    #returns min depth
    def minDepth(self):
        if self.isLeaf == True:
            return 0
        else:
            return min(1 + self.left.minDepth(), 1 + self.right.minDepth())
    #returns max depth
    def maxDepth(self):
        if self.isLeaf == True:
            return 0
        else:
            return max(1 + self.left.maxDepth(), 1 + self.right.maxDepth())

    #returns avg depth
    def avgDepth(self):
        if self.isLeaf == True:
            return 0
        else:
            return 1 + self.left.avgDepth() + 1 + self.right.avgDepth()

    #return count of leaves
    def count_leaves(self):
        count = 0
        if self.isLeaf != False :
            count += 1
        else:
            count += self.left.count_leaves()
            count += self.right.count_leaves()

        return count

    #return count of nodes
    def count_nodes(self):
        count = 0
        count += 1
        if self.isLeaf == False:
            count += self.left.count_nodes()
            count += self.right.count_nodes()
        return count

#Main function which takes in a training file annd prints the required statements
def main():
    # Read file
    f = open(sys.argv[1], 'rt')
    inData = {}
    for row in f:
        if len(row) > 1:
            row = row.split(",")
            inData.update({row[0]: [row[1], row[2]]})
    sortData = collections.OrderedDict(sorted(inData.items()))
    sortdataList = []
    for data in sortData:
        sortdataList.append([float(data),float(sortData[data][0]), int(sortData[data][1])])
    x = buildtree(sortdataList, "none")
    print("*************************Before Pruning************************************")
    print("Leaf count = ",x.count_leaves())
    print("Node count = ", x.count_nodes())
    print("Min Depth = " ,x.minDepth())
    print("Max Depth = ", x.maxDepth())
    print("Avg depth = ", x.avgDepth() / x.count_leaves())

    m = open("BPtree1.txt", 'w')
    x.printNode(m)
    m.close()
    n = open("APtree1.txt", 'w')

    x.pruneTree()
    x.printNode(n)
    n.close
    print("*************************After Pruning************************************")
    print("Leaf count = " , x.count_leaves())
    print("Node count = ", x.count_nodes())
    print("Min Depth = ", x.minDepth())
    print("Max Depth = ", x.maxDepth())
    print("Avg depth = ", x.avgDepth() / x.count_leaves())

# builds decision tree
def buildtree(samples, root):
    #node = Node()
    inData = {}
    freq = {1:0,2:0,3:0,4:0}
    # Store every instance
    for i in samples:
        x = freq[int(i[2])]
        freq[int(i[2])] = x + 1
        inData.update({i[0]: [i[1], i[2]]})
    count = 0
    leaf = 5
    for data in freq:
        if freq[data] == 0:
            count += 1
        else:
            leaf = data
    node = Node(freq)

    if count > 2 :
        node.makeLeaf(leaf)
        return node

    count = len(inData.keys())
    sortData = collections.OrderedDict(sorted(inData.items()))
    xsplit = []
    ysplit = []
    freq1 = 0 if freq[1] == 0 else math.log((freq[1] / count), 2)
    freq2 = 0 if freq[2] == 0 else math.log((freq[2] / count), 2)
    freq3 = 0 if freq[3] == 0 else math.log((freq[3] / count), 2)
    freq4 = 0 if freq[4] == 0 else math.log((freq[4] / count), 2)
    s = -((freq[1] / count) * freq1) - ((freq[2] / count) * freq2) - ((freq[3] / count) * freq3) - ((freq[4] / count) * freq4)
    sortdataList = []

    for data in sortData:
        sortdataList.append([float(data), float(sortData[data][0]), int(sortData[data][1])])
    for i in range(len(sortdataList) - 1):
        xsplit.append((sortdataList[i][0] + sortdataList[i + 1][0]) / 2)
        ysplit.append((sortdataList[i][1] + sortdataList[i + 1][1]) / 2)
    entropyx = {}
    entropyy = {}
    for i in xsplit:
        countleft = [0, 0, 0, 0]
        countright = [0, 0, 0, 0]
        for x in sortdataList:
            if x[0] < i:
                countleft[x[2] - 1] += 1
            else:
                countright[x[2] - 1] += 1
        entropyx[i] = calcEntropy(countleft, countright)
    for i in ysplit:
        countleft = [0, 0, 0, 0]
        countright = [0, 0, 0, 0]
        for x in sortdataList:
            if x[1] < i:
                countleft[x[2] - 1] += 1
            else:
                countright[x[2] - 1] += 1
        entropyy[i] = calcEntropy(countleft, countright)

    minX = min(entropyx, key=entropyx.get)
    minXEntropy = entropyx[minX]
    minY = min(entropyy, key=entropyy.get)
    minYEntropy = entropyy[minY]
    left = []
    right = []
    newRoot = ""
    if (minYEntropy < minXEntropy):
        node.addThreshold(1, minY)
        newRoot = "Y = " + str(minY)
        for data in sortdataList:
            if data[1] <= minY:
                left.append(data)
            else:
                right.append(data)
    else:
        newRoot = "X = "  + str(minX)
        node.addThreshold(0, minX)
        for data in sortdataList:
            if data[0] < minX:
                left.append(data)
            else:
                right.append(data)

    plotDataset(left, right)
    chi = calcChiSquare(left, right)
    node.chis(chi)
    node.addRight(buildtree(right,newRoot))
    node.addLeft(buildtree(left,newRoot))
    return node


# calculates entropy
def calcEntropy(countleft,countright):
    for i in range(len(countleft)):
        left1 = 0 if countleft[0] == 0 else math.log(countleft[0]/sum(countleft), 2)
        left2 = 0 if countleft[1] == 0 else math.log(countleft[1] / sum(countleft), 2)
        left3 = 0 if countleft[2] == 0 else math.log(countleft[2] / sum(countleft), 2)
        left4 = 0 if countleft[3] == 0 else math.log(countleft[3] / sum(countleft), 2)
        right1 = 0 if countright[0] == 0 else math.log(countright[0] / sum(countright), 2)
        right2 = 0 if countright[1] == 0 else math.log(countright[1] / sum(countright), 2)
        right3 = 0 if countright[2] == 0 else math.log(countright[2] / sum(countright), 2)
        right4 = 0 if countright[3] == 0 else math.log(countright[3] / sum(countright), 2)

    left = -(countleft[0]/sum(countleft) * left1) - (countleft[1]/sum(countleft) * left2)-(countleft[2]/sum(countleft) * left3) - (countleft[3]/sum(countleft)* left4)
    right = -(countright[0]/sum(countright) * right1) - (countright[1]/sum(countright)* right2 )-(countright[2]/sum(countright) * right3) - (countright[3]/sum(countright)* right4)
    return left + right

#calculates chi square
def calcChiSquare(left, right):
    sum = 0;
    freq1 = {1:0,2:0,3:0,4:0}
    freq2 = {1:0,2:0,3:0,4:0}
    # Store every instance
    for i in left:
        x = freq1[int(i[2])]
        freq1[int(i[2])] = x + 1
    for i in right:
        x = freq2[int(i[2])]
        freq2[int(i[2])] = x + 1
    total = len(left) + len(right)
    for a in range(4):
        i = 1 + a
        if freq1[i] + freq2[i] != 0:
            sum += (freq1[i] - ((freq1[i] + freq2[i]) * (len(left) / total))) ** 2 / (
            (freq1[i] + freq2[i]) * (len(left) / total))
            sum += (freq2[i] - ((freq1[i] + freq2[i]) * (len(right) / total))) ** 2 / (
            (freq1[i] + freq2[i]) * (len(right) / total))
    return sum

# def plotDataset(left, right):
#
#     for i in range(left):
#         # for j in range(len[i]):
#         #     if(j[2] == 1):
#         #         plt.plot(j[0], j[1], 'bo')
#         #     elif (j[2] == 2):
#         #         plt.plot(j[0], j[1], 'ro')
#         #     elif (j[2] == 3):
#         #         plt.plot(j[0], j[1], 'go')
#         #     else :
#         #         plt.plot(j[0], j[1], 'yo')
#
#     for i in range(right):
#         # for j in range(len[i]):
#         #     if(j[2] == 1):
#         #         plt.plot(j[0], j[1], 'bo')
#         #     elif (j[2] == 2):
#         #         plt.plot(j[0], j[1], 'ro')
#         #     elif (j[2] == 3):
#         #         plt.plot(j[0], j[1], 'go')
#         #     else :
#         #         plt.plot(j[0], j[1], 'yo')

def plotDataset(left, right):
    for j in left:
        plt.plot(j[0], j[1], 'bo')
    for j in right:
        plt.plot(j[0], j[1], 'ro')
    plt.show()
main()
