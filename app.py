from flask import Flask,request,render_template
import yaml
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
# mac char(12),dateTime datetime,status bit,speed float
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def hello():
    cur =mysql.connection.cursor()
    cur.execute('''show tables ''')
    x = cur.fetchall()
    tables = []
    data = {}
    for i in range(len(x)):
        tables.append(x[i][0])
        q = " select * from " + x[i][0]
        cur.execute(q)
        y = cur.fetchall()
        data[x[i][0]] = y
    mysql.connection.commit()
    cur.close()
    return render_template('index.html',data=data)

@app.route('/checkin',methods=['POST'])
def checkin():
    r = request.args
    cur =mysql.connection.cursor()
    q1 = "CREATE TABLE IF NOT EXISTS mac" + str(r['mac']) + "(mac char(20),dateTime datetime,status bit,speed float, fing varchar(1000)) "
    print(r['fing'])
    fingdata = r['fing'].replace("'"," ")
    fingdata = fingdata.replace(";","     ")
    print(fingdata)
    q2 = "INSERT INTO mac" + str(r['mac']) + " (mac,datetime,status,speed,fing) VALUES(" + "'" + str(r['mac']) + "'" + ","  + "'" + str(r['datetime']) + "'" + "," + str(r['status']) + "," + str(r['speed']) + "," + "'" + str(fingdata) + "'" +")"
    print(q2)
    print(q1)
    cur.execute(q1)
    cur.execute(q2)
    mysql.connection.commit()
    cur.close()
    print(type(r['status']))
    return "Received"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')