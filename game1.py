from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# Global variables
data = ["A", "B", "C", "D", "E", "F", "G", "H"]
data_length = len(data)

# Game state variables
game_data = []
clicked_cards = 0
fst_ = None
scnd_ = None
game_end = 0
start_time = None

# Function to initialize game data
def initialize_game():
    global game_data, start_time
    game_data = random.sample(data * 2, len(data) * 2)
    random.shuffle(game_data)
    clicked_cards = 0
    fst_ = None
    scnd_ = None
    game_end = 0
    start_time = time.time()

initialize_game()

# Routes
@app.route("/")
def home():
    return render_template("game1.html", game_data=game_data, len=len)

@app.route("/card_clicked", methods=["POST"])
def card_clicked():
    global clicked_cards, fst_, scnd_, game_end
    card_index = int(request.json.get("card_index"))

    if clicked_cards == 0:
        fst_ = card_index
    elif clicked_cards == 1:
        scnd_ = card_index

    # Handle the game logic here

    clicked_cards += 1

    response = {"result": "success", "game_end": game_end}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
