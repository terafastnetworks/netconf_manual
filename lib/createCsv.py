import csv

def csvOutput(testsuiteName, testCase, time, result):
    global cnt
    s = 'ms'
    #o = 'productInformation:\t'
    o = testsuiteName+':\t'
    testCase = o+str(testCase)
    t = str(time)+s
    with open('finalLog.csv', 'a') as f:
        a = csv.writer(f, delimiter = ',')
        data = (testCase, t, result )
        a.writerow(data)

