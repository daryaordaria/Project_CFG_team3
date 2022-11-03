import mysql.connector
from datetime import date
from config import USER, PASSWORD, HOST, DB_NAME

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
    db_name = DB_NAME
    db_connection = _connect_to_db(db_name)
    cur = db_connection.cursor()
        
    cur.execute(query)
    results = cur.fetchall()
    keys = ['annoucementID','userID', 'address', 'latitude', 'longitude', 'pick_up_details', 
            'expiration_date', 'vegan', 'vegetarian', 'kosher', 'halal', 'glutenfree', 
            'lactosefree', 'product_name', 'description']
    tags = ['vegan', 'vegetarian', 'kosher', 'halal', 'glutenfree', 'lactosefree']
    
    for result in results:
        result_dict = dict(zip(keys, result))
        
        tags = [key for key, val in result_dict.items() if key in tags and val == 1]
        result_dict["tags"] = ", ".join(tags)
        
        if result_dict["expiration_date"] >= date.today():
            adverts.append(result_dict) 
        else:
            delete_query = f"""
                DELETE FROM annoucements
                WHERE annoucementID = '{result_dict["annoucementID"]}'
                """
            cur.execute(delete_query)
            
    db_connection.commit()
    cur.close()
    
    if db_connection:
        db_connection.close()

    return adverts


def get_adverts_by_location(coords):
    query = f"""
        SELECT 
            annoucementID, userID, address, latitude, longitude, pick_up_details, 
            expiration_date, vegan, vegetarian, kosher, halal, glutenfree, 
            lactosefree, product_name, description
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
                annoucementID, userId, address, latitude, longitude, pick_up_details, 
                expiration_date, vegan, vegetarian, kosher, halal, glutenfree, 
                lactosefree, product_name, description
            FROM 
                annoucements 
            WHERE 
                annoucementID = '{id}'
            """
        result = _get_adverts(query)
    except:
        result = False
        
    return result


def add_advertisment(data, coords, user_id):
    try:
        db_name = 'Sherfood'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        query = f"""
            INSERT INTO annoucements 
                (
                userID, address, latitude, longitude, pick_up_details, 
                expiration_date, vegan, vegetarian, kosher, halal, glutenfree, 
                lactosefree, product_name, description
                )
            VALUES 
                (
                '{user_id}','{data["address"]}', '{coords[0]}', '{coords[1]}', 
                '{data["pick_up_details"]}', '{data["expiration_date"]}', 
                '{data.get("vegan", 0)}', '{data.get("vegetarian", 0)}',  
                '{data.get("kosher", 0)}', '{data.get("halal", 0)}',  
                '{data.get("glutenfree", 0)}', '{data.get("lactosefree", 0)}', 
                '{data["product_name"]}', '{data["description"]}'
                )
            """
        cur.execute(query)
        db_connection.commit()
        cur.close()
        is_added = True

        if db_connection:
            db_connection.close()
    except:
        is_added = False

    return is_added

# print(get_adverts_by_location({'lat_min': 54.014426863627534, 'lat_max': 54.19429093637245, 'lon_min': 22.764211235446048, 'lon_max': 23.070983364553957}))