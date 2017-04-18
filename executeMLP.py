#executeMLP.py
#Author: Vinay More, Saurabh Wani, Amey Nayak
import sys
import numpy as nm
import matplotlib.pyplot as plotter
import matplotlib.patches as pat

class Network:
    output=[]
    hidden=[]
    input=[]
    weights={}
    a={}

    #Intializing the network with output, hidden and input layer values
    #Also setting up weights from the selected weights.csv file
    def __init__(self, output, hidden, input, file1, file2):
        self.output=output
        self.hidden=hidden
        self.input=input
        #Setting up weights from weights.csv file
        with open(file1) as f:
            for line in f:
                if(len(line)>1):
                    i=line[1:line.index(",")]
                    j=line[line.index(",")+1:line.index("\"",2)]
                    k=float(line[line.index(",",4)+1:])
                    self.weights[str(i)+","+str(j)]=k

        counter=0
        totalCount=0
        name={}
        mat=[{'bolt': 0,'nut': 0,'ring': 0,'scrap': 0}, {'bolt': 0,'nut': 0,'ring': 0,'scrap': 0},{'bolt': 0,'nut': 0,'ring': 0,'scrap': 0},{'bolt': 0,'nut': 0,'ring': 0,'scrap': 0}]
        cost=[{'bolt': 20,'nut': -7,'ring': -7,'scrap': -7}, {'bolt': -7,'nut': 15,'ring': -7,'scrap': -7},{'bolt': -7,'nut': -7,'ring': 5,'scrap': -7},{'bolt':-3,'nut': -3,'ring': -3,'scrap': -3}]
        profit=0
        name[1]="bolt"
        name[2]="nut"
        name[3]="ring"
        name[4]="scrap"

        #Reading test data file
        with open(file2) as f:
            for line in f:
                totalCount=totalCount+1
                str1=line.split(",")
                result=self.__calculateResult__(str1[0],str1[1],str1[2])
                xList.append(str1[0])
                yList.append(str1[1])
                cList.append(str1[2])
                if(result==1):
                    plotter.plot(str1[0],str1[1],"ro")
                elif(result==2):
                    plotter.plot(str1[0],str1[1],"bo")
                elif(result==3):
                    plotter.plot(str1[0],str1[1],"go")
                elif(result==4):
                    plotter.plot(str1[0],str1[1],"bx")

                if(int(result)==int(str1[2])):
                    counter=counter+1
                #print(result)
                mat[int(str1[2])-1][name[result]]=mat[int(str1[2])-1][name[result]]+1
        #print(mat)
        print("Recognition Rate:",(1.0*counter/totalCount)*100,"%")
        print("------------Confusion Matrix-----------------")
        print("n="+str(totalCount)+"    "+"bolt"+"  "+"nut"+"  "+"ring"+"  "+"scrap")
        for i in range(len(mat)):
            print(name[i+1]+"     "+str(mat[i]['bolt'])+"     "+str(mat[i]['nut'])+"     "+str(mat[i]['ring'])+"    "+str(mat[i]['scrap']))
            profit=profit+mat[i]['bolt']*cost[i]['bolt']+mat[i]['nut']*cost[i]['nut']+mat[i]['ring']*cost[i]['ring']+mat[i]['scrap']*cost[i]['scrap']
        print("profit: "+str(profit))


    #Takes x,y,c values as parameters and returns a predicted class
    def __calculateResult__(self, x, y, c):
        a={}
        for i in range(len(self.input)+len(self.output)+len(self.hidden)):
            a[i]=0.0
        a[0]=1.0
        a[1]=float(x)
        a[2]=float(y)
        a[3]=1.0

        for j in self.hidden[1:]:
            for i in self.input:
                a[j]=a[j]+ float(self.weights[str(i)+","+str(j)])*float(a[i])
            a[j]=self.sigmoid(a[j])

        for j in self.output:
            for i in self.hidden:
                a[j]=a[j]+ float(self.weights[str(i)+","+str(j)])*float(a[i])
            a[j]=self.sigmoid(a[j])

        classfiersList=[a[9],a[10],a[11],a[12]]
        maxVal = max(classfiersList)
        index = classfiersList.index(maxVal)
        return index+1

    #signmoid function
    def sigmoid(self,a):
        return (1/(1+nm.exp(-a)))

xList=[]
yList=[]
cList=[]
def main():
    if len(sys.argv) != 3:
        print('Usage: python executeMLP.py weights.csv sample')
        return
    else:
        output=[9,10,11,12]
        hidden=[3,4,5,6,7,8]
        input=[0,1,2]
        network= Network(output,hidden,input, sys.argv[1],sys.argv[2])

        #Plotting x and y values from test.csv with colors describing the class
        plotter.xlabel('x values')
        plotter.ylabel('y values')

        red = pat.Patch(color='red', label='Class 1')
        blue = pat.Patch(color='blue', label='Class 2')
        green = pat.Patch(color='green', label='Class 3')
        blueX = pat.Patch(color='blue', label='Class 4')

        plotter.legend(handles=[red,blue,green,blueX])
        plotter.show()

main()
