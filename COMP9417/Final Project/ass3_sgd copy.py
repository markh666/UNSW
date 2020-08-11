import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import model_selection
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier


np.set_printoptions(precision=4, suppress=True, threshold=sys.maxsize)


def SGDLG():
    sgd =  SGDClassifier(loss='log', random_state=42, max_iter=20, learning_rate='optimal', early_stopping=True, class_weight='balanced')
    #cv on parameters: alpha, penalty
    clf = model_selection.GridSearchCV(estimator=sgd,
                            param_grid={'penalty':['l2','l1'], 'alpha':[1e-3,1e-2,1e-1]}, 
                            scoring='accuracy', cv=10)
    clf.fit(train_x, train_y)

    pred_y = clf.predict(test_x)
    pred_prob = clf.decision_function(test_x)   #get probability of the results

    #get the list of final parameters
    print(f"CV best params: {clf.best_params_}")
    #output cv results to csv for reporting
    pd.DataFrame.from_dict(clf.cv_results_).to_csv('cv_results.csv')

    #get the scores
    print(classification_report(test_y, pred_y, target_names=clf.classes_))
    #output the scores to csv for reporting
    pd.DataFrame.from_dict(classification_report(test_y, pred_y, target_names=clf.classes_, output_dict=True)).transpose().to_csv('class_scores.csv')

    #get the accuracy
    print(f"{SGDClassifier().__class__.__name__} Testing Accuracy: {accuracy_score(test_y, pred_y)}\n")

    #get the top 10 or less recommented artivles
    getTop(df_test, pred_y, pred_prob, clf)




def getTop(df_out, predict_y, predict_prob, clf):
    #for each testing data, add probability of each class and final prediction to a dataframe
    df_out = df_out.append(pd.DataFrame(columns=clf.classes_.tolist()+['predict_y']))
    for i in range(len(predict_y)):
        for j in range(len(predict_prob[i])): df_out.loc[i,clf.classes_[j]] = predict_prob[i][j]
        df_out.loc[i,'predict_y'] = predict_y[i]
    #df_out.to_csv('temp.csv')

    #this is the dataframe containing the recommended articles for each topic, and their scores
    df_recommend = pd.DataFrame(columns=['topic','suggested','precision','recall','f1'])
    for k in clf.classes_.tolist():
        #choose the top 10 articles from each predicted class
        df_sort = df_out.query(f"predict_y == '{k}'").sort_values(by=[k], ascending=False).head(10)
        print(f"{k}:")
        print(f"\t{df_sort['article_number'].tolist()}")
        print(f"\tWeighted Precision: {precision_score(df_sort['topic'], df_sort['predict_y'], average='weighted')}")
        print(f"\tWeighted Recall: {recall_score(df_sort['topic'], df_sort['predict_y'], average='weighted')}")
        print(f"\tWeighted F-1: {f1_score(df_sort['topic'], df_sort['predict_y'], average='weighted')}")
        df_recommend.loc[len(df_recommend)] = [k, 
                                        ", ".join(df_sort['article_number'].astype(int).astype(str).tolist()), 
                                        round(precision_score(df_sort['topic'], df_sort['predict_y'], average='weighted'),2),
                                        round(recall_score(df_sort['topic'], df_sort['predict_y'], average='weighted'),2),
                                        round(f1_score(df_sort['topic'], df_sort['predict_y'], average='weighted'),2)]
    #output the top recommended articles to csv for reporting
    df_recommend.to_csv('recommend_scores.csv')



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

    
    SGDLG()

