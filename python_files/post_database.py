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

    for row in rows: # additionally filter so that the user only sees postings he has skills he can trade for with
        if row[4].lower() not in skills_to_sell: #row[4] = what the poster of this posting wants
            rows.remove(row)
    arr = []
    for row in rows:
        arr += [fix_arrs(row)]

    return arr

def fix_arrs(fetched):
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






sample_data_list = [
{
    "postOwner": "alex99",
    "title": "Seeking Coding Guidance",
    "skills_being_sold": "Python",
    "skills_wanted": "Ai",
    "descript_learn": "I want to improve my ability to manage software projects efficiently.",
    "descript_teach": "I can help with Python scripting and basic ML concepts.",
    "image": None
},
{
    "postOwner": "jane_doe",
    "title": "Graphic Design Exchange",
    "skills_being_sold": "Python",
    "skills_wanted": "UI/UX Design",
    "descript_learn": "I'm interested in learning how to design user-friendly interfaces.",
    "descript_teach": "I have experience in photo editing and branding.",
    "image": "jane_profile.jpg"
},
{
    "postOwner": "tech_guru",
    "title": "Blockchain for AI Knowledge Swap",
    "skills_being_sold": "Blockchain Development",
    "skills_wanted": "Python",
    "descript_learn": "I want to understand how AI models work and how they can integrate with blockchain.",
    "descript_teach": "I have hands-on experience with Ethereum smart contracts and Solidity.",
    "image": None
},
{
    "postOwner": "chris_dev",
    "title": "Frontend-Backend Skill Exchange",
    "skills_being_sold": "Python",
    "skills_wanted": "Node.js",
    "descript_learn": "I want to build full-stack applications and improve my backend skills.",
    "descript_teach": "I can teach frontend development with React, Redux, and Tailwind CSS.",
    "image": "chris_avatar.png"
},
{
    "postOwner": "mary_craft",
    "title": "Video Editing & Marketing Swap",
    "skills_being_sold": "Video Editing, Premiere Pro",
    "skills_wanted": "Digital Marketing",
    "descript_learn": "I want to understand digital marketing strategies for social media.",
    "descript_teach": "I can help with video editing, transitions, and effects.",
    "image": None
}
]



create_post_database()
# for i in sample_data_list:
#     insert_posting(i)


# for i in read_all_posting_data():
#     print(i)
print(search("Python", ["node.js", "ai", "gaming"]))
