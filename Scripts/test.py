import CompetitionHandler as ch

testlist = list()

icehorse = ch.SportiImporter('C:\\Users\\ah\\Documents\\MED6-Icehorse-Scheduling-Assistant\\Data\\icetest-liste.xlsx')

for test in icehorse.get_test_list():
    testlist.append(
        ch.Test(
            test, 
            icehorse.count_test(test)[0], 
            icehorse.count_test(test)[1]
        )
    )