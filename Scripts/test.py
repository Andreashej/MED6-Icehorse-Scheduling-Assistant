import CompetitionHandler as ch
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, support_credentials=True)

icehorse = ch.SportiImporter('D:\\Dokumenter\\MED6-Icehorse-Scheduling-Assistant\\Data\\icetest-liste.xlsx')

@app.route('/get-tests')
@cross_origin(support_credentials=True)
def get_tests():
    client = MongoClient('localhost', 27017)
    all_tests = client.IcehorseDB.tests.find()
    client.close()
    testlist = ()
    for test in all_tests:
        test.pop('_id')
        testlist += (test,)

    return jsonify(testlist)

@app.route('/reload-file')
@cross_origin(support_credentials=True)
def reload():
    icehorse.load_file()
    icehorse.get_tests()
    return get_tests()

@app.route('/<test>/toggle-<x>-final')
@cross_origin(support_credentials=True)
def toggle_final(test, x):
    client = MongoClient('localhost', 27017)
    test_db = client.IcehorseDB.tests.find_one({'testcode': test})
    if x == 'a':
        test_db['hasAfinal'] = not test_db['hasAfinal']
    elif x == 'b':
        test_db['hasBfinal'] = not test_db['hasBfinal']
    client.IcehorseDB.tests.replace_one({'testcode': test}, test_db)
    client.close()
    test_db.pop('_id')
    return jsonify(test_db)

@app.route('/<testcode>')
@cross_origin(support_credentials=True)
def get_test(testcode):
    client = MongoClient('localhost', 27017)
    test_db = client.IcehorseDB.tests.find_one({'testcode': testcode})
    client.close()
    test_db.pop('_id')
    return jsonify(test_db)

@app.route('/settings')
@cross_origin(support_credentials=True)
def get_settings():
    client = MongoClient('localhost', 27017)
    test_db = client.IcehorseDB.competition_setup.find()
    client.close()
    settings = ()
    for setting in test_db:
        setting.pop('_id')
        settings += (setting,)

    return jsonify(settings)

if __name__ == '__main__':
    app.run(debug=True)