import pandas as pd
import numpy as np
import csv

def q1():
    df = pd.read_csv("accidents_2017.csv", index_col = False)
    result = df.columns.values.tolist()
    
    def print_title(result):
        output = ''
        index = 0
        for string in result:
            index += 1
            string = string.strip()
            for i in string:
                if i == ' ':
                    string = '"' + string + '"'
                    break
            output = output + string
            if index < len(result):
                output += ' '
        print(output)
        
    def print_data():
        row_count = 0
        for index, row in df.iterrows():
            output = ''
            column_count = 0
            row_count += 1
            if row_count > 10:
                break
            else:
                for column in df:
                    column_count += 1
                    temp = str(row[column]).strip()
                    if ord(temp[0]) > 96 and ord(temp[0]) < 123:
                        if temp[1] == "'" or (temp[0]=='l' and temp[1]=='a') or (temp[0]=='d' and temp[1]=='e'):
                            break
                        else:
                            temp = temp.capitalize()
                    flag = False
                    for i in range(len(temp)):
                        if temp[i] == ' ':
                            if ord(temp[i+1]) > 96 and ord(temp[i+1]) < 123: 
                                if temp[i+1:i+4]=="l'a":
                                    mid = "l'A"
                                    temp = temp[:i+1]+mid+temp[i+4:]
                                elif temp[i+2] != "'" and not (temp[i+1]=='l' and temp[i+2]=='a') and not (temp[i+1]=='d' and temp[i+2]=='e' and temp[i+3]==' '):
                                    mid = (chr(ord(temp[i+1])-32))
                                    temp = temp[:i+1]+mid+temp[i+2:]
                            if not flag:
                                temp = '"' + temp + '"'
                                flag = True

                    if column_count == 14:
                        if len(temp) > 9:
                            temp = str(round(float(temp), 8))
                    if column_count < 15:
                        output = output + temp + ' '

            if len(temp) > 11:
                temp = str(round(float(temp), 8))

            output += temp
            print(output)
            
    print_title(result)
    print_data()

def q2():
    df = pd.read_csv('accidents_2017.csv')
    df = df.dropna(subset=['District Name', 'Neighborhood Name']).drop_duplicates(subset='Id', keep='last')
    df_2 = df[~ df['District Name'].str.contains('Unknown')]
    df_2 = df_2[~ df_2['Neighborhood Name'].str.contains('Unknown')]
    result = df_2.columns.values.tolist()
    output = []
    for string in result:
            output.append(string)
    content_list = []
    for index, row in df_2.iterrows():
        column_count = 0
        row_list = []
        for column in df_2:
            mid = str(row[column]).strip()
            if column == 'Neighborhood Name' or column == 'Street':
                if ord(mid[0]) > 96 and ord(mid[0]) < 123:
                    if mid[1] != "'" and mid[:2] != 'la' and mid[:2] != 'de':
                        mid = mid.capitalize()
                for i in range(len(mid)):
                    if mid[i] == ' ' and ord(mid[i+1]) > 96 and ord(mid[i+1]) < 123:
                        if mid[i+1:i+4] == "l'a":
                            middle = "l'A"
                            mid = mid[:i+1]+middle+mid[i+4:]
                        elif mid[i+2] != "'" and mid[i+1:i+3] != 'la' and mid[i+1:i+4] != 'de ':
                            middle = (chr(ord(mid[i+1])-32))
                            mid = mid[:i+1]+middle+mid[i+2:]
            if column == 'Longitude' and len(mid) > 9:
                mid = str(round(float(mid), 8))
            if column == 'Latitude' and len(mid) > 11:
                mid = str(round(float(mid), 8))
            row_list.append(mid)
        content_list.append(row_list)
    with open("result_q2.csv","w") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(output)
        writer.writerows(content_list)
    csvfile.close()

def q3():
    df = pd.read_csv('accidents_2017.csv')
    df = df.dropna().drop_duplicates(subset='Id', keep='last')
    df_2 = df[~ df['District Name'].str.contains('Unknown')]
    df_2 = df_2[~ df_2['Neighborhood Name'].str.contains('Unknown')]
    f = df_2.groupby("District Name")["District Name"].size().sort_values(ascending = False).reset_index(name='Total numbers of accidents')
    result = f.columns.values.tolist()
    def print_name():
        output = ''
        index = 0
        for string in result:
            for i in string:
                if i == ' ':
                    string = '"' + string + '"'
                    break
            output += string
            if index < len(result)-1:
                output += ' '
                index += 1
        print(output)
    def print_result():
        for index, row in f.iterrows():
            output = ''
            count = 0
            for column in f:
                count += 1
                temp = str(row[column]).strip()
                for i in temp:
                    if i==' ':
                        temp = '"' + temp + '"'
                        break
                if count < 2:
                    output = output + temp + ' '
            output += temp
            print(output)
    print_name()
    print_result()

def q4():
    #Q4.1
    with open('air_stations_Nov2017.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        station = [row['Station'] for row in reader]
    with open('air_stations_Nov2017.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        district = [row['District Name'] for row in reader]
    groups = '['
    for i in range(len(station)-1):
        groups += ("{"+'"Station"'+":"+'"'+station[i].title()+'"'+","+'"District Name"'+":"+'"'+district[i].title()+'"'+"}"+',')
    i = len(station)-1
    groups += ("{"+'"Station"'+":"+'"'+station[i].title()+'"'+","+'"District Name"'+":"+'"'+district[i].title()+'"'+"}"+']')
    print(groups)
    
    #Q4.2
    df = pd.read_csv('air_quality_Nov2017.csv')
    df = df.dropna(subset=['Air Quality'])
    df = df[~ df['Air Quality'].str.contains('--')]
    df = df[~ df['Air Quality'].str.contains('Good')].head(10)
    result = df.columns.values.tolist()
    def print_title():
            output = ''
            index = 0
            for string in result:
                index += 1
                string = string.strip()
                for i in string:
                    if i == ' ':
                        string = '"' + string + '"'
                        break
                output = output + string
                if index < len(result):
                    output += ' '
            print(output)
    def print_result():
        for index, row in df.iterrows():
            output = ''
            count = 0
            for column in df:
                count += 1
                temp = str(row[column]).strip()
                for i in temp:
                    if i==' ':
                        temp = '"' + temp + '"'
                        break
                if count < 15:
                    output = output + temp + ' '
            output += temp
            print(output)
    print_title()
    print_result()
    
    #Q4.3
    df_3 = pd.read_csv('air_quality_Nov2017.csv')
    df_3 = df_3.dropna(subset=['Air Quality'])
    df_3 = df_3[~ df_3['Air Quality'].str.contains('--')]
    df_3 = df_3[~ df_3['Air Quality'].str.contains('Good')]
    day = []
    hour = []
    district = []
    for i in df_3['Generated']:
        day.append(i[:2])
        if len(i) == 15:
            hour.append(i[11])
        else:
            hour.append(i[11:13])
    for i in df_3['Station']:
        district.append(i[12:])

    df_accident = pd.read_csv('accidents_2017.csv')
    df_accident = df_accident.drop_duplicates(subset='Id', keep='last')
    result = df_accident.columns.values.tolist()
    output = []

    for string in result:
            output.append(string)

    content_list = []
    for i in range(len(district)):
        temp = df_accident[(df_accident['Month']=='November') & (df_accident['District Name']==district[i]) & (df_accident['Day']==int(day[i])) & (df_accident['Hour']==int(hour[i]))]
        for index, row in temp.iterrows():
            column_count = 0
            row_list = []
            for column in temp:
                mid = str(row[column]).strip()
                if column == 'Neighborhood Name' or column == 'Street':
                    if ord(mid[0]) > 96 and ord(mid[0]) < 123:
                        if mid[1] != "'" and mid[:2] != 'la' and mid[:2] != 'de':
                            mid = mid.capitalize()
                    for i in range(len(mid)):
                        if mid[i] == ' ' and ord(mid[i+1]) > 96 and ord(mid[i+1]) < 123:
                            if mid[i+1:i+4] == "l'a":
                                middle = "l'A"
                                mid = mid[:i+1]+middle+mid[i+4:]
                            elif mid[i+2] != "'" and mid[i+1:i+3] != 'la' and mid[i+1:i+4] != 'de ':
                                middle = (chr(ord(mid[i+1])-32))
                                mid = mid[:i+1]+middle+mid[i+2:]
                if column == 'Longitude' and len(mid) > 9:
                    mid = str(round(float(mid), 8))
                if column == 'Latitude' and len(mid) > 11:
                    mid = str(round(float(mid), 8))
                row_list.append(mid)
            content_list.append(row_list)
    #print(content_list)
    #print(len(content_list))
    with open("result_q4.csv","w") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(output)
        writer.writerows(content_list)
    csvfile.close()