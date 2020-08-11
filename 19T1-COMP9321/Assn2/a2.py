'''
COMP9321 2019 Term 1 Assignment Two Code Template
Student Name: YU HAN
Student ID: z5219071
'''

import json, sqlite3, time, requests, random
from flask import Flask, request
from flask_restplus import Api, Resource, fields, inputs, reqparse

db_file = 'data.db'

app = Flask(__name__)
#app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api = Api(app,
            default="Collections",
            title="Data Service for World Bank Economic Indicators",
            description="This service will help client to read and store some indicators from Word Bank Economic website")
indicator_model = api.model('Indicator', {'indicator_id': fields.String(required=True)})

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, help='Expected format: top<n> / bottom<n> where n is a integer between 1 to 100')

# random produce collection_id
def random_collection_id():
    d = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    r = random.sample(d, len(d))
    collection_id = ''
    for i in r:
        collection_id += i
    return collection_id

# get the url link
def get_indicator_page(indicator, page):
    return ('http://api.worldbank.org/v2/countries/all/indicators/'+indicator+'?date=2013:2018&format=json&page='+page)

# url = get_indicator_page('NY.GDP.MKTP.CD', '1')

# get the indicator_data set
def get_indicator_data(url):
    r = requests.get(url)
    contents = r.json()
    page = contents[0]['pages']
    indicator_value = contents[1][1]['indicator']['value']
    indicator = contents[1][1]['indicator']['id']
    country = []
    date = []
    value = []
    for i in range(len(contents[1])): 
        country.append(contents[1][i]['country']['value'])
        date.append(contents[1][i]['date'])
        if contents[1][i]['value'] != None:
            value.append(contents[1][i]['value'])
        else:
            value.append(0)
    return page, indicator_value, country, date, value

####### Database Functions ################
def create_entry_table(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Entry(
                    id text,
                    country text,
                    date text,
                    value real
                );""")
    conn.commit()
    conn.close()

def create_db(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Collection(
                    collection_id text PRIMARY KEY,
                    indicator text,
                    indicator_value text,
                    creation_time text
                );""")
    conn.commit()
    conn.close()
    create_entry_table(db_file)

# Check the indicator already exist or not
def indicator_already_exist(indicator_data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Collection 
                    WHERE indicator = "{indicator_data}";
                """)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    if len(result) != 0:
        return True
    else:
        return False

def collection_already_exist(collection):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Collection 
                    WHERE collection_id = "{collection}";
                """)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    if len(result) != 0:
        return True
    else:
        return False

# Insert data to entry table
def insert_entry_data(indicator_data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    #cur.execute(f"""SELECT * FROM Entry WHERE id="{indicator_data[0]}";""")
    #if len(cur.fetchall()) == 0:
    entry = []
    for i in range(len(indicator_data[1])):
        temp = (indicator_data[0], indicator_data[1][i], indicator_data[2][i], indicator_data[3][i])
        entry.append(temp)
    cur.executemany("""INSERT INTO Entry
                (id, country, date, value)
                VALUES(?,?,?,?);""", entry)
    conn.commit()
    conn.close()

# Insert data to collection table
def insert_collection_data(indicator_data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""INSERT INTO Collection
                (collection_id, indicator, indicator_value, creation_time)
                VALUES(?,?,?,?);
            """, indicator_data)
    conn.commit()
    conn.close()

# Select the data from database
def find_indicator(indicator_data):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Collection 
                    WHERE indicator = "{indicator_data}";
                """)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return  result

# Select all data from collection table and order by collection_id
def get_all_data():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Collection ORDER BY collection_id;""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def delete_a_collection(collection):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM Entry WHERE id= "{collection}";""")
    cur.execute(f"""DELETE FROM Collection WHERE collection_id = "{collection}";""")
    conn.commit()
    conn.close()

def get_entry_data(collection_id):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Entry WHERE id="{collection_id}";""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def get_collection_data(collection):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Collection WHERE collection_id="{collection}";""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def retrieve_entry_data(collection_id, year, country):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    sql = f"""SELECT * FROM Entry WHERE id="{collection_id}" AND date="{year}" AND country="{country}";"""
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def get_order_records(collection_id, year, n, order):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    if order == 'top':
        cur.execute(f"""SELECT * FROM Entry WHERE id="{collection_id}" AND date="{year}" ORDER BY value DESC Limit {n};""")
    else:
        cur.execute(f"""SELECT * FROM Entry WHERE id="{collection_id}" AND date="{year}" ORDER BY value Limit {n};""")
    entry = cur.fetchall()
    conn.commit()
    conn.close()
    return entry

def get_data_by_year(collection_id,year):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Entry WHERE id="{collection_id}" AND date={year};""")
    entry = cur.fetchall()
    conn.commit()
    conn.close()
    return entry

def no_collection_in_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Collection""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

######## Api Functions #############
@api.route('/collection')
class CollectionList(Resource):
    # For Q1
    @api.response(200, 'The collection already in the database')
    @api.response(201, 'Collection created successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description='Q1 Import a collection from the data service.')
    @api.expect(indicator_model)
    def post(self):
        body = request.json

        # check the input indicator_id is valid or not
        if 'indicator_id' not in body:
            return {"message": "Missing indicator_id"}, 400

        # check in indicator_id already in the database or not
        indicator = body['indicator_id']
        # If has the data set, return 200
        try:
            if indicator_already_exist(indicator):
                result = find_indicator(indicator)
                return {
                    'location': f"/collections/{str(result[0][0])}",
                    'collection_id': str(result[0][0]),
                    'creation_time': str(result[0][3]),
                    'indicator': int(result[0][1])}, 200

            # If there is no this data, insert the data to database
            else:
                url = get_indicator_page(indicator, '1')  # use the indicator to get url
                page, indicator_value, country, date, value = get_indicator_data(url) # get data from the url
                creation_time = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.localtime(time.time())) # creation time
                collection_id = random_collection_id()  # generate a collection_id
                entries = (collection_id, country, date, value) # collect data for entry table
                insert_entry_data(entries)    # insert data to entry table
                collection_data = (collection_id, indicator, indicator_value, creation_time)    # collect data for collection table
                insert_collection_data(collection_data)   # insert data to collection table
                if page != '1':
                    url_2 = get_indicator_page(indicator, '2')
                    page_2, indicator_value_2, country_2, date_2, value_2 = get_indicator_data(url_2)
                    entries = (collection_id, country_2, date_2, value_2) # collect data for entry table
                    insert_entry_data(entries)    # insert data to entry table
                result = find_indicator(indicator)
                return {
                    'location': f"/collections/{str(result[0][0])}",
                    'collection_id': str(result[0][0]),
                    'creation_time': str(result[0][3]),
                    'indicator': str(result[0][1])}, 201
        except:
            return {'message': "There is no data for this indicator"}, 400

    # For Q3
    @api.response(200, 'Get the collection successfully')
    @api.response(400, 'Unable to get the collection')
    @api.doc(description='Q3 Retrieve the list of available collections')
    def get(self):
        result = no_collection_in_db()
        if len(result) == 0:
            return {'message': 'There is no collection yet, please post one'}, 200
        else:
            result = get_all_data()
            return [{
                    'location': f'/collections/{str(result[i][0])}',
                    'collection_id': str(result[i][0]),
                    'creation_time': str(result[i][3]),
                    'indicator': str(result[i][1])
                } for i in range(len(result))], 200

@api.route('/collection/<string:id>')
@api.param('id', 'collection_id')
class CollectionId(Resource):
    # For Q2
    @api.response(404, 'Collection was not found')
    @api.response(200, 'Successful')
    @api.doc(description='Q2 Delete collection from database')
    #@api.expect(collection_model)
    def delete(self, id):
        try:
            collection_id = id
            if collection_already_exist(collection_id):
                delete_a_collection(collection_id)
                return {'message': f'Collection = {collection_id} is removed from the database!'}, 200
            else:
                return {'message': 'There is no such collection' }, 404
        except:
            return 400

    # For Q4
    @api.response(200, 'Successful')
    @api.response(404, 'Collection was not found')
    @api.doc(description='Q4 Retrieve a collection')
    #@api.expect(collection_model)
    def get(self, id):
        collection_id = id
        try:
            if collection_already_exist(collection_id):
                collection_data = get_collection_data(collection_id)
                entry_data = get_entry_data(collection_id)
                return {
                        'collection_id': collection_id,
                        'indicator': str(collection_data[0][1]),
                        'indicator_value': str(collection_data[0][2]),
                        'creation_time': str(collection_data[0][3]),
                        'entries': [{
                            'country': str(entry_data[i][1]),
                            'date': str(entry_data[i][2]),
                            'value': entry_data[i][3]
                        } for i in range(len(entry_data))]}, 200
            else:
                return {'message': 'There is no such collection' }, 404
        except:
            return 400

@api.route('/collection/<string:id>/<string:year>/<string:country>')
@api.param('id', 'collection id')
@api.param('year', 'year range from 2013-2018 ')
@api.param('country', 'country name')
class EntryData(Resource):
    @api.response(200, 'Successful')
    @api.response(404, 'Collection was not found')
    @api.doc(description='Q5 Retrieve economic indicator value for given country and a year')
    def get(self, id, year, country):
        collection_id = id
        try:
            if collection_already_exist(collection_id):
                collection_data = get_collection_data(collection_id)
                entry_data = retrieve_entry_data(collection_id, year, country)
                return {
                    'collection_id': str(collection_id),
                    'indicator': str(collection_data[0][1]),
                    'country': str(entry_data[0][1]), 
                    'year': str(entry_data[0][2]),
                    'value': entry_data[0][3]
                }, 200
            else:
                return {'message': 'There is no such collection' }, 404
        except:
            return {'message': "Invalid input data"}, 400

@api.route('/collection/<string:id>/<string:year>')
@api.param('id', 'collection id')
@api.param('year', 'year range from 2013-2018')
class TopBottomIndicator(Resource):
    @api.response(200, 'Successful')
    @api.response(404, 'Collection was not found')
    @api.doc(description='Q6 Retrieve top/bottom economic indicator values for a given year')
    def get(self, id, year):
        if not collection_already_exist:
            return {'message': 'There is no such collection' }, 404
        else:
            try:
                args = parser.parse_args()
                query = args.get('q')
                if query[0:3] == 'top':
                    order = 'top'
                    n = int(query[3:])
                else:
                    order = 'bottom'
                    n = int(query[6:])
                entry_data = get_order_records(id, year, n, order)
                collection_data = get_collection_data(id)
                return ({
                    'indicator': str(collection_data[0][1]),
                    'indicator_value': str(collection_data[0][2]),
                    'entries': [{
                        'country': str(entry_data[i][1]),
                        'date': str(entry_data[i][2]),
                        'value': entry_data[i][3]
                    } for i in range(len(entry_data))]
                }), 200
            except:
                entry_data = get_data_by_year(id, year)
                collection_data = get_collection_data(id)
                return ({
                    'indicator': str(collection_data[0][1]),
                    'indicator_value': str(collection_data[0][2]),
                    'entries': [{
                        'country': str(entry_data[i][1]),
                        'date': str(entry_data[i][2]),
                        'value': entry_data[i][3]
                    } for i in range(len(entry_data))]
                }), 200


if __name__ == '__main__':
    create_db(db_file) # connect(create) the database doc
    app.run(debug=True)
