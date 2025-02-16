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
                skills_being_sold TEXT, -- compressed array
                skills_wanted TEXT,
                descriptLearn TEXT, 
                descriptTeach TEXT,
                date TEXT,
                image TEXT
            );
        ''')
    connection.close()


def insert_posting(data):
    """
    Returns a tuple where the first element is a boolean indicating whether the post was successfully added.
    The second element contains metadata such as "success", "invalid credentials", or error messages.
    """
    connection = sqlite3.connect("post_database.db")
    cursor = connection.cursor()

    # Extract data from the input dictionary
    postOwner = data["postOwner"]
    title = data["title"]
    skills_being_sold = data["skills_being_sold"]
    skills_wanted = data["skills_wanted"]
    descriptLearn = data["descript_learn"]
    descriptTeach = data["descript_teach"]
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image = data["image"]

    # Validate that all required fields are present
    if not (postOwner and title and skills_being_sold and skills_wanted and descriptLearn and descriptTeach and current_date):
        return (False, "Invalid credentials")

    try:
        # Insert the data into the database
        cursor.execute("""
            INSERT INTO postings (postOwner, title, skills_being_sold, skills_wanted, 
                                  descriptLearn, descriptTeach, date, image) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (postOwner, title, skills_being_sold, skills_wanted, descriptLearn, descriptTeach, current_date, image))

        connection.commit()
        return (True, "success")
    except sqlite3.IntegrityError as e:
        error_message = str(e)
        if "UNIQUE constraint failed: postings.postId" in error_message:
            return (False, "post already exists")
        else:
            return (False, f"Database error: {error_message}")
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
    
def search(skill_wanted, skills_to_sell):
    connection = sqlite3.connect("post_database.db")
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM postings where skills_being_sold = ?;''', (skill_wanted,))  
    rows = cursor.fetchall()
    print(rows)
    print(skills_to_sell)

    for row in rows: # additionally filter so that the user only sees postings he has skills he can trade for with
        print(row[4])
        if row[4].lower() not in skills_to_sell: #row[4] = what the poster of this posting wants
            rows.remove(row)


    return rows


    



