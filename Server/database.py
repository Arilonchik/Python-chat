import psycopg2 as ps


def connect_base():
    """
    Connection to database.
    :return: [{str:str}], [
    {'username':str, 'text': str, 'time': float}
    ...
    ], new database connection

    """
    conn = ps.connect(dbname='Messenger', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "users"')
    users_np = cursor.fetchall()
    users = {}
    for user in users_np:
        users[user[0]] = user[1]

    cursor.execute('SELECT * FROM "messages"')
    messages_np = cursor.fetchall()
    messages = []
    for message in messages_np:
        messages.append({'username': message[0], 'text': message[1], 'time': message[2]})

    print(messages)
    print(users)
    cursor.close()

    return users, messages, conn
