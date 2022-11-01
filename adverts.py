from flask import Flask, flash, render_template, request, url_for
from .connect_database import get_adverts_by_id, get_adverts_by_location
from .functions import extract_data

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.secret_key = 'I#love<3cookies'

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template(
            'main.html',)


@app.route('/search', methods=['GET','POST'])
def search():
    return render_template(
        'search.html')


@app.route('/results', methods=['GET','POST'])
def results():
    address = request.form.get('address').strip()
    city, country = extract_data(address)
    results = get_adverts_by_location(city, country)
    
    return render_template(
        'results.html',
        results
        )


@app.route('/results/item/<id>', methods=['GET','POST'])
def item_details(id):
    result = get_adverts_by_id(id)
    return render_template(
        'item.html',
        result)


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
