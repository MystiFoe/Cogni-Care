from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import random

app = Flask(__name__)

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['gamescore']
collection = db['player_scores']

# Initialize variables
cards = []
current_card = None
logical_sequence = None
remembered_details = None
reasoning_problem = None
student_scores = {}

# Generate a deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
for suit in suits:
    for value in values:
        cards.append({'suit': suit, 'value': value})

# Shuffle the deck
random.shuffle(cards)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw_card', methods=['GET'])
def draw_card():
    global current_card
    if not cards:
        return jsonify({'message': 'No more cards to draw'})

    current_card = cards.pop()
    return jsonify(current_card)

@app.route('/logical_sequence', methods=['POST'])
def check_logical_sequence():
    global logical_sequence
    user_sequence = request.json.get('user_sequence', [])
    correct_sequence = sorted(cards[:5], key=lambda x: (x['suit'], values.index(x['value'])))

    if user_sequence == correct_sequence:
        logical_sequence = True
        return jsonify({'message': 'Correct!'})
    else:
        logical_sequence = False
        return jsonify({'message': 'Incorrect!'})

@app.route('/remember_details', methods=['POST'])
def remember_details():
    global remembered_details
    remembered_details = request.json.get('details', [])
    return jsonify({'message': 'Details remembered!'})

@app.route('/reasoning_problem', methods=['POST'])
def reasoning_problem_solve():
    global reasoning_problem
    reasoning_problem = request.json.get('solution', '')
    return jsonify({'message': 'Problem solved!'})

@app.route('/store_round_score', methods=['POST'])
def store_round_score():
    global student_scores

    student_name = request.json.get('student_name')
    round_name = request.json.get('round_name')
    round_score = request.json.get('round_score')

    # Initialize the student's score if it doesn't exist
    if student_name not in student_scores:
        student_scores[student_name] = {}

    # Store the round score for the student
    student_scores[student_name][round_name] = round_score

    return jsonify({'message': 'Round score stored successfully'})

@app.route('/store_final_score', methods=['POST'])
def store_final_score():
    student_name = request.json.get('student_name')

    # Calculate the final score by summing scores from all rounds
    final_score = sum(student_scores.get(student_name, {}).values())

    # Store the final score in the MongoDB collection
    collection.insert_one({
        'student_name': student_name,
        'final_score': final_score,
        'round_scores': student_scores.get(student_name, {}),
    })

    # Clear the student's scores for the next round
    student_scores.pop(student_name, None)

    return jsonify({'message': 'Final score stored successfully'})

if __name__ == '__main__':
    app.run(debug=True)
