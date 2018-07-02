import CompetitionHandler as ch
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson.objectid import ObjectId
import math
import os
import copy
import datetime

ip = '85.191.252.150'
port = 32773

app = Flask(__name__)
CORS(app, support_credentials=True)

filepath = os.path.dirname(os.path.realpath(__file__))

icehorse = ch.SportiImporter(filepath + '\\..\\Data\\us1_final.xlsx')

@app.route('/drop-all')
def drop_all():
    MongoClient(ip, port).IcehorseDB.tests.delete_many({})
    return jsonify(True)

@app.route('/get-tests/<state>/<track>')
@cross_origin(support_credentials=True)
def get_tests(state, track):
    client = MongoClient(ip, port)
    if state == 'unassigned' or track == '':
        all_tests = client.IcehorseDB.tests.find({'state': state})
    else:
        time = datetime.datetime.utcfromtimestamp(int(state)/1000)
        all_tests = client.IcehorseDB.tests.find({'state': time, 'track': track})
    client.close()
    testlist = ()
    for test in all_tests:
        test["_id"] = str(test["_id"])
        testlist += (test,)

    return jsonify(testlist)

@app.route('/reload-file/<competition_id>')
@cross_origin(support_credentials=True)
def reload(competition_id):
    client = MongoClient(ip,port)
    settings = client.IcehorseDB.competition_setup.find_one({"_id": ObjectId(competition_id)})
    icehorse = ch.SportiImporter(filepath + '\\..\\Data\\' + settings['import_path'])
    icehorse.load_file()
    icehorse.get_tests()
    return get_tests('unassigned', '')

@app.route('/<test>/toggle-<x>-final')
@cross_origin(support_credentials=True)
def toggle_final(test, x):
    client = MongoClient(ip, port)
    test_db = client.IcehorseDB.tests.find_one({'_id': ObjectId(test)})
    if x == 'a':
        test_db['hasAfinal'] = not test_db['hasAfinal']
        if test_db['hasAfinal']:
            print (test_db['base_test'])
            icehorse.create_final(test_db['base_test'], x, test)
        else:
            icehorse.remove_final(test_db['testcode'], x)

    elif x == 'b':
        test_db['hasBfinal'] = not test_db['hasBfinal']

        if test_db['hasBfinal']:
            icehorse.create_final(test_db['base_test'], x, test)
        else:
            icehorse.remove_final(test_db['testcode'], x)

    client.IcehorseDB.tests.replace_one({'_id': ObjectId(test)}, test_db)
    client.close()

    test_db.pop('_id')

    return jsonify(test_db)

@app.route('/<testcode>/<phase>/<int:section>/save/<state>/<start_block>/<int:start>/<int:end>/<string:track>')
@cross_origin(support_credentials=True)
def save(testcode, phase, section, state, start_block, start, end, track):
    client = MongoClient(ip, port)
    test_db = client.IcehorseDB.tests.find_one({'testcode': testcode.upper(), 'phase': phase, 'section': section})
    if test_db == None:
        test_db = client.IcehorseDB.tests.find_one({'testcode': testcode, 'phase': phase, 'section': section})

    prev_start = copy.copy(test_db['start'])
    prev_state = copy.copy(test_db['state'])

    if state == 'unassigned':
        test_db['state'] = state
        test_db['start_block'] = 0
        test_db['start'] = 0
        test_db['end'] = 0
        test_db['track'] = ''
    else:
        state = int(state)
        state = datetime.datetime.utcfromtimestamp(state/1000)
        start = datetime.datetime.utcfromtimestamp(start/1000)
        end = datetime.datetime.utcfromtimestamp(end/1000)
        test_db['state'] = state
        test_db['start_block'] = start_block
        test_db['start'] = start
        test_db['end'] = end
        test_db['track'] = track

    replace = client.IcehorseDB.tests.replace_one({'testcode': testcode.upper(), 'phase': phase, 'section': section}, test_db)
    if replace.modified_count < 1:
        client.IcehorseDB.tests.replace_one({'testcode': testcode, 'phase': phase, 'section': section}, test_db)

    judges = client.IcehorseDB.judges.find({
        'tests': {
            '$elemMatch': {
                'testcode': testcode.upper(),
                'phase': phase,
                'start': prev_start
            }
        }
    },{
        'fname': 1,
        'lname': 1,
        'status': 1,
        'tests': {
            '$elemMatch': {'date': prev_state}
        },
        'times': {
            '$elemMatch': {'date': prev_state}
        }
    })

    for judge in judges:
        judge_obj = ch.Judge(judge['fname'], judge['lname'])
        judge_obj.update_tests(testcode, start, end, test_db['prel_time'], state, prev_start, track)
        judge_obj.calculate_time(state)
        judge_obj.calculate_time(prev_state)
        judge_obj.update()

    test_db.pop('_id')
    client.close()
    return jsonify(test_db)

@app.route('/settings/<competition_id>')
@cross_origin(support_credentials=True)
def get_settings(competition_id):
    client = MongoClient(ip, port)
    settings = client.IcehorseDB.competition_setup.find_one({"_id": ObjectId(competition_id) })
    client.close()

    settings["_id"] = str(settings["_id"])

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
    new_section['right_rein'] = test_doc['right_rein'] - right * test_doc['riders_per_heat']
    new_section['left_rein'] = test_doc['left_rein'] - left * test_doc['riders_per_heat']
    new_section['left_heats'] = math.ceil(new_section['left_rein'] / new_section['riders_per_heat'])
    new_section['right_heats'] = math.ceil(new_section['right_rein'] / new_section['riders_per_heat'])
    new_section['section'] = highest_id + 1
    new_section['prel_time'] = (new_section['left_heats'] + new_section['right_heats']) * new_section['time_per_heat']
    new_section['state'] = 'unassigned'
    new_section.pop('_id')
    client.IcehorseDB.tests.insert_one(new_section)

    test_doc['left_rein'] = left * test_doc['riders_per_heat']
    test_doc['right_rein'] = right * test_doc['riders_per_heat']
    test_doc['left_heats'] = math.ceil(test_doc['left_rein'] / test_doc['riders_per_heat'])
    test_doc['right_heats'] = math.ceil(test_doc['right_rein'] / test_doc['riders_per_heat'])
    test_doc['prel_time'] = (test_doc['left_heats'] + test_doc['right_heats']) * test_doc['time_per_heat']
    client.IcehorseDB.tests.replace_one(match_doc, test_doc)
    new_section.pop('_id')
    
    client.close()
    test_doc.pop('_id')

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

@app.route('/set-judge/<fname>/<lname>/<testcode>/<phase>/<date>/')
@cross_origin(support_credentials=True)
def set_judge(fname, lname, testcode, phase, date):
    judge = ch.Judge(fname, lname)
    client = MongoClient(ip, port)
    tests = client.IcehorseDB.tests.find({
        'testcode': testcode,
        'phase': phase
    })
    client.close()
    for test in tests:
        judge.tests.append({
            'testcode': testcode.upper(),
            'phase': phase,
            'date': datetime.datetime.utcfromtimestamp(int(date)/1000),
            'start': test['start'],
            'end': test['end'],
            'time': test['prel_time'],
            'track': test['track']
        })
    judge.calculate_time(date)
    judge.update()
    return jsonify(judge.to_tuple())

@app.route('/unset-judge/<fname>/<lname>/<testcode>/<phase>/<date>/')
@cross_origin(support_credentials=True)
def unset_judge(fname, lname, testcode, phase, date):
    judge = ch.Judge(fname, lname)
    client = MongoClient(ip, port)
    tests = client.IcehorseDB.tests.find({
        'testcode': testcode,
        'phase': phase
    })
    client.close()
    for test in tests:
        judge.tests.remove({
            'testcode': testcode.upper(),
            'phase': phase,
            'date': datetime.datetime.utcfromtimestamp(int(date)/1000),
            'start': test['start'],
            'end': test['end'],
            'time': test['prel_time'],
            'track': test['track']
        })
    judge.calculate_time(date)
    judge.update()

    return jsonify(judge.to_tuple())
    
@app.route('/get-judges/')
@cross_origin(support_credentials=True)
def get_judges():
    client = MongoClient(ip, port)
    judges = client.IcehorseDB.judges.find({})

    judge_arr = []
    for judge in judges:
        judge.pop('_id')
        judge_arr += (judge,)

    return jsonify(judge_arr)

@app.route('/update-judge/<fname>/<lname>/<new_fname>/<new_lname>/<new_status>')
@cross_origin(support_credentials=True)
def update_judge(fname, lname, new_fname, new_lname, new_status):
    judge = ch.Judge(fname, lname)
    judge.update_judge_info(new_fname, new_lname, new_status)
    judge.update()

    return jsonify(judge.to_tuple())

@app.route('/get-judges-not-in/<test>/<phase>/')
@cross_origin(support_credentials=True)
def get_judges_not_in_test(test, phase):
    judge_arr = []
    client = MongoClient(ip, port)
    judges = client.IcehorseDB.judges.find()

    client.close()
    for judge in judges:
        if any(t.get('testcode', None) == test and t.get('phase', None) == phase for t in judge['tests']):
            continue
        judge.pop('_id')
        judge_arr += (judge,)

    return jsonify(judge_arr)


@app.route('/get-judges/<test>/<phase>/<int:date>')
@cross_origin(support_credentials=True)
def get_judges_for_test(test, phase, date):
    judge_arr = []
    if type(date) == int:
        client = MongoClient(ip, port)
        judges = client.IcehorseDB.judges.find({
            'tests': {
                '$elemMatch': {
                    'testcode': test.upper(),
                    'phase': phase,
                }
            }
        },{
            'fname': 1,
            'lname': 1,
            'status': 1,
            'tests': {
                '$elemMatch': {'date': datetime.datetime.utcfromtimestamp(int(date)/1000)}
            },
            'times': {
                '$elemMatch': {'date': datetime.datetime.utcfromtimestamp(int(date)/1000)}
            }
        })

        client.close()
        for judge in judges:
            judge.pop('_id')
            judge_arr += (judge,)

    return jsonify(judge_arr)

@app.route('/create_custom/<testcode>/<duration>')
@cross_origin(support_credentials=True)
def create_entry(testcode, duration):
    entry = ch.Test(testcode,0,0)
    entry.phase = 'custom'
    entry.prel_time = duration
    entry.update()

    return jsonify(entry.to_dict())

@app.route('/generate-schedule')
@cross_origin(support_credentials=True)
def generate_schedule():
    test_arr = []
    client = MongoClient(ip, port)

    settings = client.IcehorseDB.competition_setup.find_one()

    test_collection = client.IcehorseDB.tests
    current_day = 0
    current_time = settings['days'][current_day]
    current_block = 0

    try:
        next_test = test_collection.find({'state': 'unassigned'}).sort([('priority', 1)]).limit(1).next()
    except:
        return jsonify("No unassigned tests left...")
    
    while next_test:   
        if next_test['prel_time'] > 120:
            heats_per_two_hour = math.floor(120 / next_test['time_per_heat'])
            if next_test['left_heats'] > heats_per_two_hour:
                left = heats_per_two_hour
                right = 0
            elif next_test['right_heats'] > heats_per_two_hour:
                right = heats_per_two_hour
                left = 0
            else:
                left = math.floor(next_test['left_heats'] / 2)
                right = math.floor(next_test['right_heats'] / 2)

            split(next_test['testcode'], next_test['phase'], next_test['section'], left, right)
            next_test = test_collection.find_one({'testcode': next_test['testcode'], 'phase': next_test['phase'], 'section': next_test['section']})
        
        if current_time.time().minute % 5 != 0:
            rounded_minutes = 5 - (current_time.time().minute % 5)
        else:
            rounded_minutes = 0
        next_test['start'] = current_time + datetime.timedelta(minutes=rounded_minutes)
        next_test['end'] = next_test['start'] + datetime.timedelta(minutes=next_test['prel_time'])

        if str(next_test['priority'])[1] == "3":
            next_test['track'] = 'Pace Track'
        else:
            next_test['track'] = 'Oval Track'
        
        if next_test['end'] > settings['days'][current_day] + datetime.timedelta(hours=settings['hours']):
            current_day += 1
            current_block = 0
            try:
                current_time = settings['days'][current_day]
            except:
                break
            next_test['start'] = current_time
            next_test['end'] = next_test['start'] + datetime.timedelta(minutes=next_test['prel_time'])

        next_test['start_block'] = int(current_block)
        next_test['state'] = settings['days'][current_day]

        blocksize = math.ceil(next_test['prel_time'] / 5)

        current_time = next_test['end'] + datetime.timedelta(minutes=5)
        current_block = next_test['start_block'] + blocksize + 1

        test_collection.replace_one({'testcode': next_test['testcode'].upper(), 'phase': next_test['phase'], 'section': next_test['section']},next_test)

        next_test = test_collection.find_one({'state': 'unassigned', 'testcode': next_test['testcode'], 'phase': next_test['phase']})

        if next_test == None:
            try:
                next_test = test_collection.find({'state': 'unassigned'}).sort([('priority', 1)]).limit(1).next()
            except:
                break

    all_tests = test_collection.find()
    for test in all_tests:
        test.pop('_id')
        test_arr.append(test)

    client.close()
    return jsonify(test_arr)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)