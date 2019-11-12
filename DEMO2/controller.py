from bottle import route, run, get, post, static_file, request, redirect
import sqlite3
from sqlite3 import Error


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
    return static_file("default.html", root = '')

@get('/login')
def login():
    return static_file("login.html", root='')

@post('/login')
def inputlogin():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username + " " + password)
    user = validateUser(User(username, password, ""))
    redirect('/')

@get('/users')
def admin():
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "Select * from User"
    returnval = cur.execute(sql)
    cur.close()
    conn.close()
    return returnval

@get('/user/new')
def newUser():
    return static_file("newuser.html", root = '')

@post('/user/new')
def inputNewUser():
    Name = request.forms.get('Name')
    Rank = request.forms.get('Rank')
    Email = request.forms.get('Email')
    Password = request.forms.get('Password')
    print(Name)
    print(Password)
    print(Rank)
    validusers.append(User(Email, Password, ""))
    conn = create_connection(dbfile)
    cur = conn.cursor()
    sql = "INSERT INTO User(name, password, userType) VALUES (?,?,?)"
    task = (Name, Password, Rank)
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        print(e)
        redirect("/user/new")
    redirect("/")

@get('/booking')
def booking():
    return static_file("booking.html", root='')

@post('/booking')
def inputbooking():
    return "TODO"

@get('/dates/available')
def showDates():
    string = ""
    for date in openDates:
        string += "<div>" + date + "</div>"
    return string

@get('/register')
def home():
    if user is not "":
        return static_file("table.html", root='')
    else:
        redirect("/login")

@post('/register')
def inputhome():
    if user is not "":
            Fname = request.forms.get('Fname')
            Lname = request.forms.get('Lname')
            Email = request.forms.get('Email')

run(host='localhost', port=8080, debug=True)
