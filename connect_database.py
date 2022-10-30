import mysql.connector
from .config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx


def _get_adverts(query):
    adverts = []
    db_name = 'Sherfood'
    db_connection = _connect_to_db(db_name)
    cur = db_connection.cursor()
    print("Connected to DB: %s" % db_name)
        
    cur.execute(query)
    results = cur.fetchall()  # this is a list with db records where each record is a tuple

    keys = ['userID', 'annoucementID', 'country', 'city', 'pick_up_details', 
    'expiration_date', 'vegan', 'vegetarian', 'kosher', 'halal', 'glutenfree', 
    'lactosefree', 'product_name', 'description', 'status']
    tags = ['vegan', 'vegetarian', 'kosher', 'halal', 'glutenfree', 'lactosefree']
    
    for result in results:
        result_dict = dict(zip(keys, result))
        
        tags = [key for key, val in result_dict.items() if key in tags and val == 1]
        result_dict[tags] = ", ".join(tags)
        
        adverts.append(result_dict) 
    cur.close()
    
    if db_connection:
        db_connection.close()

    return adverts


def get_adverts_by_location(city, country):
    query = f"""
        SELECT userID, annoucmentID, country, city, pick_up_details, 
        expiration_date, vegan, vegetarian, kosher, halal, glutenfree, 
        lactosefree, product_name, description, status
        FROM annoucements 
        WHERE city = '{city}' AND country = '{country}' 
        """

    result = _get_adverts(query)
    return result


def get_adverts_by_id(id):
    query = f"""
        SELECT userID, annoucmentID, country, city, pick_up_details, 
        expiration_date, vegan, vegetarian, kosher, halal, glutenfree, 
        lactosefree, product_name, description, status
        FROM annoucements 
        WHERE annoucmentID = '{id}'
        """
    result = _get_adverts(query)
    return result
