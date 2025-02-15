from flask import Flask, request, render_template, jsonify
import requests


app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route('/')
def home():
    return render_template("index.html")

# this isnt the correct code, just correct header just as a template
@app.route('/index', methods = ['POST'])
def winner_winner():
    data = request.json
    wpm = round(data['wpm'])
    print(data['wins'])
    print(find_stats(data['name']))
    wins = find_stats(data['name'])[0] + data['wins']
    print(wins)
    update_stats({'wins': wins, 'name': data['name'], 'wpm': wpm})
    return jsonify({'message': 'congratulations, stats updated'})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)