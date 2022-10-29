import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password'
        database=db_name
    )
    return cnx

def get_adverts(city, country):
    adverts = []
    db_name = 'Sherfood'
    db_connection = connect_to_db(db_name)
    cur = db_connection.cursor()
    print("Connected to DB: %s" % db_name)

    query = """
        SELECT expiration_date
        FROM annoucements 
        """

    cur.execute(query)

    results = cur.fetchall()  # this is a list with db records where each record is a tuple
    for result in results:
        adverts.append(result) 
    cur.close()

    raise DbConnectionError("Failed to read data from DB")

    if db_connection:
        db_connection.close()
        print("DB connection is closed")

    return adverts

print(get_adverts("Warsaw", "Poland"))