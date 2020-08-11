import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('training.csv')
df1 = pd.read_csv('test.csv')

# Create text array
text = df['article_words']
textTest = df1['article_words']

# Create bag of words feature matrix
count = CountVectorizer()
X  = count.fit_transform(text)
XTest = count.transform(textTest)

# Create target vector
y = df['topic']
yTest = df1['topic']

#Train and fit - logitic regression 78.4% accuracy, SVM will give 77.4%
clf =  SGDClassifier(loss='log', penalty='l2', alpha=1e-3, random_state=42, max_iter=5)
clf.fit(X, y)

#Predict
predicted = clf.predict(XTest)
confidence = clf.decision_function(XTest)

#Classes ['ARTS CULTURE ENTERTAINMENT' 'BIOGRAPHIES PERSONALITIES PEOPLE' 'DEFENCE' 'DOMESTIC MARKETS' 
# 'FOREX MARKETS' 'HEALTH' 'IRRELEVANT' 'MONEY MARKETS''SCIENCE AND TECHNOLOGY' 'SHARE LISTINGS' 'SPORTS']
#Get top 10 suggestions
suggested = np.zeros((11, 10))
id = df1['article_number']
for i in range(11):
    count = 0
    topic = clf.classes_[i]
    for j in range(500):
        if (predicted[j] == topic) & (count < 10):
            suggested[i][count] = id[j]
            count += 1
        elif count >= 10:
            break

topics = topic = {'IRRELEVANT':0, 'ARTS CULTURE ENTERTAINMENT':1, 'BIOGRAPHIES PERSONALITIES PEOPLE':2, 'DEFENCE':3, 'DOMESTIC MARKETS':4, 'FOREX MARKETS':5, 'HEALTH':6, 'MONEY MARKETS':7, 'SCIENCE AND TECHNOLOGY':8, 'SHARE LISTINGS':9, 'SPORTS':10}
print(metrics.classification_report(yTest, predicted, target_names=topics.keys()))

#print suggestions
print("ARTS CULTURE ENTERTAINMENT: ", suggested[0])
print("BIOGRAPHIES PERSONALITIES PEOPLE: ", suggested[1])
print("DEFENCE: ", suggested[2])
print("DOMESTIC MARKETS: ", suggested[3])
print("FOREX MARKETS: ", suggested[4])
print("HEALTH: ", suggested[5])
print("MONEY MARKETS: ", suggested[7])
print("SCIENCE AND TECHNOLOGY: ", suggested[8])
print("SHARE LISTINGS: ", suggested[9])
print("SPORTS: ", suggested[10])

print("Accuracy Test Dataset:", accuracy_score(yTest, predicted))
