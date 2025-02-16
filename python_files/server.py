from flask import Flask, request, render_template, jsonify
import requests

from user_database import check_info, insert_user, read_user_data
from post_database import insert_posting, search


app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route('/')
def home():
    return render_template("index.html")

@app.route("/index.html")
def home2():
    return render_template("index.html")

@app.route("/homepage.html")
def homepage():
    return render_template("homepage.html")

# this isnt the correct code, just correct header just as a template
@app.route('/index', methods = ['POST'])
def winner_winner():
    pass

@app.route("/signin.html")
def signin():
    return render_template("signin.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/signin", methods = ['POST'])
def handle_login():
    print("hello")
    # check_info() will return a number from 1-3
    # returning 1 means email not found
    # returning 2 means password doesn't match
    # returning 3 means everything is good
    data = request.json
    print("data: "+ str(data))
    result = check_info(data)
    if result[0] == 1:
        return jsonify({"message": "This Email is not valid", 'success': False, 'name': None})
    elif result[0] == 2:
        return jsonify({'message': "Password is incorrect", 'success': False, 'name': None})
    else:
        data = result[1]
        return jsonify({'message': 'Login Successful', 'success': True, 'name': result[1]["name"], "skills": result[1]["skills"]})


@app.route('/register', methods=['POST'])
def handle_signup():
    data = request.json
    dumped_data = insert_user(data)
    if not dumped_data:
        return jsonify({"message": "User was unable to sign up successfully", 'success': False, 'name': None, "skills": None})
    if dumped_data[0]:
        name = data['username']
        return jsonify({"message": "User signed up successfully", 'success': True, 'name': name, "skills": data["skills"]})
    else:
        return jsonify({"message": dumped_data[1], 'success': False, 'name': None, "skills": None})


@app.route("/create_post", methods=["POST"])
def handle_post_creation():
    data = request.json
    result = insert_posting(data)
    print(result)
    if not result:
        return jsonify({"message": "Unable to create post", "success": False})
    if result[0]:
        return jsonify({"message": "Post created successfully", 'success': True})
    else:
        return jsonify({"message": "Post does not exist", "success": False})


@app.route("/create_post.html")
def create_post():
    return render_template("create_post.html")

@app.route("/skillset.html")
def skillset():
    return render_template("skillset.html")

@app.route("/index")
def handle_search():
    data = request.json

    if not(data["search"] and data["skill_set"]):
        return jsonify({"data": []})

    return jsonify({"data": search(data["search"], data["skill_set"])})

    

@app.route("/posting_page.html")
def posing_page():
    return render_template("posting_page.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)