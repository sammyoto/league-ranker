# Code based off of https://github.com/mesosbrodleto/playerank/blob/master/playerank/models/Weighter.py
# Minor changes made, but same for the most part

from sklearn.base import BaseEstimator
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
import json
import numpy as np

class Weighter(BaseEstimator):
    """Automatic weighting of performance features

    random_state : int
        RandomState instance or None, optional, default: None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Attributes
    ----------
    clf_: LinearSVC object
        the object of the trained classifier
    weights_ : array, [n_features]
        weights of the features computed by the classifier
    """
    def __init__(self, random_state=42):
        self.random_state_ = random_state

    def fit(self, column_names, Xtrain, ytrain, scaled=False, filename='weights.json'):
        
        X = Xtrain
        y = ytrain

        if scaled:
            X = StandardScaler().fit_transform(X)

        self.feature_names_ = column_names
        self.clf_ = LinearSVC(fit_intercept=True, dual = False,  max_iter = 50000, random_state=self.random_state_)

        self.clf_.fit(X, y)

        importances = self.clf_.coef_[0]

        sum_importances = sum(np.abs(importances))
        self.weights_ = importances / sum_importances

        ## Save the computed weights into a json file
        print("Saving weights to JSON.\n")
        features_and_weights = {}
        for feature, weight in sorted(zip(self.feature_names_, self.weights_),key = lambda x: x[1]):
            features_and_weights[feature]=  weight
        json.dump(features_and_weights, open('%s' %filename, 'w'))
        ## Save the object
        #pkl.dump(self, open('%s.pkl' %filename, 'wb'))

    def get_weights(self):
        return self.weights_

    def get_feature_names(self):
        return self.feature_names_