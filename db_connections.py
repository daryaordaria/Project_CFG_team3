import mysql.connector
from datetime import date
from collections import defaultdict, namedtuple
from functools import wraps
from config import USER, PASSWORD, HOST, DB_NAME


tags = ['vegan', 'vegetarian', 'kosher', 'halal', 'glutenfree', 'lactosefree']
keys = ['annoucementID','userID', 'address', 'latitude', 'longitude', 'pick_up_details', 
            'expiration_date', *tags, 'product_name', 'description']


# decorator:
def db_connection(func):
    @wraps(func)
    def inner(*args):
        db_connection = _connect_to_db(DB_NAME)
        cur = db_connection.cursor()
        results = func(*args,cur)
        db_connection.commit()
        cur.close()

        if db_connection:
            db_connection.close()
        return results
    return inner


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return cnx


def _delete_advert(id, cur):
    query = f"""
        DELETE FROM annoucements
        WHERE annoucementID = '{id}'
        """
    cur.execute(query)
    
    
@db_connection
def _get_adverts(*args):
    Args = namedtuple('Args',('query', 'db_cursor'))
    arg = Args(*args)
    
    arg.db_cursor.execute(arg.query)
    results = arg.db_cursor.fetchall()
    
    adverts = []
    for result in results:
        result_dict = dict(zip(keys, result))
        
        present_tags = [key for key, val in result_dict.items() if key in tags and val == 1]
        result_dict["tags"] = ", ".join(present_tags)
        
        if result_dict["expiration_date"] >= date.today():
            adverts.append(result_dict) 
        else:
            _delete_advert(result_dict["annoucementID"], arg.db_cursor)
            
    return adverts


def get_adverts_by_location(coords):
    query = f"""
        SELECT 
            {", ".join(keys)}
        FROM 
            annoucements 
        WHERE 
            (latitude BETWEEN '{coords["lat_min"]}' AND '{coords["lat_max"]}')
            AND (longitude BETWEEN '{coords["lon_min"]}' AND '{coords["lon_max"]}') 
        """
    result = _get_adverts(query)
        
    return result


def get_adverts_by_id(id):
    try:
        query = f"""
            SELECT 
                {", ".join(keys)}
            FROM 
                annoucements 
            WHERE 
                annoucementID = '{id}'
            """
        result = _get_adverts(query)
        
    except:
        result = False
        
    return result


@db_connection
def add_advertisment(*args):
    Args = namedtuple('Args',('data','coords','user_id', 'db_cursor'))
    arg = Args(*args)
    
    try:
        data = defaultdict(int, arg.data)
        query = f"""
            INSERT INTO annoucements 
                (
                {", ".join(keys[1:])}
                )
            VALUES 
                (
                '{arg.user_id}','{data["address"]}', '{arg.coords[0]}', '{arg.coords[1]}', 
                '{data["pick_up_details"]}', '{data["expiration_date"]}', 
                '{data["vegan"]}', '{data["vegetarian"]}',  
                '{data["kosher"]}', '{data["halal"]}',  
                '{data["glutenfree"]}', '{data["lactosefree"]}', 
                '{data["product_name"]}', '{data["description"]}'
                )
            """
        arg.db_cursor.execute(query)
        
        return True
    
    except:
        return False


@db_connection
def get_email_address(*args):
    try:
        Args = namedtuple('Args',('user_id', 'db_cursor'))
        arg = Args(*args)

        query = f""" 
                SELECT 
                    email
                FROM 
                    users 
                WHERE 
                    userID = '{arg.user_id}' 
                """
                    
        arg.db_cursor.execute(query)
        email_address = arg.db_cursor.fetchone()
        
    except:
        return False

    return email_address[0]

