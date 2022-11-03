import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, flash, session, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from connect_database import get_adverts_by_id, get_adverts_by_location, add_advertisment
from lat_long import extract_lat_long_via_address, calculate_distance
from config import HOST, USER, PASSWORD


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
app.config['SECRET_KEY'] = 'the random string'    
mysql = MySQL()
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template(
            'main.html')


@app.route('/search', methods=['GET','POST'])
def search():
    return render_template(
        'search.html')


@app.route('/results', methods=['GET','POST'])
def results():
    if not request.form.get('address'):
        flash("Invalid addres")
        return redirect(url_for('search'))
    
    msg = ""
    address = request.form.get('address').strip()
    coords = extract_lat_long_via_address(address)
    
    if coords[0] is not None and coords[1] is not None:
        area = calculate_distance(coords)
        
        if area:
            results = get_adverts_by_location(area)
            
            if not results:
                msg = "Sorry. No result was found within 10 km from the given address."
        else:
            flash("Something went wrong. Try again later.")      
    else:
        flash("Something went wrong. Try again later.")
    
    return render_template(
        'results.html',
        results=results,
        msg = msg
        )


@app.route('/results/item/<id>', methods=['GET','POST'])
def item_details(id):
    result = get_adverts_by_id(id)
    if not result:
        flash("Something went wrong. Try agin later.")    
        return redirect(url_for('results'))
    return render_template(
        'item.html',
        result=result)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and request.form.get('signup') == "1":
        alert = 'alert-warning'
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
                
            else:
                flash('Sorry, username or/and password are invalid. Try again')
                alert = "alert-warning"
                
            return render_template(
                'login.html', 
                alert=alert)
        else:
            flash("Please enter both username and password to sign in.")
        
    return render_template(
        'login.html')

    
@app.route('/sher', methods=['GET','POST'])
def sher():
    if not session:
        flash("Please sign in before posting a new advertisment")
        return render_template(
            'login.html'
        )
    return render_template(
        'sher.html')
    

@app.route('/sher/add', methods=['GET','POST'])
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
            alert = "alert-warning"
            
        return render_template(
            'sher.html', alert=alert)
        
    return render_template(
        'sher.html'
        )
    
@app.route('/logout', methods=['GET','POST'])
def logout():
   session.pop('username', None)
   session.pop('id', None)
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
