import CompetitionHandler as ch
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import math
import os

ip = '85.191.252.150'
port = 32772

app = Flask(__name__)
CORS(app, support_credentials=True)

filepath = os.path.dirname(os.path.realpath(__file__))

# Laptop
# icehorse = ch.SportiImporter('C:\\Users\\ah\\Documents\\MED6-Icehorse-Scheduling-Assistant\\Data\\icetest-liste.xlsx')
# Desktop
icehorse = ch.SportiImporter(filepath + '\\..\\Data\\icetest-liste.xlsx')

@app.route('/get-tests/<state>')
@cross_origin(support_credentials=True)
def get_tests(state):
    client = MongoClient(ip, port)
    all_tests = client.IcehorseDB.tests.find({'state': state})
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
    return get_tests('unassigned')

@app.route('/<test>/toggle-<x>-final')
@cross_origin(support_credentials=True)
def toggle_final(test, x):
    client = MongoClient(ip, port)
    test_db = client.IcehorseDB.tests.find_one({'testcode': test.upper(), 'phase': 'Preliminary'})
    if x == 'a':
        test_db['hasAfinal'] = not test_db['hasAfinal']
        if test_db['hasAfinal']:
            final = icehorse.create_final(test, x)
        else:
            final = icehorse.remove_final(test, x)

    elif x == 'b':
        test_db['hasBfinal'] = not test_db['hasBfinal']

        if test_db['hasBfinal']:
            final = icehorse.create_final(test, x)
        else:
            final = icehorse.remove_final(test, x)

    client.IcehorseDB.tests.replace_one({'testcode': test.upper(), 'phase': 'Preliminary'}, test_db)
    client.close()

    test_db.pop('_id')

    return jsonify(test_db)

@app.route('/<testcode>/<phase>/<int:section>/save/<state>/<start_block>/')
@cross_origin(support_credentials=True)
def save(testcode, phase, section, state, start_block):
    client = MongoClient(ip, port)
    test_db = client.IcehorseDB.tests.find_one({'testcode': testcode.upper(), 'phase': phase, 'section': section})
    test_db['state'] = state
    test_db['start_block'] = start_block
    client.IcehorseDB.tests.replace_one({'testcode': testcode.upper(), 'phase': phase, 'section': section}, test_db)
    test_db.pop('_id')
    client.close()
    return jsonify(test_db)

@app.route('/settings')
@cross_origin(support_credentials=True)
def get_settings():
    client = MongoClient(ip, port)
    test_db = client.IcehorseDB.competition_setup.find()
    client.close()
    settings = ()
    for setting in test_db:
        setting.pop('_id')
        settings += (setting,)

    return jsonify(settings)

@app.route('/get-time/<string:test>/<string:phase>')
@cross_origin(support_credentials=True)
def get_times(test, phase):
    client = MongoClient(ip, port)
    test_doc = client.IcehorseDB.test_times.find_one(
        {
            'phase': phase.lower(),
            'test': test.lower()
        }
    )
    client.close()
    test_doc.pop('_id')
    return jsonify(test_doc)

@app.route('/split/<testcode>/<phase>/<int:section_id>/<int:left>/<int:right>')
@cross_origin(support_credentials=True)
def split(testcode, phase, section_id, left, right):
    match_doc = {
            'phase': phase,
            'testcode': testcode.upper(),
            'section': section_id
        }
    client = MongoClient(ip, port)
    test_doc = client.IcehorseDB.tests.find_one(match_doc)
    new_section = test_doc.copy()

    highest_id = client.IcehorseDB.tests.find({'phase': phase, 'testcode': testcode.upper()}).sort('section', -1).limit(1)[0]['section']

    new_section['left_rein'] = test_doc['left_rein'] - left
    new_section['right_rein'] = test_doc['right_rein'] - right
    new_section['left_heats'] = math.ceil(new_section['left_rein'] / new_section['riders_per_heat'])
    new_section['right_heats'] = math.ceil(new_section['right_rein'] / new_section['riders_per_heat'])
    new_section['section'] = highest_id + 1
    new_section['prel_time'] = (new_section['left_heats'] + new_section['right_heats']) * new_section['time_per_heat']
    new_section['state'] = 'unassigned'
    new_section.pop('_id')

    test_doc['left_rein'] = left
    test_doc['right_rein'] = right
    test_doc['left_heats'] = math.ceil(test_doc['left_rein'] / test_doc['riders_per_heat'])
    test_doc['right_heats'] = math.ceil(test_doc['right_rein'] / test_doc['riders_per_heat'])
    test_doc['prel_time'] = (test_doc['left_heats'] + test_doc['right_heats']) * test_doc['time_per_heat']
    client.IcehorseDB.tests.replace_one(match_doc, test_doc)
    
    client.IcehorseDB.tests.insert_one(new_section)
    client.close()

    new_section.pop('_id')
    
    return jsonify(new_section)

@app.route('/<testcode>/<phase>/join/<int:section_id1>/<int:section_id2>')
@cross_origin(support_credentials=True)
def join(testcode, phase, section_id1, section_id2):
    match_doc1 = {
        'phase': phase,
        'testcode': testcode.upper(),
        'section': section_id1
    }
    match_doc2 = {
        'phase': phase,
        'testcode': testcode.upper(),
        'section': section_id2
    }
    client = MongoClient(ip, port)
    section1 = client.IcehorseDB.tests.find_one(match_doc1)
    section2 = client.IcehorseDB.tests.find_one(match_doc2)

    section1['left_rein'] += section2['left_rein']
    section1['right_rein'] += section2['right_rein']
    section1['left_heats'] += section2['left_heats']
    section1['right_heats'] += section2['right_heats']
    section1['prel_time'] = (section1['left_heats'] + section1['right_heats']) * section1['time_per_heat']
    section1['section'] = min([section1['section'],section2['section']])
    
    client.IcehorseDB.tests.remove(section2)
    client.IcehorseDB.tests.update(match_doc1, section1)
    client.close()

    section1.pop('_id')

    return jsonify(section1)

@app.route('/<testcode>/<phase>/judges/add/<name>')
@cross_origin(support_credentials=True)
def add_judge(testcode, phase, name):
    match = {
        'phase': phase,
        'testcode': testcode.upper(),
    }
    client = MongoClient(ip, port)
    tests = client.IcehorseDB.tests.find(match)
    test_arr = ()
    for test in tests:
        test['judges'].append(name)
        client.IcehorseDB.tests.save(test)

        test.pop('_id')
        test_arr += (test,)

    return jsonify(test_arr)

@app.route('/<testcode>/<phase>/judges/remove/<name>')
@cross_origin(support_credentials=True)
def remove_judge(testcode, phase, name):
    match = {
        'phase': phase,
        'testcode': testcode.upper(),
    }
    client = MongoClient(ip, port)
    tests = client.IcehorseDB.tests.find(match)
    test_arr = ()
    for test in tests:
        test['judges'].remove(name)
        client.IcehorseDB.tests.save(test)
        
        test.pop('_id')
        test_arr += (test,)

    return jsonify(test_arr)

@app.route('/get-judges')
@cross_origin(support_credentials=True)
def get_judges():
    print()


if __name__ == '__main__':
    app.run(debug=True)