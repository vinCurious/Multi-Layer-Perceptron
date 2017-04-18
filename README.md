# Multi-Layer-Perceptron
Training and executing MLPs with hidden layers
Files in this directory:
trainMLP.py: Program to train the MLP using train_data.csv file. Takes commad line arugment.
             'Usage: python trainMLP.py samplefile'
executeMLP.py:	Executes the trained MLP on test data using test_data.csv. 'Usage: python executeMLP.py weights.csv sample' 
trainDT.py:	This program takes the training data file as input via the command line. 
            This program display the min.max,avg depth, number of nodes and leaves before and after pruning. 
			To run this porgram  - python3 trainDT.py train_data.csv
			Multiple plots are generated after every split.
executeDT.py:   This program takes the testing data file as input and provides the classification of data as at plot graphs
				This program also calculates confusion matrix and total profit before and after pruning
				To run this program - python3 trainDT.py test_data.csv
train_data.csv: Training data file
test_data.csv: Testing data file
weights0.csv: weight values at initial stage
weights10.csv: weight values after 10 Epocs
weights100.csv: weight values after 100 Epocs
weights1000.csv: weight values after 1000 Epocs
weights10000.csv: Weight values after 10000 Epocs
			
How to run the program files:
	1. Make sure that all program and date files are in same folder
	2. Run python programs by following how to run information given along with that.
	3. A graph will be plotted which shows specific epoc vs sum of squared error for samples in each epoc for trainMLP.py.
	   weight files are created in the same folder based on the Epoc values. 
	4. After running executeMLP.py program, results will be displayed in console along with a graph where all points are 
	   plotted with different colorrs or shape based on thier classes.
