## import modules here 

################# Question 1 #################
def build_dic(dic_prev,dic_output,sms):
    sms = set(sms)
    sms = list(sms)
    for i in range(len(sms)):
        if sms[i] in dic_prev.keys():
            if sms[i] in dic_output.keys():
                dic_output[sms[i]] += dic_prev[sms[i]]
            else:
                dic_output[sms[i]] = dic_prev[sms[i]]
        else:
            if sms[i] not in dic_output.keys():
                dic_output[sms[i]] = 0
    return dic_output

def get_count(dic):
    count=0
    for i in dic.keys():
        count += dic[i]
    return count

def probability(dic, count, vocabulary,sms):
    p = 1
    v = len(vocabulary)
    for i in dic.keys():
        if i not in vocabulary:
            continue
        p *= ((dic[i] + 1) / (count + v))**sms.count(i)
    return p

def get_vocabulary(training_data, vocabulary):
    for i in training_data.keys():
        if i not in vocabulary:
            vocabulary.add(i)
    return vocabulary

def multinomial_nb(training_data, sms):
    ham_dic = {}
    spam_dic = {}
    count_ham = 0
    count_spam = 0
    vocabulary = set()
    p_h = 0
    p_s = 0
    for i in range(len(training_data)):
        if training_data[i][1] == "ham":
            ham_dic = build_dic(training_data[i][0], ham_dic, sms)
            count_1 = get_count(training_data[i][0])
            vocabulary = get_vocabulary(training_data[i][0], vocabulary)
            count_ham += count_1
            #print(f"ham:{count_ham}", ham_dic)
            p_h += 1
        else:
            spam_dic =  build_dic(training_data[i][0], spam_dic, sms)
            count_2 = get_count(training_data[i][0])
            vocabulary = get_vocabulary(training_data[i][0], vocabulary)
            count_spam += count_2
            p_s += 1
    #print(f"ham:{count_ham}",ham_dic)
    #print(f"spam:{count_spam}", spam_dic)
    a = probability(ham_dic, count_ham, vocabulary,sms)
    b = probability(spam_dic, count_spam, vocabulary, sms)
    #print("h:",p_h, "s:",p_s)
    #print(f"ham:{count_ham}",ham_dic)
    #print(f"spam:{count_spam}", spam_dic)
    return (p_s*b)/(p_h*a)
