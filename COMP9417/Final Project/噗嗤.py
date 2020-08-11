import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn import model_selection
from sklearn.svm import LinearSVC


np.set_printoptions(precision=4, suppress=True, threshold=sys.maxsize)


def loadData():
    df = pd.read_csv('training.csv')
    df_test = pd.read_csv('test.csv')

    df['topic_id'] = df['topic'].factorize()[0]

    topic_to_id = dict(df[['topic', 'topic_id']].drop_duplicates().sort_values('topic_id').values)
    id_to_topic = dict(df[['topic_id', 'topic']].drop_duplicates().sort_values('topic_id').values)

    df_test['topic_id'] = df_test['topic'].apply(lambda x : topic_to_id[x])

    return df, df_test, topic_to_id, id_to_topic



def SVMachine():

    #cross validation
    regu = [0.01, 0.1, 0.5, 0.9, 1, 1.5]
    best_c = regu[0]
    score_init = 0

    for c in regu:
        svm = LinearSVC(C=c)
        score = model_selection.cross_val_score(svm, train_x, train_y, cv=10, scoring='accuracy')

        if score.mean() > score_init:
            best_c = c
            score_init = score.mean()

    svm = LinearSVC(C=best_c)
    svm.fit(train_x, train_y)

    pred_y = svm.predict(test_x)
    pred_prob = svm.decision_function(test_x)

    print(metrics.classification_report(test_y, pred_y, target_names=topic_to_id.keys()))
    print(f"{LinearSVC().__class__.__name__} Testing Accuracy (c={best_c}): {metrics.accuracy_score(pred_y, test_y)}\n")

    getTop(df_test, pred_y, pred_prob)




def getTop(df_out, predict_y, predict_prob):
    df_out = df_out.append(pd.DataFrame(columns=list(topic_to_id.keys())+['predict_y']))
    for i in range(len(predict_y)):
        for j in range(len(predict_prob[i])): df_out.loc[i,id_to_topic[j]] = predict_prob[i][j]
        df_out.loc[i,'predict_y'] = predict_y[i]

    for k in topic_to_id.keys():
        #recommend exactly 10, sorted by prediction
        #df_sort = df_out.query(f"predict_y == {topic_to_id[k]}").sort_values(by=[k], ascending=False).append(df_out.query(f"predict_y != {topic_to_id[k]}").sort_values(by=[k], ascending=False))
        #recommend at most 10, sorted by prediction
        df_sort = df_out.query(f"predict_y == {topic_to_id[k]}").sort_values(by=[k], ascending=False)
        print(f"{k}: {df_sort['article_number'].head(10).tolist()}")




if __name__ == '__main__':
    df, df_test, topic_to_id, id_to_topic = loadData()
    tfidf_vect = TfidfVectorizer(norm='l2', stop_words='english')

    train_x = tfidf_vect.fit_transform(df['article_words'])
    train_y = df['topic_id']
    test_x = tfidf_vect.transform(df_test['article_words'])
    test_y = df_test['topic_id']

    SVMachine()
