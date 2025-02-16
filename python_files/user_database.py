import sqlite3
import json
import os
from password_hash import hash_password, verify_password


def create_user_database():
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()
    cursor.execute(
        ''' CREATE table IF NOT EXISTS sample(
        username VARCHAR(50) PRIMARY KEY,
        email VARCHAR(50) UNIQUE,
        password VARCHAR(50),
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
    username = data['username'] #string 'username' is a key in the json
    email = data['email'] #string 'email is a kew in the json'
    password = hash_password(data['password']) #password 'password' is a key in the json
    skills = json.dumps(data["skills"]) # string of json data can be recreated with json.load 'skills' is a key in the json
    if not(username and password and email and skills):
        return (False, "Invalid credentials")
    try:
        cursor.execute("INSERT INTO sample VALUES (?, ?, ?, ?)", (username, email, password, skills))
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
    connection = sqlite3.connect("user_database.db")
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM sample where username = ?;''', (user,))
    fetched = cursor.fetchall()
    connection.close()
    if fetched:
        fetched = fetched[0]
        dic = {}
        dic["name"] = fetched[0]
        dic["skills"] = json.loads(fetched[3])
        return dic
    return None

def read_all_user_data():
    """
    read all the data in the sql table as a list of jsons
    """
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM sample")
    fetched = cursor.fetchall() # this is list
    connection.close()
    return fetched

def delete_user(user:str):
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor() 
    cursor.execute('''DELETE FROM sample WHERE username = ?;''', (user,))
    connection.commit()
    connection.close()

def check_info(data):
    """
    check that the email,password pair exists
    """
    email = data['email']
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM sample WHERE email = ?;''', (email,))
    fetched = cursor.fetchall()
    connection.close()
    # returning 1 means email not found
    # returning 2 means password doesn't match
    # returning 3 means everything is good ( we also return his data on login)
    if not fetched:
        return (1,)
    fetched = fetched[0]
    if not verify_password(fetched[2], data['password']):
        return (2,)
    else:
        dic = {}
        dic["name"] = fetched[0]
        dic["skills"] = json.loads(fetched[3])
        return (3, dic)
    



#### TESTING FUNCTIONALITY ####

data = {"username": "diddy", "email": "123@gmail.com", "password": "teehee", "skills": ["python", "english"]}

data2 = {"username": "diddy", "email": "123@gmail.com", "password": "teehee", "skills": ["python", "english"]}

create_user_database()

# print(insert_user(data))
# print(insert_user(data2))

# l = read_user_data("diddy")
# print(l)



# print(read_user_data("diddy"))
# print("\n")
# delete_user("diddy")
# print(read_all_user_data())

