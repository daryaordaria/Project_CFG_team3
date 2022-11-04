import mysql.connector
from login_email import USER, HOST, PASSWORD

def _connection_to_sherfood_db(db_name):
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database= db_name,


    )
    return connection


def get_email_address(userid):
    try:
        db_name = 'SherFood'
        connect_to_db = _connection_to_sherfood_db(db_name)
        c = connect_to_db.cursor()

        query = """ SELECT email
              FROM users WHERE userID = {} """.format(userid)
        c.execute(query)
        email_address_list = c.fetchone()

        for email in email_address_list:
            sender_email = email



    except:
        print('An error occurred whilst connecting to the DB please try again')

    return sender_email