#trainMLP.py
#Author: Vinay More, Saurabh Wani, Amey Nayak
import sys
import matplotlib.pyplot as plotter
import numpy as nm
import random as r
import csv

#Setting number of Epocs
EPOC=10000

def sigmoid(a):
    return (1.0/(1.0+nm.exp(-1*a)))

#Main program
def main():
    """main function """
    if len(sys.argv) != 2:
        print('Usage: python trainMLP.py samplefile')
        return
    else:
        #intializing  network
        output=[9,10,11,12]
        hidden=[3,4,5,6,7,8]
        input=[0,1,2]

        #Initializing weights dictionary with random weights between [-1,1]
        weights={}
        for i in input:
            for j in hidden[1:]:
                weights[str(i)+","+str(j)]=r.uniform(-1,1)
        for i in hidden:
            for j in output:
                weights[str(i)+","+str(j)]=r.uniform(-1,1)

        #Initialzing a values with 0
        a={}
        for i in range(len(input)+len(output)+len(hidden)):
            a[i]=0.0

        #initializing weights.csv files before writing weight values for network architecture
        f=open("weights0.csv","w")
        fwrite=csv.writer(f)
        for i in weights.items():
            fwrite.writerow(i)
        f.close()

        f10=open("weights10.csv","w")
        fwrite10=csv.writer(f10)

        f100=open("weights100.csv","w")
        fwrite100=csv.writer(f100)

        f1000=open("weights1000.csv","w")
        fwrite1000=csv.writer(f1000)

        f10000=open("weights10000.csv","w")
        fwrite10000=csv.writer(f10000)

        #Initializing xList, yList, cList to store x, y, c values from training set
        sumSquare=[] #stores sum of the sqaured error after each epoc
        delta={} #stores delta values for network

        #reading training sample
        source=[]
        with open(sys.argv[1]) as file:
            for line in file:
                source.append(line)

        for ins in range(EPOC+1):
            sum=0.0
            xList = []
            yList = []
            cList =[]
            for line in source:
                str1=line.split(",")
                xList.append(str1[0])
                yList.append(str1[1])
                cList.append(str1[2])

                #Adding bias values
                a[0]=1.0
                a[3]=1.0

                a[1]=float(str1[0])
                a[2]=float(str1[1])

                for j in hidden[1:]:
                    for i in input:
                        a[j]=a[j]+ float(weights[str(i)+","+str(j)])*float(a[i])
                    a[j]=sigmoid(a[j])

                for j in output:
                    for i in hidden:
                        a[j]=a[j]+ float(weights[str(i)+","+str(j)])*float(a[i])
                    a[j]=sigmoid(a[j])

                for j in output:
                    if(int(str1[2])==1):
                        if(int(j)==9):
                            delta[j]= a[j]*(1 - a[j])*(1- a[j])
                            sum=sum+0.5*(1-a[j])*(1-a[j])
                        else:
                            delta[j]= a[j]*(1 - a[j])*(0- a[j])
                            sum=sum+0.5*(0-a[j])*(0-a[j])
                    elif(int(str1[2])==2):
                        if(int(j)==10):
                            delta[j]= a[j]*(1 - a[j])*(1- a[j])
                            sum=sum+0.5*(1-a[j])*(1-a[j])
                        else:
                            delta[j]= a[j]*(1 - a[j])*(0- a[j])
                            sum=sum+0.5*(0-a[j])*(0-a[j])
                    elif(int(str1[2])==3):
                        if(int(j)==11):
                            delta[j]= a[j]*(1 - a[j])*(1- a[j])
                            sum=sum+0.5*(1-a[j])*(1-a[j])
                        else:
                            delta[j]= a[j]*(1 - a[j])*(0- a[j])
                            sum=sum+0.5*(0-a[j])*(0-a[j])
                    elif(int(str1[2])==4):
                        if(int(j)==12):
                            delta[j]= a[j]*(1 - a[j])*(1- a[j])
                            sum=sum+0.5*(1-a[j])*(1-a[j])
                        else:
                            delta[j]= a[j]*(1 - a[j])*(0- a[j])
                            sum=sum+0.5*(0-a[j])*(0-a[j])

                for i in hidden:
                    temp=0.0
                    for j in output:
                        temp=temp+weights[str(i)+","+str(j)]*delta[j]
                    delta[i]=a[i]*(1-a[i])*temp

                for i in input:
                    temp=0.0
                    for j in hidden[1:]:
                        temp=temp+weights[str(i)+","+str(j)]*delta[j]
                    delta[i]=a[i]*(1-a[i])*temp

                for element in weights:
                    strSplit=element.split(",")
                    i = int(strSplit[0])
                    j = int(strSplit[1])
                    weights[element]=weights[element]+0.1*a[int(i)]*delta[int(j)]
            sumSquare.append(sum)
            if(ins==10):
                fwrite10.writerows(weights.items())
                f10.close()
            elif(ins==100):
                fwrite100.writerows(weights.items())
                f100.close()
            elif(ins==1000):
                fwrite1000.writerows(weights.items())
                f1000.close()
            elif(ins==10000):
                fwrite10000.writerows(weights.items())
                f10000.close()

        #plotting squared error difference and adding weight values in weights.csv
        plotter.figure("Epoc vs Sum of squared error")
        plotter.xlabel('Number of Epocs')
        plotter.ylabel('Sum of squared error')
        plotter.plot(sumSquare)
        plotter.show()

main()