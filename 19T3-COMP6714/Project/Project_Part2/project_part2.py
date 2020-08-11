import spacy
import math
import copy
import xgboost as xgb
import numpy as np


def initiation(documents):
    global tf_entities, tf_tokens, idf_entities, idf_tokens

    tf_entities = {}
    tf_tokens = {}
    idf_tokens = {}
    idf_entities = {}

    ents_counter = {} # 用于和token中的entity抵消
    for i in documents:
        doc = nlp(documents[i])
        for n in doc.ents:
            if len(n) == 1:
                for tmp in n:
                    e = n.lemma_
            else:
                e = n.orth_
            if e not in tf_entities:
                tf_entities[e] = {}
                tf_entities[e][i] = 1
                if len(n) == 1:
                    ents_counter[e] = {}
                    ents_counter[e][i] = 1
            elif i not in tf_entities[e]:
                tf_entities[e][i] = 1
                if len(n) == 1:
                    ents_counter[e][i] = 1
            else:
                tf_entities[e][i] += 1
                if len(n) == 1:
                    ents_counter[e][i] += 1

        for text in doc:
            if not text.is_punct and not text.is_space and not text.is_stop:
                word = text.lemma_
                if word not in ents_counter or i not in ents_counter[word]:
                    if word not in tf_tokens:
                        tf_tokens[word] = {}
                        tf_tokens[word][i] = 1
                    elif i not in tf_tokens[word]:
                        tf_tokens[word][i] = 1
                    else:
                        tf_tokens[word][i] += 1
                else:
                    if ents_counter[word][i] > 1:
                        ents_counter[word][i] -= 1
                    else:
                        del ents_counter[word][i]

    idf_tokens = copy.deepcopy(tf_tokens)
    idf_entities = copy.deepcopy(tf_entities)

    # update the score
    for key in idf_tokens:
        for i in idf_tokens[key]:
            idf_tokens[key][i] = (1+math.log(1+math.log(idf_tokens[key][i]))) * (1+math.log(len(documents)/(1+len(idf_tokens[key]))))
    for key in idf_entities:
        for i in idf_entities[key]:
            idf_entities[key][i] = (1+math.log(idf_entities[key][i])) * (1+math.log(len(documents)/(1+len(idf_entities[key]))))
    
    return tf_entities, tf_tokens, idf_entities, idf_tokens

def tf_idf(candidate, doc_id):
    tokens_score = entities_score = 0
    candidate = nlp(candidate.replace('_', ' '))
    for ent in candidate.ents:
        if ent.lemma_ in idf_entities and doc_id in idf_entities[ent.lemma_]:
            entities_score += idf_entities[ent.lemma_][doc_id]

    for token in candidate:
        if token.lemma_ in idf_tokens and doc_id in idf_tokens[token.lemma_]:
            tokens_score += idf_tokens[token.lemma_][doc_id]

    combined_score = (entities_score + tokens_score * 0.4)/len(candidate)

    return combined_score

def minDistance(word1, word2):
    if not word1:
        return len(word2 or '') or 0

    if not word2:
        return len(word1 or '') or 0

    size1 = len(word1)
    size2 = len(word2)

    last = 0
    tmp = list(range(size2 + 1))
    value = None

    for i in list(range(size1)):
        tmp[0] = i + 1
        last = i
        for j in range(size2):
            if word1[i] == word2[j]:
                value = last
            else:
                value = 1 + min(last, tmp[j], tmp[j + 1])
            last = tmp[j+1]
            tmp[j+1] = value
    return value

def cosine(str1, str2):
    str2 = str2.replace('_', ' ')
    list_word1 = str1.split()
#     print(list_word1)
    list_word2 = str2.split()
#     print(list_word2)
    key_word = list(set(list_word1 + list_word2))
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))
    count = 0
    flag = True
    for i in range(len(key_word)):
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
     
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1
            if list_word2[k] in list_word1 and flag:
                count += 1  
        flag = False

    dist1=float(np.dot(word_vector1,word_vector2)/(np.linalg.norm(word_vector1)*np.linalg.norm(word_vector2)))
    count = count/len(list_word1)
    return dist1,count

def label_value(data, label):
    lis = []
    for i in data:
        for word in data[i]['candidate_entities']:
            if word == label[i]['label']:
                lis.append(1)
            else:
                lis.append(0)
    return np.array(lis)

def extract_features(mentions):
    distance_list = []
    tfidf_list = []
    same_counter = []
    cosine_list = []
    for i in mentions:
        for candidate in mentions[i]['candidate_entities']:
            distance_list.append(minDistance(mentions[i]['mention'], candidate))
            tfidf_list.append(tf_idf(candidate,mentions[i]['doc_title']))
            cosine_value, same_count = cosine(mentions[i]['mention'], candidate)
            cosine_list.append(cosine_value)
            same_counter.append(same_count)
    return np.array([tfidf_list, distance_list, cosine_list, same_counter]).T 

def data_group(mentions):
    data_group = []
    for i in mentions:
        data_group.append(len(mentions[i]['candidate_entities']))
    data_groups = np.array(data_group)
    return data_groups

def transform_data(features, groups, labels=None):
    xgb_data = xgb.DMatrix(data=features, label=labels)
    xgb_data.set_group(groups)
    return xgb_data

def disambiguate_mentions(train_mentions, train_labels, dev_mentions, men_docs, parsed_entity_pages):
	global nlp
	nlp = spacy.load('en_core_web_sm')
	# start = time.time()
	initiation(men_docs)
	# print("initiation cost time: {}".format(time.time()-start))

	# start = time.time()
	train_data = extract_features(train_mentions)
	train_groups = data_group(train_mentions)
	train_label = label_value(train_mentions,train_labels)
	xgboost_train = transform_data(train_data, train_groups, train_label)
	# print("train data set cost time: {}".format(time.time()-start))

	# Test Data
	# start = time.time()
	test_data = extract_features(dev_mentions)
	test_groups = data_group(dev_mentions)
	xgboost_test = transform_data(test_data, test_groups)
	# print("test data set cost time: {}".format(time.time()-start))

	# start = time.time()
	param = {'max_depth': 7, 'eta': 0.05, 'silent': 1, 'objective': 'rank:pairwise',
	         'min_child_weight': 0.01, 'lambda':100}
	classifier = xgb.train(param, xgboost_train, num_boost_round=2100)
	##  Predict test data...
	preds = classifier.predict(xgboost_test)
	# print("predict cost time: {}".format(time.time()-start))

	# start = time.time()
	result = []
	counter = 0
	preds = list(preds)
	test_group = list(test_groups)

	for i in range(len(test_group)):
	    tmp = preds[counter:(test_group[i]+counter)]
	    result.append(tmp.index(max(tmp)))
	    counter += test_group[i]

	result_dict = {}
	for i in range(len(result)):
	    result_dict[i+1] = dev_mentions[i+1]['candidate_entities'][result[i]]
	# print("build result cost time: {}".format(time.time()-start))

	return result_dict