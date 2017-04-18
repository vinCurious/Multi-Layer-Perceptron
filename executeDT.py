"""
Filename: executeDT.py
author: Ameya Nayak, Vinay More, Saurabh Wani
"""


import collections
import math
import sys
import matplotlib.pylab as plt
class Node:
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

    def makeLeaf(self, decision):
        self.isLeaf = True
        self.decision = decision

    def prune(self):
        self.chiPruned = True

    def chis(self, chi):
        self.chi = chi

    def addLeft(self, left):
        self.left = left

    def addRight(self, right):
        self.right = right

    def addThreshold(self, attribute, threshold):
        self.attribute = attribute
        self.threshold = threshold

    def printNode(self, m):
        m.write("\nAttribute = " + str(self.attribute))
        m.write("\nThreshold = " + str(self.threshold))
        m.write("\nLeaf =" + str(self.isLeaf))
        m.write("\nDecision = " + str(self.decision))
        if self.isLeaf == False:
            m.write("\nRight of " + str(self.attribute) + " = " + str(self.threshold))
            self.right.printNode(m)
            m.write("\nLeft of" + str(self.attribute) + " = " + str(self.threshold))
            self.left.printNode(m)

    def pruneTree(self):
        if (self.chi <= 7.815):
            self.makeLeaf(max(self.freq, key=self.freq.get))
        if self.right != None:
            self.right.pruneTree()
        if self.left != None:
            self.left.pruneTree()

    def getDecision(self, test):
        if self.isLeaf:
            return self.decision
        else:
            if test[self.attribute] > self.threshold:
                return self.right.getDecision(test)
            else:
                return self.left.getDecision(test)

def main():
    # Read file
    f = open("train_data.csv", 'rt')
    inData = {}
    for row in f:
        if len(row) > 1:
            row = row.split(",")
            inData.update({row[0]: [row[1], row[2]]})
    sortData = collections.OrderedDict(sorted(inData.items()))
    sortdataList = []
    for data in sortData:
        sortdataList.append([float(data), float(sortData[data][0]), int(sortData[data][1])])
    x = buildtree(sortdataList, "none")
    print("*************************Before Pruning************************************")
    # Calculating profit and confusion matrix
    m = open(sys.argv[1], 'rt')
    name = {}
    mat = [{'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}, {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0},
           {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}, {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}]
    cost = [{'bolt': 20, 'nut': -7, 'ring': -7, 'scrap': -7}, {'bolt': -7, 'nut': 15, 'ring': -7, 'scrap': -7},
            {'bolt': -7, 'nut': -7, 'ring': 5, 'scrap': -7}, {'bolt': -3, 'nut': -3, 'ring': -3, 'scrap': -3}]
    profit = 0
    name[1] = "bolt"
    name[2] = "nut"
    name[3] = "ring"
    name[4] = "scrap"
    totalCount = 0
    counter = 0

    for row in m:
        if len(row) > 1:
            totalCount += 1
            row = row.split(",")
            inData.update({row[0]: [row[1], row[2]]})
            if(int(x.getDecision([float(row[0]), float(row[1])])) == 1):
                plt.plot(row[0], row[1], 'bo')
            elif (int(x.getDecision([float(row[0]), float(row[1])])) == 2):
                plt.plot(row[0], row[1], 'ro')
            elif (int(x.getDecision([float(row[0]), float(row[1])])) == 3):
                plt.plot(row[0], row[1], 'go')
            else:
                plt.plot(row[0], row[1], 'yo')
            #print("Calculated Classification = ", x.getDecision([float(row[0]), float(row[1])]),
                  #" Actual Classification = ", row[2])
            result = x.getDecision([float(row[0]), float(row[1])])
            if int(result) == int(row[2]):
                counter += 1
            mat[int(row[2]) - 1][name[result]] = mat[int(row[2]) - 1][name[result]] + 1
    plt.show()

    print("Recognition Rate:", (1.0 * counter / totalCount) * 100, "%")
    print("------------Confusion Matrix-----------------")
    print("n=" + str(totalCount) + "    " + "bolt" + "  " + "nut" + "  " + "ring" + "  " + "scrap")
    for i in range(len(mat)):
        print(name[i + 1] + "     " + str(mat[i]['bolt']) + "     " + str(mat[i]['nut']) + "     " + str(mat[i]['ring']) + "    " + str(mat[i]['scrap']))
        profit = profit + mat[i]['bolt'] * cost[i]['bolt'] + mat[i]['nut'] * cost[i]['nut'] + mat[i]['ring'] * cost[i][
            'ring'] + mat[i]['scrap'] * cost[i]['scrap']
    print("profit: " + str(profit))

    m.close()
    m = open(sys.argv[1], 'rt')


    x.pruneTree()

    print("*************************After Pruning************************************")
    m = open(sys.argv[1], 'rt')
    name = {}
    mat = [{'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}, {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0},
           {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}, {'bolt': 0, 'nut': 0, 'ring': 0, 'scrap': 0}]
    cost = [{'bolt': 20, 'nut': -7, 'ring': -7, 'scrap': -7}, {'bolt': -7, 'nut': 15, 'ring': -7, 'scrap': -7},
            {'bolt': -7, 'nut': -7, 'ring': 5, 'scrap': -7}, {'bolt': -3, 'nut': -3, 'ring': -3, 'scrap': -3}]
    profit = 0
    name[1] = "bolt"
    name[2] = "nut"
    name[3] = "ring"
    name[4] = "scrap"
    totalCount = 0
    counter = 0

    for row in m:
        if len(row) > 1:
            totalCount += 1
            row = row.split(",")
            inData.update({row[0]: [row[1], row[2]]})
            #print("Calculated Classification = ", x.getDecision([float(row[0]), float(row[1])])," Actual Classification = ", row[2])
            result = x.getDecision([float(row[0]), float(row[1])])
            if int(result) == int(row[2]):
                counter += 1
            mat[int(row[2]) - 1][name[result]] = mat[int(row[2]) - 1][name[result]] + 1
            if (int(x.getDecision([float(row[0]), float(row[1])])) == 1):
                plt.plot(row[0], row[1], 'bo')
            elif (int(x.getDecision([float(row[0]), float(row[1])])) == 2):
                plt.plot(row[0], row[1], 'ro')
            elif (int(x.getDecision([float(row[0]), float(row[1])])) == 3):
                plt.plot(row[0], row[1], 'go')
            else:
                plt.plot(row[0], row[1], 'yo')
    plt.show()

    print("Recognition Rate:", (1.0 * counter / totalCount) * 100, "%")
    print("------------Confusion Matrix-----------------")
    print("n=" + str(totalCount) + "    " + "bolt" + "  " + "nut" + "  " + "ring" + "  " + "scrap")
    for i in range(len(mat)):
        print(name[i + 1] + "     " + str(mat[i]['bolt']) + "     " + str(mat[i]['nut']) + "     " + str(mat[i]['ring']) + "    " + str(mat[i]['scrap']))
        profit = profit + mat[i]['bolt'] * cost[i]['bolt'] + mat[i]['nut'] * cost[i]['nut'] + mat[i]['ring'] * cost[i][
            'ring'] + mat[i]['scrap'] * cost[i]['scrap']
    print("profit: " + str(profit))

    m.close()



def buildtree(samples, root):
    # node = Node()
    inData = {}
    freq = {1: 0, 2: 0, 3: 0, 4: 0}
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

    if count > 2:
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
    s = -((freq[1] / count) * freq1) - ((freq[2] / count) * freq2) - ((freq[3] / count) * freq3) - (
    (freq[4] / count) * freq4)
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
        newRoot = "X = " + str(minX)
        node.addThreshold(0, minX)
        for data in sortdataList:
            if data[0] < minX:
                left.append(data)
            else:
                right.append(data)
    chi = calcChiSquare(left, right)
    node.chis(chi)
    node.addRight(buildtree(right, newRoot))
    node.addLeft(buildtree(left, newRoot))
    return node


def calcEntropy(countleft, countright):
    for i in range(len(countleft)):
        left1 = 0 if countleft[0] == 0 else math.log(countleft[0] / sum(countleft), 2)
        left2 = 0 if countleft[1] == 0 else math.log(countleft[1] / sum(countleft), 2)
        left3 = 0 if countleft[2] == 0 else math.log(countleft[2] / sum(countleft), 2)
        left4 = 0 if countleft[3] == 0 else math.log(countleft[3] / sum(countleft), 2)
        right1 = 0 if countright[0] == 0 else math.log(countright[0] / sum(countright), 2)
        right2 = 0 if countright[1] == 0 else math.log(countright[1] / sum(countright), 2)
        right3 = 0 if countright[2] == 0 else math.log(countright[2] / sum(countright), 2)
        right4 = 0 if countright[3] == 0 else math.log(countright[3] / sum(countright), 2)

    left = -(countleft[0] / sum(countleft) * left1) - (countleft[1] / sum(countleft) * left2) - (
    countleft[2] / sum(countleft) * left3) - (countleft[3] / sum(countleft) * left4)
    right = -(countright[0] / sum(countright) * right1) - (countright[1] / sum(countright) * right2) - (
    countright[2] / sum(countright) * right3) - (countright[3] / sum(countright) * right4)
    return left + right


def calcChiSquare(left, right):
    sum = 0;
    freq1 = {1: 0, 2: 0, 3: 0, 4: 0}
    freq2 = {1: 0, 2: 0, 3: 0, 4: 0}
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


main()
