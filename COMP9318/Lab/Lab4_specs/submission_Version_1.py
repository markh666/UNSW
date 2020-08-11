
import pandas as pd
############### Question 1 #################

sms = 'I am not spam'
raw_data = pd.read_csv('./asset/data.txt', sep='\t')
raw_data.head()

def tokenize(sms):
    return sms.split(' ')

def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1

    return tokens

training_data = []
for index in range(len(raw_data)):
    training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))



sms = tokenize(sms)
c_ham=0
c_spam=0
L_spam = 0
L_count = []
L_ham = 0
spam_list = [0]*len(sms)
ham_list = [0]*len(sms)
for tup in training_data:
    if tup[1]=='ham':
        c_ham=c_ham+1

        for key,value in tup[0].items():
            L_ham += tup[0][key]
            for i in range(len(sms)):
                if sms[i] == key:
                    ham_list[i] += value
            if key not in L_count:
                L_count.append(key)
    else:
        c_spam=c_spam+1
        for key,value in tup[0].items():
            L_spam += tup[0][key]
            for j in range(len(sms)):
                if sms[j] == key:
                    spam_list[j] += value
            if key not in L_count:
                L_count.append(key)
Pcj = c_spam/c_ham
number_of_vocab = len(L_count)
print(Pcj)

for i in range(len(spam_list)):
    if spam_list[i] == 0 and ham_list[i] == 0:
        continue
    else:
        P_ham = (ham_list[i]+1)/(L_ham + number_of_vocab)
        P_spam = (spam_list[i]+1)/(L_spam + number_of_vocab)
        answer = P_spam/P_ham
        print(answer)
        Pcj *= answer



print(L_ham)
print(number_of_vocab)
print(L_spam)
print(spam_list)
print(ham_list)
print(Pcj)



#print(multinomial_nb(training_data, tokenize(sms))
