import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import model_selection
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier


np.set_printoptions(precision=4, suppress=True, threshold=sys.maxsize)


def Bayes():
    Bayes =  BernoulliNB()
    #cv on parameters: alpha, penalty
    clf = model_selection.GridSearchCV(estimator=Bayes,
                            param_grid={'fit_prior':['True','False'], 'alpha':[1e-3,1e-2,1e-1]}, 
                            scoring='accuracy', cv=10)
    clf.fit(train_x, train_y)

    pred_y = clf.predict(test_x)
    # pred_prob = clf.decision_function(test_x)   #get probability of the results

    #get the list of final parameters
    print(f"CV best params: {clf.best_params_}")
    #output cv results to csv for reporting
    pd.DataFrame.from_dict(clf.cv_results_).to_csv('cv_results.csv')

    #get the scores
    print(classification_report(test_y, pred_y, target_names=clf.classes_))
    #output the scores to csv for reporting
    pd.DataFrame.from_dict(classification_report(test_y, pred_y, target_names=clf.classes_, output_dict=True)).transpose().to_csv('class_scores.csv')

    #get the accuracy
    print(f"{BernoulliNB().__class__.__name__} Testing Accuracy: {accuracy_score(test_y, pred_y)}\n")




if __name__ == '__main__':

    df = pd.read_csv('training.csv')
    df_test = pd.read_csv('test.csv')

    #try both methods of vectorisation
    count_vect = CountVectorizer()#stop_words='english')
    #count_vect = TfidfVectorizer(stop_words='english')

    train_x = count_vect.fit_transform(df['article_words'])
    train_y = df['topic']
    test_x = count_vect.transform(df_test['article_words'])
    test_y = df_test['topic']

    
    Bayes()

