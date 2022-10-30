from flask import Flask, flash, render_template, request, url_for
# from .connect_database import get_adverts_by_id, get_adverts_by_location
# from .functions import extract_data
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from config import USER, PASSWORD, HOST

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.secret_key = 'I#love<3cookies'

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
#  database connection
app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = 'Sherfood'
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template(
            'main.html',)


@app.route('/search', methods=['GET','POST'])
def search():
    return render_template(
        'search.html')


# @app.route('/results', methods=['GET','POST'])
# def results():
#     address = request.form.get('address').strip()
#     city, country = extract_data(address)
#     results = get_adverts_by_location(city, country)
#
#     return render_template(
#         'results.html',
#         results
#         )


# @app.route('/results/item/<id>', methods=['GET','POST'])
# def item_details(id):
#     result = get_adverts_by_id(id)
#     return render_template(
#         'item.html',
#         result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
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
            return "You are logged in successfully!"
        else:
            msg = 'Sorry, username or/and password are invalid. Try again'
    return render_template('login.html', msg )


# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
#     if request.method == 'POST' and 'username' in request.login and 'user_password' in request.login and 'phone_number' in request.login:
#         username = request.login['username']
#         user_password = request.login['user_password']
#         email = request.login['email']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM login WHERE username = %s AND user_password = %s', (username, user_password,))
#         login = cursor.fetchone()
#         if login:
#             message = "This account already does exist. Please, sign in."
#         elif not username or not user_password or not phone_number:
#             message = "Please, fill in all required field."
#         else:
#             cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username, user_password, email,))
#             mysql.connection.commit()
#             message = 'You are registered successfully!'
#     elif request.method == 'POST':
#         message = 'Please fill in the form'
#     return render_template('registration.html', msg=message)
#
@app.route('/sher', methods=['GET','POST'])
def sher():
    return render_template(
        'sher.html')


if __name__ == '__main__':
    app.run(debug=True)
