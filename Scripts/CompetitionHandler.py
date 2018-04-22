import pandas as pd
from pymongo import MongoClient

class SportiImporter:
    sheet = ""
    filepath = ""

    def __init__(self, filepath):
        self.filepath = filepath
        self.load_file()
        
    
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
        return list(self.sheet)[7:]
    
    def get_tests(self):
        testlist = tuple()
        for test in self.get_test_list():
            current = Test(test, self.count_test(test)[0], self.count_test(test)[1])
            testlist += current.to_tuple()

        return testlist


class Test:
    testcode = ""
    left_rein = 0
    right_rein = 0
    hasAfinal = False
    hasBfinal = False

    def __init__(self, tc, lr, rr):
        self.testcode = tc
        self.left_rein = lr
        self.right_rein = rr
        client = MongoClient('localhost', 27017)
        db = client.IcehorseDB
        tests = db.tests
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
                'hasBfinal': self.hasBfinal
            },
        )
    
    def to_dict(self):
        return {
            'testcode': self.testcode,
            'left_rein': self.left_rein,
            'right_rein': self.right_rein,
            'hasAfinal': self.hasAfinal,
            'hasBfinal': self.hasBfinal
        }

    def save(self):
        client = MongoClient('localhost', 27017)
        db = client.IcehorseDB
        tests = db.tests
        tests.insert_one(self.to_dict())
        client.close()

    def update(self):
        client = MongoClient('localhost', 27017)
        db = client.IcehorseDB
        test = db.tests
        test.replace_one({'testcode': self.testcode}, self.to_dict())
