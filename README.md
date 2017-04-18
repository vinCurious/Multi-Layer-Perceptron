# Multi-Layer-Perceptron
Training and executing MLPs with hidden layers
<br>
Files in this directory:<br>

1. trainMLP.py: Program to train the MLP using train_data.csv file. Takes commad line arugment.
             'Usage: python trainMLP.py samplefile'<br>

2. executeMLP.py:	Executes the trained MLP on test data using test_data.csv. 'Usage: python executeMLP.py weights.csv sample'<br>
 
3. trainDT.py:	This program takes the training data file as input via the command line. <br>This program display the min.max,avg depth, number of nodes and leaves before and after pruning. To run this porgram  - python3 trainDT.py train_data.csv <br>
Multiple plots are generated after every split.<br>
4. executeDT.py:   This program takes the testing data file as input and provides the classification of data as at plot graphs. <br>This program also calculates confusion matrix and total profit before and after pruning. <br> To run this program - python3 trainDT.py test_data.csv <br>

5. train_data.csv: Training data file<br>
6. test_data.csv: Testing data file<br>
7. weights0.csv: weight values at initial stage<br>
8. weights10.csv: weight values after 10 Epocs<br>
9. weights100.csv: weight values after 100 Epocs<br>
10. weights1000.csv: weight values after 1000 Epocs<br>
11. weights10000.csv: Weight values after 10000 Epocs<br>
			<br>
How to run the program files:<br>
	1. Make sure that all program and date files are in same folder<br>
	2. Run python programs by following how to run information given along with that.<br>
	3. A graph will be plotted which shows specific epoc vs sum of squared error for samples in each epoc for trainMLP.py.
	   weight files are created in the same folder based on the Epoc values. <br>
	4. After running executeMLP.py program, results will be displayed in console along with a graph where all points are 
	   plotted with different colorrs or shape based on thier classes.
