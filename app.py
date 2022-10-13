from flask import Flask,render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from config import USER, PASSWORD, HOST

app = Flask(__name__)


app.secret_key = 'your secret key'
#  database connection
app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = 'Sherfood'

# Intialize MySQL
mysql = MySQL(app)
# Creating login page

#home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''j
    #This view function uses the render_template() function to render a template file called login.html.
    return render_template('login.html', msg='')
    if request.method == 'POST' and 'username' in request.login and 'password' in request.login:
        username = request.login['username']
        user_password = request.login['user_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = %s AND user_password = %s', (username, user_password,))
        login = cursor.fetchone()
        if login:
            session['username'] = username
            session['phone_number'] = login['phone_number']
            session['id'] = login['id']
            return render_template('index.html', msg )
        else:
            msg = 'Sorry, username or/and password are invalid. Try again'
    return render_template('login.html', msg )

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     message = ''
#     if request.method == 'POST' and 'username' in request.registration and 'password' in request.registration:
#





if __name__ == "__main__":
    app.run(debug=True)
