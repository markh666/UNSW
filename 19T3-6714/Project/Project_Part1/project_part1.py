import spacy
import math
from collections import Counter
import copy

class InvertedIndex:
    def __init__(self):
        ## You should use these variable to store the term frequencies for tokens and entities...
        self.tf_tokens = {}
        self.tf_entities = {}

        ## You should use these variable to store the inverse document frequencies for tokens and entities...
        self.idf_tokens = {}
        self.idf_entities = {}

    ## Your implementation for indexing the documents...
    def index_documents(self, documents):
        nlp = spacy.load('en_core_web_sm')
        ents_counter = {} # 用于和token中的entity抵消
        for i in range(1, len(documents)+1):
            doc = nlp(documents[i])
            for n in doc.ents:
                e = n.orth_
                if e not in self.tf_entities:
                    self.tf_entities[e] = {}
                    self.tf_entities[e][i] = 1
                    if len(n) == 1:
                        ents_counter[e] = {}
                        ents_counter[e][i] = 1
                elif i not in self.tf_entities[e]:
                    self.tf_entities[e][i] = 1
                    if len(n) == 1:
                        ents_counter[e][i] = 1
                else:
                    self.tf_entities[e][i] += 1
                    if len(n) == 1:
                        ents_counter[e][i] += 1

            for text in doc:
                if not text.is_punct and not text.is_space and not text.is_stop:
                    word = text.orth_
                    if word not in ents_counter or i not in ents_counter[word]:
                        if word not in self.tf_tokens:
                            self.tf_tokens[word] = {}
                            self.tf_tokens[word][i] = 1
                        elif i not in self.tf_tokens[word]:
                            self.tf_tokens[word][i] = 1
                        else:
                            self.tf_tokens[word][i] += 1
                    else:
                        if ents_counter[word][i] > 1:
                            ents_counter[word][i] -= 1
                        else:
                            del ents_counter[word][i]

        self.idf_tokens = copy.deepcopy(self.tf_tokens)
        self.idf_entities = copy.deepcopy(self.tf_entities)

        # update the score
        for key in self.idf_tokens:
            for i in self.idf_tokens[key]:
                self.idf_tokens[key][i] = (1+math.log(1+math.log(self.idf_tokens[key][i]))) * (1+math.log(len(documents)/(1+len(self.idf_tokens[key]))))
        for key in self.idf_entities:
            for i in self.idf_entities[key]:
                self.idf_entities[key][i] = (1+math.log(self.idf_entities[key][i])) * (1+math.log(len(documents)/(1+len(self.idf_entities[key]))))

    def getSubLists(self, lis=[],l=0):
        res = []
        for m in range(1, l+1):
            allAns = []
            ans = [None for i in range(m)]  
            self.subLists(lis,m,ans,allAns)
            res.extend(allAns)
        return res

    def subLists(self, lis=[],m=0,ans=[],allAns=[]):
        if m==0:
            allAns.append(ans.copy()) 
            return
        if len(lis)<m:
            return
        length=len(lis)
        for iter in range(length-m+1):
            ans[-m]=lis[iter]
            if iter+1<length:
                self.subLists(lis[iter+1:],m-1,ans,allAns)
            else:
                allAns.append(ans.copy())
                return

    def Query_counter(self, query):
        q_count = {} 
        for word in query:
            if word not in q_count:
                q_count[word] = 1
            else:
                q_count[word] += 1
        return q_count

    def filter_options(self, all_ops, q_count):
        after_filter = []
        for op in all_ops:
            dic_op = {}
            flag = True
            for item in op:
                item = item.split()
                for i in item:
                    if i not in dic_op:
                        dic_op[i] = 1
                    else:
                        dic_op[i] += 1
            for word in dic_op:
                if word not in q_count or q_count[word] < dic_op[word]:
                    flag = False
                    break
            if flag:
                after_filter.append(op)
        return after_filter

    ## Your implementation to split the query to tokens and entities...
    def split_query(self, Q, DoE):
        query = Q.split()
        q_count = self.Query_counter(query)
        Query_entity = []
        for i in DoE:
            tmp = copy.deepcopy(q_count)
            Flag = True
            for j in i.split():
                if j not in tmp or tmp[j] == 0:
                    Flag = False
                    break
                else:
                    tmp[j] -= 1
            if Flag:
                Query_entity.append(i)
        all_ops = self.getSubLists(Query_entity, len(Query_entity))
        e_options = self.filter_options(all_ops, q_count)
        result = [{'tokens': query, 'entities': []}]
        for i in range(len(e_options)):
            k = query.copy()
            e = []
            for DoE_i in DoE:
                if DoE_i in e_options[i]:
                    e.append(DoE_i)
            e_tmp = []
            for j in e:
                e_tmp.extend(j.split())
            for word in e_tmp:
                k.remove(word)
            result.append({'tokens': k, 'entities': e})
        return result

    ## Your implementation to return the max score among all the query splits...
    def max_score_query(self, query_splits, doc_id):
        max_score = 0
        result = []
        for i in query_splits:
            k, e, tokens_score, entities_score = i['tokens'], i['entities'], 0, 0
            for h in k:
                if h in self.idf_tokens and doc_id in self.idf_tokens[h]:
                    tokens_score += self.idf_tokens[h][doc_id]
            for j in e:
                if j in self.idf_entities and doc_id in self.idf_entities[j]:
                    entities_score += self.idf_entities[j][doc_id]
            combined_score = entities_score + tokens_score * 0.4
            if combined_score > max_score:
                max_score = combined_score
                max_query = i
            # result.append([combined_score, i])
        return (max_score, max_query)
        ## Output should be a tuple (max_score, {'tokens': [...], 'entities': [...]})