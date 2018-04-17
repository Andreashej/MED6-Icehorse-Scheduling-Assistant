import pandas as pd

class SportiImporter:
    sheet = ""

    def __init__(self, filepath):
        xls = pd.ExcelFile(filepath)
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

class Test:
    testcode = ""
    left_rein = 0
    right_rein = 0

    def __init__(self, tc, lr, rr):
        self.testcode = tc
        self.left_rein = lr
        self.right_rein = rr