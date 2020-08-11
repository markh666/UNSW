import os,re;
from flask import Flask, render_template, session, request,url_for, Response;
import sys;
import json;
import numpy as np
from sklearn.preprocessing import MinMaxScaler,normalize
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3");

app = Flask(__name__)

# clean the data
def clean():
    f = open('processed.cleveland.data','r')
    data = f.read()
    rows = data.split('\n')
    clean_data = []
    for row in rows:
        if re.search(r'\?',row):
            continue;
        else:
            split_row = row.split(",")
            if (split_row != ['']):
                clean_data.append(split_row)
    return clean_data

# Part 2 Head --------------------------------------------------------------------------------------------------------------
def potential_factors():
    data = clean()
    x = []
    label = []
    for i in data:
        x.append([float(j) for j in i[:-1]])
        if i[-1] != '0':
            label.append(1)
        else:
            label.append(i[-1])
    attributes = ['age','sex','chest pain type','resting blood pressure','serum cholestoral in mg/dl',\
                  'fasting blood sugar > 120 mg/dl','resting electrocardiographic results','maximum heart rate achieved',\
                  'exercise induced angina','oldpeak','the slope of the peak exercise ST segment','number of major vessels (0-3) colored by flourosopy',\
                  'thal(Thalassemia)']

    rfc = RandomForestClassifier(random_state = 13)
    rfc.fit(x,label)
    l = rfc.feature_importances_
    data_dic = {attributes[i]:l[i] for i in range(len(l))}
    sorted_data_list = sorted(data_dic.items(), key=lambda k: k[1])
    sorted_data_dic ={i[0]:i[1]  for i in sorted_data_list}
    plot_attributes = [i for i in sorted_data_dic.keys()]
    plot_value = [i for i in sorted_data_dic.values()]
    plt.figure(figsize=(15,10))
    plt.title('Feature Importances')
    plt.barh(range(len(plot_value)), plot_value,tick_label = plot_attributes)
    plt.xlabel('Relative Importance Score')
    plt.subplots_adjust(left=0.35,wspace=0.35, hspace=0.35,bottom=0.13, top=0.91)
    plt.savefig('./static/pictures/feature_importance.png')
# Part 2 Tail --------------------------------------------------------------------------------------------------------------


# Part 3 Track Two Head --------------------------------------------------------------------------------------------------------------
@app.route('/result', methods=['GET','POST'])
def get():
    # 从 Form 读取用户输入的结果， 除了{age,resting blood pressure,serum cholestoral,oldpeak} ，其他必须输入，如果用户没有输入，用 '*' 代替。
    # 将 list 传给 predic(list)
    age = request.form.get('age')
    sex = request.values.get('sexual')
    chest = request.values.get('chest')
    pressure = request.form.get('pressure')
    ser = request.form.get('ser')
    bs = request.values.get('bs')
    rer = request.values.get('rer')
    mh = request.form.get('mh')
    eia = request.values.get('eia')
    oldpeak = request.form.get('o')
    s = request.values.get('s')
    v = request.values.get('v')
    thal = request.values.get('thal')

    
    user_input=[age,sex,chest,pressure,ser,bs,rer,mh,eia,oldpeak,s,v,thal]
    print(user_input)
    result = predic(user_input)
    #result 会得到 0/1 两种结果

    return render_template('result.html',result = result);

def predic(user_input):
    data = clean()
    x = []
    label = []
    for i in data:
        x.append([float(j) for j in i[:-1]])
        if i[-1] != '0':
            label.append(1)
        else:
            label.append(i[-1])

    np_data = np.array(data,dtype='float')
    np_mean_data = np.mean(np_data,axis=0)
    user_data = []
    for i in range(len(user_input)):
        if user_input[i] == '':
            user_data.append(np_mean_data[i])
        else:
            user_data.append(user_input[i])
    rfc = RandomForestClassifier()
    rfc.fit(x,label)
    return int(rfc.predict([user_data])[0])

# Part 3 Track Two Tail --------------------------------------------------------------------------------------------------------------



# Homepage
@app.route('/', methods=['GET','POST'])
@app.route('/home.html', methods=['GET','POST'])
def home():
	return render_template('home.html');
	

if __name__ == '__main__':
    potential_factors()
    app.secret_key = os.urandom(12) 
    app.run(port=5000,debug=True)