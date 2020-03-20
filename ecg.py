import mysql.connector
import time
import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user="flask",
  passwd="shrey@212",
  database ="heartbeat"
)

def checker():
    cur = mydb.cursor()
    cur.execute(''' use heartbeat ''')
    x =cur.execute(''' show tables ''')
    x = cur.fetchall()
    for i in range(len(x)):
        tables = []
        tables.append(x[i][0])
        q = " select * from " + x[i][0] + " ORDER BY datetime DESC LIMIT 1"
        cur.execute(q)
        y = cur.fetchall()
        now = datetime.datetime.now()
        diff = (now - y[0][1]).total_seconds()
        if(diff>380):
            cur = mydb.cursor()
            q2 = "INSERT INTO " + str(x[i][0]) + " (mac,datetime,status,speed,fing) VALUES(" + "'" + str(x[i][0][3:]) + "'" + ","  + "'" + str(now) + "'" + "," + str(0) + "," + str(0) + "," + "'" + str("-") + "'" +")"
            print(q2)
            cur.execute(q2)
            mydb.commit()
        print(diff)


z = 1
while z == 1:
  try: 
    i = i +1
  except:
    i = 0
  if(i == 60  or i ==0):
    checker()
    i = 0
  print(i)
  time.sleep(1)