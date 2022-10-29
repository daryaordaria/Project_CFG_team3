from flask import Flask, flash, render_template, request, url_for
import requests
import json

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.secret_key = 'I#love<3cookies'

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True



@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template(
            'main.html')


@app.route('/search', methods=['GET','POST'])
def search():
    return render_template(
        'search.html')



@app.route('/search', methods=['GET','POST'])
def results():
    return render_template(
        'results.html')


@app.route('/results/item', methods=['GET','POST'])
def item_details():
    return render_template(
        'item.html')


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template(
        'login.html')


@app.route('/sher', methods=['GET','POST'])
def sher():
    return render_template(
        'sher.html')


if __name__ == '__main__':
    app.run(debug=True)
