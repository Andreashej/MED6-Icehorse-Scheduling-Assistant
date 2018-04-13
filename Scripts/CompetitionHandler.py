import pandas as pd

class SportiImporter:
    sheet = ""

    def __init__(self, filepath):
        global sheet
        xls = pd.ExcelFile(filepath)
        sheet = xls.parse(0)
        
    def count_test(self, testcode):
        global sheet
        count_left = 0
        count_right = 0

        for t in sheet[testcode]:
            if t == 1:
                count_left = count_left + 1
            elif t == '1L':
                count_left = count_left + 1
            elif t == '1R':
                count_right = count_right + 1
        
        return count_left, count_right

    def get_test_list(self):
        global sheet
        return list(sheet)[7:]

class Test:
    testcode = ""
    left_rein = 0
    right_rein = 0

    def __init__(self, tc, lr, rr):
        global testcode, left_rein, right_rein
        testcode = tc
        left_rein = lr
        right_rein = rr

    def get_testcode(self):
        return testcode
    
    def get_left_rein(self):
        return left_rein
    
    def get_right_rein(self):
        return right_rein