import sqlite3
import json
from password_hash import hash_password, verify_password


def create_database():
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()
    cursor.execute(
        ''' CREATE table sample(
        username VARCHAR(50) PRIMARY KEY,
        email VARCHAR(50) UNIQUE,
        password VARCHAR(50),
        postIds TEXT, -- list of post ids stored as a json string
        skills TEXT -- list of skills stored as a json string
        )''')
    connection.close()


def insert_user(data):
    """
    returns a tuple where the first element is the boolean regarding whether the user was succesfully added
    the second element will contain metadata such as "success", "email exists", "usernam exists"
    """
    connection = sqlite3.connect("user_database.db")
    cursor = connection.cursor()
    username = data['username'] #string
    email = data['email'] #string
    password = hash_password(data['password']) #password
    postIds = json.dumps(data["postIds"]) # string of json data can be recreated with json.load
    skills = json.dumps(data["skills"]) # string of json data can be recreated with json.load
    if not(username and password and email and postIds and skills):
        return (False, "Invalid credentials")
    try:
        cursor.execute("INSERT INTO sample VALUES (?, ?, ?, ?, ?)", (username, email, password, postIds, skills))
        connection.commit()
        return (True, "success")
    except sqlite3.IntegrityError as e:
        error_message = str(e)
        if "UNIQUE constraint failed: sample.username" in error_message:
            return (False, "Username exists")
        elif "UNIQUE constraint failed: sample.email" in error_message:
            return (False, "Email exists")
        else:
            return (False, "Invalid credentials")

    finally:
        connection.close()


def read_user_data(user: str):
    """
    returns json representation of the user data via the username
    """
    pass

def read_all_user_data():
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM sample")
    fetched = cursor.fetchall() # this is list
    connection.close()
    return fetched

data = {"username": "diddy", "email": "123@gmail.com", "password": "teehee", "postIds": [101, 102, 103], "skills": ["python", "english"]}
# create_database()
print(insert_user(data))
print(read_all_user_data()[0])



    



