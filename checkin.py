import requests 
URL = "http://122.99.125.51:5000/checkin"
import datetime    
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d %H:%M:%S')
from uuid import getnode
import speedtest
import time

mac = getnode()

def fingData():
    print('Starting Fing')
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    import subprocess
    subprocess.call("sudo fing --rounds=1 -o table,csv," + str(dir_path) + '/fing.csv',shell=True)
    import pandas as pd
    path = dir_path + '/fing.csv'
    data = pd.read_csv(path)
    final = ""
    data2 = data.values.tolist()
    for i in data2:
        final = final + str(i[0]) + " "
    return final



print(mac)
def checkSpeed():
    print('Checking speed!')
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    results_dict = s.results.dict()
    return results_dict['download']/1000000
    
def checkin():
    dl = checkSpeed()
    print('Couldnt Check speed')
    fing = fingData()
    print("Couldnt perform find")
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'mac':mac,
        'datetime': date,
        'status': "up",
        'speed': dl,
        'fing': fing
    } 
    r = requests.post(url = URL, params = data) 
    print('Couldnt post request')
    print(r)

def res(num):
    time.sleep(num)

x = 1
while x == 1:
    try: 
        i = i +1
    except:
        i = 0
    if(i == 300 or i ==0):
        try:
            checkin()
        except:
            print("Couldn't Checkin")
        i = 0
    print(i)
    res(1)
  