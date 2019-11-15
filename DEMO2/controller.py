#import bottle
from bottle import route, run, get, post, static_file, request, redirect
import sqlite3
from sqlite3 import Error
from cork import Cork
import simplejson as json
import datetime

class User:
    def __init__(self, username, password, rank):
        self.username = username
        self.password = password
        self.rank = rank

validusers = [User("admin", "password", "admin"), User("user", "pass", "client")]
openDates = []

user = "";
dbfile = "pythonsqlite.db"
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    print(conn)
    return conn


#Get all availible dates
filepath = ''
with open("NOV_Avail_Dates", "r") as fp:
    line = fp.readline()
    openDates.append(line)
    while line:
    	line = fp.readline()
    	openDates.append(line);


def validateUser(attemptedLogin):
    for user in validusers:
        if attemptedLogin.username == user.username and attemptedLogin.password == user.password:
            return attemptedLogin
            redirect("/")
    print("Failed Login")
    redirect('/login')

def checkIfValidDate():
    file = ''
    with open("NOV_Avail_Dates", "r") as f:
    	date = f.readline()
    	x = date in availDates
    	print(x)

@get('/')
def default():
    return static_file("default.html", root = 'HTML/')

@get('/login')
def login():
    return static_file("login.html", root='HTML/')

@post('/login')
def inputlogin():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username + " " + password)
    user = validateUser(User(username, password, ""))
    redirect('/')

@get('/json/users')
def getAllUsers():
    returnval = []
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from User"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for user in data:
        returnval.append({"id": user[0],
                        "name": user[1],
                        "password": user[2],
                        "userType": user[3]})
    return json.dumps(returnval)

@get('/json/user/<id>')
def getUserById(id):
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from User where id = " + id
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    conn.close()
    returnval = {"id": data[0],
                    "name": data[1],
                    "password": data[2],
                    "userType": data[3]}
    return json.dumps(returnval)


@get('/user/new')
def newUser():
    return static_file("newuser.html", root = 'HTML/')

@post('/user/new')
def inputNewUser():
    Name = request.forms.get('Name')
    Rank = request.forms.get('Rank')
    Password = request.forms.get('Password')
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "INSERT INTO User(name, password, userType) VALUES (?,?,?)"
    task = (Name, Password, Rank)
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)
        redirect("/user/new")
    finally:
        cur.close()
        conn.close()
    redirect("/")

@get('/booking')
def booking():
    return static_file("booking.html", root='HTML/')

@post('/booking')
def inputbooking():
    Name = request.forms.get('name')
    StartDate = request.forms.get('startDate')
    EndDate = request.forms.get('endDate')
    RoomType = request.forms.get('roomType')
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "INSERT INTO Reservations(customerId, startDate, endDate, roomType) VALUES (?,?,?,?)"
    task = (Name, StartDate, EndDate, RoomType)
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        print(e)
        redirect("/booking")
    redirect("/")

@get('/json/booking')
def jsonAllReservations():
    thisreturnval = []
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from Reservations"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for piece in data:
        #customer = json.loads(getUserById(str(piece[0])))
        thisreturnval.append({"id": piece[0],
                        "customerId": piece[1],
                        "startDate": piece[2],
                        "endDate": piece[3],
                        "roomType": piece[4]})
    return json.dumps(thisreturnval)

@get('/json/booking/future')
def jsonAllReservations():
    now = datetime.datetime.now()
    thisreturnval = []
    print(now)
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from Reservations where startDate > DateTime('"+str(now.year) + "-" + str(now.month) +"-"+str(now.day) + " 00:00:00"+"');"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for piece in data:
        #customer = json.loads(getUserById(str(piece[0])))
        thisreturnval.append({"id": piece[0],
                        "customerId": piece[1],
                        "startDate": piece[2],
                        "endDate": piece[3],
                        "roomType": piece[4]})
    return json.dumps(thisreturnval)

@get('/json/booking/current')
def jsonAllReservations():
    now = datetime.datetime.now()
    thisreturnval = []
    print(now)
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from Reservations where startDate <= DateTime('"+str(now.year) + "-" + str(now.month) +"-"+str(now.day) + " 00:00:00"+"') and endDate >= DateTime('"+str(now.year) + "-" + str(now.month) +"-"+str(now.day) + " 00:00:00"+"');"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for piece in data:
        #customer = json.loads(getUserById(str(piece[0])))
        thisreturnval.append({"id": piece[0],
                        "customerId": piece[1],
                        "startDate": piece[2],
                        "endDate": piece[3],
                        "roomType": piece[4]})
    return json.dumps(thisreturnval)

@get('/json/booking/past')
def jsonAllReservations():
    now = datetime.datetime.now()
    thisreturnval = []
    print(now)
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from Reservations where endDate < DateTime('"+str(now.year) + "-" + str(now.month) +"-"+str(now.day) + " 00:00:00"+"');"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for piece in data:
        #customer = json.loads(getUserById(str(piece[0])))
        thisreturnval.append({"id": piece[0],
                        "customerId": piece[1],
                        "startDate": piece[2],
                        "endDate": piece[3],
                        "roomType": piece[4]})
    return json.dumps(thisreturnval)


@get('/dates/available')
def showDates():
    string = ""
    for date in openDates:
        string += "<div>" + date + "</div>"
    return string

@get('/register')
def home():
    if user is not "":
        return static_file("table.html", root='HTML/')
    else:
        redirect("/login")

@post('/register')
def inputhome():
    if user is not "":
            Fname = request.forms.get('Fname')
            Lname = request.forms.get('Lname')
            Email = request.forms.get('Email')

run(host='localhost', port=8080, debug=True)
