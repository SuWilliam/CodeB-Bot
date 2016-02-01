import sys
import pprint
import time
import socket
import sys 
    
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

###########################################################################################

def run1b(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    rline = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        rline = rline.split()
    finally:
        sock.close()
        return rline

# DO NOT USE MULTIPLE COMMANDS
def run2(*commands):
        return run1b("AlgoStealYoMoney", "topnotch", commands[0])

def getData(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data = user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    list = []
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        list = rline.split()
        del list[0]
    finally:
        sock.close()
        return list
        
def updateMoving(tickers, sec_mvg_avg, data, seconds):
    mvg_avg = dict(zip(tickers, [0] * len(tickers)))
    index = 1
    for ticker in tickers:
        sec_mvg_avg[ticker].append(float(data[index]))
        if len(sec_mvg_avg[ticker]) > seconds:
            del sec_mvg_avg[ticker][0]
            mvg_avg[ticker] = sum(sec_mvg_avg[ticker]) / float(len(sec_mvg_avg[ticker]))
            # print mvg_avg
        index += 4
    return [sec_mvg_avg, mvg_avg]
   
sec_list = run2("SECURITIES")[1:]
sec_list = sec_list[::4]

empty_lists = [[]] * 10
false_list = [False] * 10

smooth_map = dict(zip(sec_list, false_list))

#tickers:: list of stock names
#sec_mvg_avg:: map of stock to moving avg 



###########################################################################################
#divides "MY_SECURITIES" into dictionary
def divDict(*commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data="AlgoStealYoMoney" + " " + "topnotch" + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        stocks = sfile.readline()
        aDict = {}
        companies = sec_list
        aList = stocks.split()
        for x in range(len(aList)):
            if aList[x] in companies:
                aDict[aList[x]] = [aList[x+1], aList[x+2]]
    finally:
        sock.close()
        return aDict
#returns a dictionary of all stocks and their geometric ratios
def divDec():
    dict1 = divDict("MY_SECURITIES")
    time.sleep(1)
    dict2 = divDict("MY_SECURITIES")
    ratioDict = {}
    for key in dict1:
        div2 = float(dict2[key][1])
        div1 = float(dict1[key][1])
        if (div1 == 0):
            div1 = 1
        ratio = div2 / div1
        ratioDict[key] = ratio
    return ratioDict

#gets time it takes for a stock's dividend to reach 25% of original stock dividend    
def timeDiv(company):
    counter = 1
    dict1 = divDict("MY_SECURITIES")
    ratio = divRatio()[company]

    div = float(dict1[company][1])
    if div == 0:
        div = 1
    div2 = ratio * div
    while (div2/div > 0.25):
        div2 = ratio * div2
        counter += 1
        print float(div2/div)
    return counter;
    
    # pct is 0.08?
def checkMovingAverages(tickers, mov_avg_short, mov_avg_long, pct):
    wantToBuy = []
    wantToSell = []
    dd = divDict("MY_SECURITIES")
    money = int(float(run2("MY_CASH")[1]))
    for t in tickers:
        ratio = mov_avg_short[t] / mov_avg_long[t]
        if 1 + pct < ratio:
            wantToBuy.append(t)
        elif 1 - pct > ratio:
            if dd[t][0] > 0:
                wantToSell.append(t)
        else:
            divs = divDict("MY_SECURITIES")
        div = float(divs[t][1])
        if (div < 0.001 and div != 0):
            wantToSell.append(t)

    print("~~~B&S~~~")
    print(wantToBuy)
    print(wantToSell)

    for s in wantToSell:
        askPrice = int(float(run2("ORDERS " + s)[7])) * 0.97
        print("ASK " + s + " " + str(askPrice) + " " + str(int(dd[s][0])))    
        run2("ASK " + s + " " + str(askPrice) + " " + str(int(dd[s][0])))    

    for b in wantToBuy:
        bidPrice = int(float(run2("ORDERS " + b)[3])) * 1.05
        stocksToBuy = int(money / (bidPrice * 10))
        print("BID " + b + " " + str(bidPrice) + " " + str(stocksToBuy))
        run2("BID " + b + " " + str(bidPrice) + " " + str(stocksToBuy))

def startBidding():
    sec_mvg_avg_short = dict((k, []) for k in sec_list)
    sec_mvg_avg_long = dict((k, []) for k in sec_list)
    outputShort = [sec_mvg_avg_short, ]
    outputLong = [sec_mvg_avg_long, ]
    data=getData("AlgoStealYoMoney", "topnotch", "SECURITIES")

    outputShort = updateMoving(sec_list, outputShort[0], data, 10)

    i = 0
    while True:
        outputShort = updateMoving(sec_list, outputShort[0], data, 10)
        outputLong = updateMoving(sec_list, outputLong[0], data, 40)
        data = getData("AlgoStealYoMoney", "topnotch", "SECURITIES")
        time.sleep(0.8)
        try:
            if i % 10 == 0:
                    print(run2("MY_ORDERS"))
            if i > 50: 
                checkMovingAverages(sec_list, outputShort[1], outputLong[1], 0.008)
        except:
            print("index error")
        i += 1
