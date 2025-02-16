from datetime import datetime
import sqlite3
import json
import os
from password_hash import hash_password, verify_password


def create_post_database():
    connection = sqlite3.connect('post_database.db')
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS postings (
                postId INTEGER PRIMARY KEY AUTOINCREMENT,
                postOwner VARCHAR(50),
                title TEXT,
                date TEXT,
                skills_being_sold TEXT, -- compressed array
                skills_wanted TEXT,
                descriptLearn TEXT, 
                descriptTeach TEXT,
                image TEXT
            );
        ''')
    connection.close()


def insert_posting(data):
    """
    returns a tuple where the first element is the boolean regarding whether the user was succesfully added
    the second element will contain metadata such as "success", "email exists", "usernam exists"
    """
    connection = sqlite3.connect("post_database.db")
    cursor = connection.cursor()
    postId = data['postId'] #string 'postId' is a key in the json
    postOwner = data['postOwener'] #string 'postOwner is a kew in the json'
    title = data["title"]
    skills_being_sold = data["skills_being_sold"]
    skills_wanted = data["skills_wanted"]
    descriptLearn = data["descript_learn"]
    descriptTeach = data["descript_teach"]
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image = data["image"]

    if not(postId and postOwner and title and skills_being_sold and skills_wanted and descriptLearn and descriptTeach and current_date):
        return (False, "Invalid credentials")
    try:
        cursor.execute("INSERT INTO postings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (postId, postOwner, title, skills_being_sold, skills_wanted, descriptLearn, descriptTeach, current_date, image))
        connection.commit()
        return (True, "success")
    except sqlite3.IntegrityError as e:
        error_message = str(e)
        if "UNIQUE constraint failed: postings.postId" in error_message:
            return (False, "post already exists")
        else:
            return (False, "cooked, bud, you not your code")

    finally:
        connection.close()


def read_posting_data(id: str):
    """
    returns json representation of the user data via the username
    """
    connection = sqlite3.connect("post_database.db")
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM postings where postId = ?;''', (id,))
    fetched = cursor.fetchall()
    connection.close()
    if fetched:
        fetched = fetched[0]
        dic = {}
        dic["postId"] = fetched[0]
        dic["postOwner"] = fetched[1]
        dic["title"] = fetched[2]
        dic["skills_being_sold"] = fetched[3]
        dic["skills_wanted"] = fetched[4]
        dic["descript_learn"] = fetched[5]
        dic["descript_teach"] = fetched[6]
        dic["current_date"] = fetched[7]
        dic["image"] = fetched[8]
        return dic
    return None

def read_all_posting_data():
    """
    read all the data in the sql table as a list of jsons
    """
    connection = sqlite3.connect('post_database.db')
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM postings")
    fetched = cursor.fetchall() # this is list
    connection.close()
    return fetched

def delete_postings(id:str):
    connection = sqlite3.connect('post_database.db')
    cursor = connection.cursor() 
    cursor.execute('''DELETE FROM postings WHERE postId = ?;''', (id,))
    connection.commit()
    connection.close()



    



#### TESTING FUNCTIONALITY ####

sample_data = {
    "postId": "1",
    "postOwener": "diddy",  # Note the key matches the provided typo "postOwener"
    "title": "Looking for a Mentor",
    "skills_being_sold": "Web Development",
    "skills_wanted": "Graphic Design",
    "descript_learn": "I want to learn about the latest design trends.",
    "descript_teach": "I can teach HTML, CSS, and JavaScript.",
    "image": None
}


create_post_database()
print(read_posting_data("1"))
# print(read_all_posting_data())

