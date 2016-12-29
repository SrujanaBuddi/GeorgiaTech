import csv
import numpy as np  # http://www.numpy.org


"""
Here, X is assumed to be a matrix with n rows and d columns
where n is the number of total records
and d is the number of features of each record

Also, y is assumed to be a vector of d labels
"""

"""
This skeleton is provided to help you implement the assignment. It requires
implementing more that just the empty methods listed below. 

So, feel free to add functionalities when needed, but you must keep
the skeleton as it is.
"""

class RandomForest(object):
    class __DecisionTree(object):
        tree = {}

        def learn(self, X, y):
            # TODO: train decision tree and store it in self.tree
            pass

        def classify(self, record):
            # TODO: return predicted label for a single record using self.tree
            return 0

    num_trees = 0
    decision_trees = []
    bootstraps_datasets = [] # the bootstrapping dataset for trees
    bootstraps_labels = []   # the true class labels,
                             # corresponding to records in the bootstrapping dataset 

    def __init__(self, num_trees):
        # TODO: do initialization here.
        self.num_trees = num_trees
        self.decision_trees = [self.__DecisionTree() for i in range(num_trees)]
    
    def _bootstrapping(self, X, n):
        # TODO: create a sample dataset with replacement of size n
        #
        # Note that you will also need to record the corresponding
        #           class labels for the sampled records for training purpose.
        #
        # Referece: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
        pass

    def bootstrapping(self, X):
        # TODO: initialize the bootstrap datasets for each tree.
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(X, len(X))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    def fitting(self):
        # TODO: train `num_trees` decision trees using the bootstraps datasets and labels
        pass

    def voting(self, X):
        y = np.array([], dtype = int)

        for record in X:
            # TODO: find the sets of proper trees that consider the record
            #       as an out-of-bag sample, and predict the label(class) for the record. 
            #       The majority vote serves as the final label for this record.
            votes = []
            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]
                if record not in dataset:
                    OOB_tree = self.decision_trees[i] 
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            counts = np.bincount(votes)
            if len(counts) == 0:
                # TODO: special handling may be needed.
                pass
            else:
                y = np.append(y, np.argmax(counts))

        return y

def main():
    X = list()
    y = list()

    # Note: you must NOT change the general steps taken in this main() function.

    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)

        for line in csv.reader(f, delimiter = ","):
            X.append(line[:-1])
            y.append(line[-1])

    X = np.array(X, dtype = float)

    # Initialize according to your implementation
    forest_size = 10 

    # Initialize a random forest
    randomForest = RandomForest(forest_size)

    # Create the bootstrapping datasets
    randomForest.bootstrapping(X)

    # Build trees in the forest
    randomForest.fitting()

    # Provide an unbiased error estimation of the random forest 
    # based on out-of-bag (OOB) error estimate.
    # Note that you may need to handle the special case in
    #       which every single record in X has used for training by some 
    #       of the trees in the forest.
    y_truth = np.array(y, dtype = int)
    y_predicted = randomForest.voting(X)

    #results = [prediction == truth for prediction, truth in zip(y_predicted, y_test)]
    results = [prediction == truth for prediction, truth in zip(y_predicted, y_truth)]

    # Accuracy
    accuracy = float(results.count(True)) / float(len(results))
    print "accuracy: %.4f" % accuracy

main()
