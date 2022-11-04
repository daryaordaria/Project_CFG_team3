import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, flash, session, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors

from db_connections import get_adverts_by_id, get_adverts_by_location, add_advertisment
from geo_calculations import extract_lat_long_via_address, calculate_distance
from login_logout import log_out, login_check
from email_sender import render_email_msg
from config import HOST, USER, PASSWORD, DB_NAME, EMAIL_USER, EMAIL_PASSWORD



app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.secret_key = 'I#love<3cookies'

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
#  database connection
app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DB_NAME
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = EMAIL_USER
app.config["MAIL_PASSWORD"] = EMAIL_PASSWORD
mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)



@app.route('/', methods=['GET', 'POST'])
@login_check(session)
def main():
    return 'main.html', {}


@app.route('/search', methods=['GET','POST'])
@login_check(session)
def search():
    return 'search.html', {}


@app.route('/results', methods=['GET','POST'])
@login_check(session)
def results():

    alert = "alert-danger"
    if not request.form.get('address'):
        flash("Invalid addres")
        return 'search.html', {'alert': alert}
    
    address = request.form.get('address').strip()
    coords = extract_lat_long_via_address(address)
    if coords[0] is not None or coords[1] is not None:
        area = calculate_distance(coords)
        if area:
            results = get_adverts_by_location(area)
            if results:
                return 'results.html', {'results': results}
            else:
                alert="alert-warning"
                flash("Sorry. No results were found within 10 km from the given address.")
        else:
            flash("Something went wrong. Try again later.")
    else:
        flash("Something went wrong. Try again later.")
        
    return 'search.html', {'alert': alert}


@app.route('/results/item/<id>', methods=['GET','POST'])
@login_check(session)
def item_details(id):
    result = get_adverts_by_id(id)
    if not result:
        alert = "alert-danger"
        flash("Something went wrong. Try agin later.")    
        return 'search.html', {'alert': alert}
    return 'item.html', {'result': result[0]}

@app.route('/results/item/send', methods =['GET','POST'])
@login_check(session)
def contact():
    msg = ('omg')
    print(request.form)
    if request.method == 'POST':
        msg, is_msg_rendered = render_email_msg(request.form)
        print(type(msg))
        if is_msg_rendered:
            mail.send(msg)
            alert = "alert-info"
            flash("Message send succcessfully!")
        else:
            alert="alert-danger"
            flash(msg)
            
    return 'login.html', {'alert': alert}


@app.route('/login', methods=['GET','POST'])
def login():
    alert = 'alert-warning'
    if request.method == 'POST' and request.form.get('signup') == "1":
        username = request.form['username']
        email = request.form['email']
        user_password = request.form['user_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT userID FROM users WHERE username = %s', (username,))
        existing_username = cursor.fetchone()
        cursor.execute('SELECT userID FROM users WHERE email = %s', (email,))
        existing_email = cursor.fetchone()
        
        if existing_email:
            flash("This email already does exist. Please, sign in.")
        elif existing_username:
            flash("This username already does exist.")
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, user_password, email,))
            flash('You are registered successfully! Please, sign in.')
            alert = "alert-info"
            
        mysql.connection.commit()
        
        return render_template(
            'login.html', alert=alert)
        
    if request.method == 'POST' and request.form.get('signin') == "1":
        if request.form['username'] is not None and request.form['user_password'] is not None:
            username = request.form['username']
            user_password = request.form['user_password']
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT userID FROM users WHERE username = %s AND user_password = %s', (username, user_password,))
                login = cursor.fetchone()
            except:
                login = False
            
            if login:
                session['username'] = username
                session['id'] = login['userID']
                
                alert = "alert-info"
                flash ("You are logged in successfully!")
                
                return render_template(
                'main.html', 
                alert=alert)
                
            else:
                flash('Sorry, username or/and password are invalid. Try again')
                alert = "alert-danger"
                
        else:
            flash("Please enter both username and password to sign in.")
        
    return render_template(
        'login.html')

    
@app.route('/sher', methods=['GET','POST'])
@login_check(session)
def sher():
    if not session:
        flash("Please sign in before posting a new advertisment")
        return 'login.html', {'alert': "alert-warning"}
        
    return 'sher.html', {}
    

@app.route('/sher/add', methods=['GET','POST'])
@login_check(session)
def add_advert():
    if request.method == 'POST':
        user_id = session['id']
        data = request.form
        coords = extract_lat_long_via_address(data["address"])
        is_added = add_advertisment(data, coords, user_id)
        
        if is_added:
            flash("Advert successfully added")
            alert = "alert-info"
        else:
            flash("Something went wrong. Try again later.")
            alert = "alert-danger"
            
        return 'sher.html', {'alert':alert}
        
    return 'sher.html', {}
    
    
@app.route('/logout', methods=['GET','POST'])
def logout():
    is_logged_out = log_out(session)
    
    if is_logged_out:
        alert= "alert-info"
        flash("Successfully logged out. See ya!")
    else:
        alert= "alert-danger"
        flash("We weren't able to log you out.")
        
    return  render_template(
        'login.html', 
        alert=alert
        )


if __name__ == '__main__':
    app.run(debug=True)
