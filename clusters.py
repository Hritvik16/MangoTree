import csv
import math
import numpy as np
from sklearn.cluster import KMeans

def to_numerical(votes):
    return [1 if (vote == 'Yea' or vote == 'Aye') else 0 for vote in votes]

def to_string(votes):
    """
        Implement the inverse of to_numerical here.
        (hint: Change this if you make changes to to_numerical.)
    """
    return ["Yea" if vote == 1 else "Nay" for vote in votes]

class CongressionalKMeans():
    data = []
    votes = []
    def __init__(self, path_to_csv, k, seed=0):
        """
        A model for clustering members of congress based on 
        their voting records. Complete this constructor in order
        to load the voting records from the file given by
        path_to_csv.
        (hint 1: See get_votes for the desired format.)
        (hint 2: Use to_binary function to convert data into numeric format 
                 appropriate for k-means clustering)
        (hint 3: You can use the DataSet constructor in tree.py for inspiration,
                 but you will need to do some things differently. You also do not
                 need all of the attributes, only the voting record.)

        Args:
            path_to_csv (str): The path to a congressional data set
            k (int): The number of clusters to fit
            seed (int): The random seed
        """
        np.random.seed(seed)
        self.k = k
        self.k_means = KMeans(n_clusters=self.k, random_state=0)
        with open(path_to_csv, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            
            for row in csvreader:
                self.data.append(row)

            for data in self.data:
                self.votes.append(to_numerical(data[4:]))

                # data = to_numerical(row[4:])
                # if(len(self.votes) == 0):
                #     self.votes = data
                # else:
                #     self.votes.append(data)
            # self.votes = np.array(self.votes)
            ##### TODO complete the constructor #####
            pass

        

    def get_votes(self):
        """
        Returns an (N, M) numpy array containing all votes 2018,
        where N is the number of congresspeople andM is the number 
        of resolutions. Each vote should have a numerical value. (See to_numerical)
        (hint: You shouldn't have to do anything accept access an
               instance variable in this function. All of the work
               should be done in the constructor)
        """
        # print(self.votes)
        return np.array(self.votes)

    def fit(self):
        """
        Fit the dataset using k-means clustering.
        (hint: Store any variables you need for other parts
               of the assignment as instance variables. No return
               value is necessary.)
        """
        self.k_means.fit(self.get_votes())
        

    def predict(self, i):
        """
        Predict the cluster for the i-th congressperson.
        Return a single number representing the cluster ID.
        (hint 1: you must call fit() first)
        (hint 2: see the documentation for sklearn.cluster.KMeans.predict())
        (hint 3: remember to store anything you need in fit())

        Args:
            i (int): The index of the congressperson to predict.

        Returns:
            (int): The cluster that the i-th congressperson belongs to.
        """
        self.fit()
        return self.k_means.predict(self.get_votes())[i]
        

    def get_cluster_center(self, i):
        """
        Return a numpy array of size (N,) containing center of the i-th cluster.
        (hint: see the documentation for sklearn.cluster.KMeans.cluster_centers_)
        """
        self.fit()
        return self.k_means.cluster_centers_[i]
        pass

    def get_median_voter(self, i):
        """
        Return an numpy array of size (N,) containing the the most likely
        vote for each vote for the given cluster.
        (hint: Use np.round on the cluster center to convert votes to 0 or 1 (or other values that you use).)
        """
        self.fit()
        np.round(self.get_cluster_center(i))
        pass

    def percentage(self):
        correct = 0
        count = 0
        for x in self.data:
            d = 0
            if x[3] == "Democrat":
                d = 1
            p = self.predict(count)
            if(p == 0 and d == 0 or p == 1 and d == 1):
                correct += 1
            else:
                print(d, p, count)
            
            count += 1
        print(correct/len(self.data))

if __name__ == '__main__':
    """
    You can use this area to test your implementation and to generate
    output for the assignment. The autograder will ignore this area.
    """
    kmeans = CongressionalKMeans('congress_data.csv', 2)
    kmeans.fit()
    kmeans.percentage();
    print(kmeans.predict(0))
    print(kmeans.predict(2))
