import pandas as pd
from pymongo import MongoClient
import math

ip = '85.191.252.150'
port = 32772

class SportiImporter:
    sheet = ""
    filepath = ""
    testlist = []

    def __init__(self, filepath):
        self.filepath = filepath
        self.load_file()
        
    
    def load_file(self):
        MongoClient(ip, port).IcehorseDB.tests.remove({})
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
        return list(self.sheet)[7:]
    
    def get_tests(self):
        testlist = tuple()
        for test in self.get_test_list():
            current = Test(test, self.count_test(test)[0], self.count_test(test)[1])
            testlist += current.to_tuple()
            self.testlist.append(current)

        return testlist
    
    def create_final(self, testcode, phase):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        collection = db.tests
        times = db.test_times

        test = collection.find_one({
            'testcode': testcode.upper(),
            'phase': 'Preliminary'
        })

        final = test.copy()
        final['phase'] = (phase + 'fin').lower()
        final['prel_time'] = times.find_one({
            'test': testcode.lower(),
            'phase': final['phase'].lower()
        })['time']
        final['left_rein'] = 1
        final['right_rein'] = 0
        final['left_heats'] = 1
        final['right_heats'] = 0
        final['state'] = 'unassigned'
        final['section'] = 0
        final['start_block'] = 0
        final.pop('_id')
        collection.insert_one(final)

        final.pop('_id')
        return(final)

    def remove_final(self, testcode, phase):
        client = MongoClient(ip, port)
        db = client.IcehorseDB
        collection = db.tests

        deleted = collection.remove({
            'testcode': testcode.upper(),
            'phase': (phase + 'fin').lower()
        })
        client.close()
        return(deleted)

class Test:

    def __init__(self, tc, lr, rr):
        self.testcode = tc
        self.left_rein = lr
        self.right_rein = rr
        self.sections = []
        self.start_block = 0
        self.state = 'unassigned'
        self.hasAfinal = False
        self.hasBfinal = False
        self.judges = []

        client = MongoClient(ip, port)
        db = client.IcehorseDB
        tests = db.tests
        times = db.test_times
        test_info = times.find_one({
            'test': self.testcode.lower(),
            'phase': 'prel'
        })
        self.riders_per_heat = test_info['riders_per_heat']
        self.time_per_heat = test_info['time']
        self.phase = 'Preliminary'
        self.section_id = 0
        self.left_heats = math.ceil(self.left_rein / self.riders_per_heat)
        self.right_heats = math.ceil(self.right_rein / self.riders_per_heat)
        self.prel_time = (self.left_heats + self.right_heats) * self.time_per_heat
        self.expected_judges = test_info['expected_judges']

        client.close()
        if tests.find_one({'testcode': self.testcode}):
            self.update()
        else:
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
                'judges': self.judges,
                'expected_judges': self.expected_judges
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
            'judges': self.judges,
            'expected_judges': self.expected_judges
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
