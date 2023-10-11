from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["gamescore"]

# Initialize variables to store student scores for each category
student_scores = {}

# Sample questions and answers for all categories
categories = [
    {
        'name': 'Rememberance',
        'questions': [
            {
                'question': 'What color is the sky during the day?',
                'options': ['Red', 'Blue', 'Green'],
                'answer': 'Blue'
            },
            {
                'question': 'What is the color of grass?',
                'options': ['Yellow', 'Green', 'Brown'],
                'answer': 'Green'
            },
            {
                'question': 'What color is a stop sign?',
                'options': ['Green', 'Blue', 'Red'],
                'answer': 'Red'
            },
            {
                'question': 'Which planet is closest to the Sun?',
                'options': ['Venus', 'Mars', 'Mercury'],
                'answer': 'Mercury'
            },
        ]
    },
    {
        'name': 'Logical Thinking',
        'questions': [
            {
                'question': 'If a cat has fur and barks like a dog, is it still a cat?',
                'options': ['Yes', 'No'],
                'answer': 'No'
            },
            {
                'question': 'If you have a red ball and a blue ball, how many balls do you have?',
                'options': ['One', 'Two'],
                'answer': 'Two'
            },
            # Add more questions here
        ]
    },
    # Add more categories here
]

@app.route('/')
def index():
    return render_template('questions.html', categories=categories)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    student_name = request.form.get('student_name')

    # Initialize the student's scores if they don't exist
    if student_name not in student_scores:
        student_scores[student_name] = {}

    for category in categories:
        category_name = category['name']
        round_scores = []

        for question in category['questions']:
            question_text = question['question']
            correct_answer = question['answer']
            user_answer = request.form.get(question_text, '').strip().lower()

            if user_answer == correct_answer.lower():
                round_scores.append(1)
            else:
                round_scores.append(0)

        # Calculate the round score (total correct answers) for this category
        category_score = sum(round_scores)

        # Store the category score for the student
        student_scores[student_name][category_name] = category_score

        # You can store scores in the database as needed

    return jsonify({'message': 'Answers submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
