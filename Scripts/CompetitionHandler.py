import pandas as pd
from pymongo import MongoClient
import math
import datetime
from bson.objectid import ObjectId

ip = '85.191.252.150'
port = 32773

class SportiImporter:

    def __init__(self, filepath):
        self.filepath = filepath
        self.load_file()
        self.testlist = []
        self.sheet = ""
        
    def load_file(self):
        xls = pd.ExcelFile(self.filepath)
        self.sheet = xls.parse(0)
        
    def count_test(self, testcode):
        count_left = 0
        count_right = 0

        for t in self.sheet[testcode]:
            if t == 1:
                count_left = count_left + 1
            elif t == '1L':
                count_left = count_left + 1
            elif t == '1R':
                count_right = count_right + 1
        
        return count_left, count_right

    def get_test_list(self):
        return list(self.sheet)[12:]
    
    def get_tests(self):
        testlist = tuple()
        for test in self.get_test_list():
            current = Test(test, self.count_test(test)[0], self.count_test(test)[1])
            testlist += current.to_tuple()
            self.testlist.append(current)

        return testlist
    
    def create_final(self, base_test, phase, test_id):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        collection = db.tests
        test = collection.find_one({
            "_id": ObjectId(test_id)
        })

        final = test.copy()

        final['phase'] = (phase + 'fin').lower()

        times = db.test_times.find_one({
            'test': base_test.lower(),
            'phase': final['phase'].lower()
        })

        final['prel_time'] = times['time']
        final['left_rein'] = 1
        final['right_rein'] = 0
        final['left_heats'] = 1
        final['right_heats'] = 0
        final['state'] = 'unassigned'
        final['section'] = 0
        final['start_block'] = 0
        final['priority'] = times['priority']
        final.pop('_id')
        collection.insert_one(final)

        final.pop('_id')
        return(final)

    def remove_final(self, testcode, phase):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        collection = db.tests

        deleted = collection.remove({
            "testcode": testcode,
            "phase": (phase + 'fin').lower()
        })
        client.close()
        return(deleted)

class Test:

    def __init__(self, tc, lr, rr, ageclass = "", s=0, yr=0, j=0):
        self.testcode = tc + " " + ageclass
        self.left_rein = lr
        self.right_rein = rr
        self.base_test = tc
        self.senior = s
        self.young_rider = yr
        self.junior = j

        client = MongoClient(ip, port)
        db = client.IcehorseDB
        tests = db.tests
        times = db.test_times
        self.section_id = 0
        try:
            test_info = times.find_one({
                'test': self.base_test.lower(),
                'phase': 'prel'
            })
            self.riders_per_heat = test_info['riders_per_heat']
            self.time_per_heat = test_info['time']
            self.left_heats = math.ceil(self.left_rein / self.riders_per_heat)
            self.right_heats = math.ceil(self.right_rein / self.riders_per_heat)
            self.expected_judges = test_info['expected_judges']
            self.priority = test_info['priority']
            self.phase = 'Preliminary'
        except:
            self.riders_per_heat = 0
            self.time_per_heat = 0
            self.left_heats = 0
            self.right_heats = 0
            self.expected_judges = 0
            self.priority = 999
            self.phase = 'custom'

        self.prel_time = (self.left_heats + self.right_heats) * self.time_per_heat
        client.close()
        test = tests.find_one({'testcode': self.testcode, 'phase': self.phase, 'section': self.section_id})
        if test:
            self.state = test['state']
            self.track = test['track']
            self.start_block = test['start_block']
            self.hasAfinal = test['hasAfinal']
            self.hasBfinal = test['hasBfinal']
            self.start = test['start']
            self.end = test['end']
            self.update()
        else:
            self.state = 'unassigned'
            self.track = ''
            self.start_block = 0
            self.hasAfinal = False
            self.hasBfinal = False
            self.start = 0
            self.end = 0
            self.save()
    
    def to_tuple(self):
        return (
            {
                'testcode': self.testcode,
                'left_rein': self.left_rein,
                'right_rein': self.right_rein,
                'hasAfinal': self.hasAfinal,
                'hasBfinal': self.hasBfinal,
                'riders_per_heat': self.riders_per_heat,
                'time_per_heat': self.time_per_heat,
                'prel_time': self.prel_time,
                'phase': self.phase,
                'state': self.state,
                'start_block': self.start_block,
                'section': self.section_id,
                'left_heats': self.left_heats,
                'right_heats': self.right_heats,
                'expected_judges': self.expected_judges,
                'start': self.start,
                'end': self.end,
                'priority': self.priority,
                'track': self.track,
                'base_test': self.base_test
            },
        )
    
    def to_dict(self):
        return {
            'testcode': self.testcode,
            'left_rein': self.left_rein,
            'right_rein': self.right_rein,
            'hasAfinal': self.hasAfinal,
            'hasBfinal': self.hasBfinal,
            'riders_per_heat': self.riders_per_heat,
            'time_per_heat': self.time_per_heat,
            'prel_time': self.prel_time,
            'phase': self.phase,
            'state': self.state,
            'start_block': self.start_block,
            'section': self.section_id,
            'left_heats': self.left_heats,
            'right_heats': self.right_heats,
            'expected_judges': self.expected_judges,
            'start': self.start,
            'end': self.end,
            'priority': self.priority,
            'track': self.track,
            'base_test': self.base_test
            
        }

    def save(self):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        tests = db.tests
        tests.insert_one(self.to_dict())
        client.close()

    def update(self):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        test = db.tests
        test.replace_one({'testcode': self.testcode, 'phase': self.phase, 'section': self.section_id}, self.to_dict())

class Judge:
    def __init__(self, fname, lname):
        client = MongoClient(ip, port)
        judges = client.IcehorseDB.judges
        curr_judge = judges.find_one({'fname': fname, 'lname': lname})
        
        if curr_judge != None:
            self.fname = curr_judge['fname']
            self.lname = curr_judge['lname']
            self.status = curr_judge['status']
            self.tests = curr_judge['tests']
            self.times = curr_judge['times']
        else:
            self.fname = fname
            self.lname = lname
            self.status = 'unknown'
            self.tests = []
            self.times = []
        client.close()

    def update_judge_info(self, new_fname, new_lname, new_status):
        client = MongoClient(ip, port)
        judge = client.IcehorseDB.judges.find_one({'fname': self.fname, 'lname': self.lname})
        self.fname = new_fname
        self.lname = new_lname
        self.status = new_status

        if judge:
            client.IcehorseDB.judges.replace_one(judge, self.to_dict())
        else:
            self.save()
        client.close()

    def update_tests(self, testcode, start, end, time, date, prev_start, track):
        test = self.tests[self.tests.index(next((test for test in self.tests if test['testcode'] == testcode and test['start'] == prev_start)))]
        test['date'] = date
        test['start'] = start
        test['end'] = end
        test['time'] = time
        test['track'] = track

    def calculate_time(self, date):
        try:
            date = datetime.datetime.utcfromtimestamp(int(date)/1000)
        except:
            print('unassigned')
        client = MongoClient(ip, port)
        time = 0
        starts = []
        ends = []
        start = 0
        end = 0

        if len(self.tests) > 0:
            for tests in self.tests:
                if tests['date'] == date:
                    starts.append(tests['start'])
                    ends.append(tests['end'])
                    time += tests['time']
            
            if len(starts) > 0:
                start = min(starts)

            if len(ends) > 0:
                end = max(ends)

        client.close()

        if any(t.get('date', None) == date for t in self.times):
            self.times[self.times.index(next((day for day in self.times if day['date'] == date)))] = {
                'date': date,
                'time': time,
                'start': start,
                'end': end
            }
        else:
            self.times.append(
                {
                    'date': date,
                    'time': time,
                    'start': start,
                    'end': end
                }
            )

    def to_dict(self):
        return {
            'fname': self.fname,
            'lname': self.lname,
            'status': self.status,
            'tests': self.tests,
            'times': self.times
        }
    
    def to_tuple(self):
        return (
            {
                'fname': self.fname,
                'lname': self.lname,
                'status': self.status,
                'tests': self.tests,
                'times': self.times
            },
        )
    
    def save(self):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        judges = db.judges
        judges.insert_one(self.to_dict())
        client.close()
    
    def update(self):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        judges = db.judges
        replace = judges.replace_one({'lname': self.lname, 'fname': self.fname}, self.to_dict())
        client.close()

        if replace.modified_count < 1:
            self.save()
