from tkinter import DISABLED, Tk, Button, Frame
import random
import time
import pymongo

#### GLOBAL VARIABLES ######

# data list contains the data in the cards
data = ["A", "B", "C", "D", "E", "F", "G", "H"]
data_length = len(data)

# to check if the game ends, No more available cards
game_end = 0

# dictionary stores buttons(keys) and their texts(values)
dict_cards = {}

# to check how many cards clicked if 2, stop and check similarity
clicked_cards = 0

# fst_ refers to the first clicked card
fst_ = ""

# scnd_ refers to the second clicked card
scnd_ = ""

# store the moment when the game starts
start = time.time()

# Initialize MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["memory_game_results"]
collection = db["results"]

# Timing score categories
# Modify the timing_scores dictionary to use specific time ranges
timing_scores = {
    (0, 40): 10,          # Less than 10 seconds
    (40, 50): 9,          # 10-15 seconds
    (50, 60): 8,          # 15-20 seconds
    (60, 65): 7,          # 20-25 seconds
    (65, 70): 6,          # 25-30 seconds
    (70, 75): 5,          # 30-35 seconds
    (75, 80): 4,          # 35-40 seconds
    (80, 85): 3,          # 40-45 seconds
    (85, 90): 2,          # 45-50 seconds
    (90, float('inf')): 1,  # Above 50 seconds
}

# initialize or initiate our root(window)
root = Tk()
root.resizable(False, False)
root.title("Memory Game")

# first frame_
f1 = Frame(root)
f1.pack()

# fonts
fonts = ['Helvetica', '20', 'bold']

bt1 = Button(f1, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt1))
bt1.grid(row=0, column=0, padx=20, pady=40)
dict_cards[bt1] = ""

bt2 = Button(f1, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt2))
bt2.grid(row=0, column=1, padx=20, pady=40)
dict_cards[bt2] = ""

bt3 = Button(f1, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt3))
bt3.grid(row=0, column=2, padx=20, pady=40)
dict_cards[bt3] = ""

bt4 = Button(f1, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt4))
bt4.grid(row=0, column=3, padx=20, pady=40)
dict_cards[bt4] = ""

# second frame_
f2 = Frame(root)
f2.pack()

bt5 = Button(f2, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt5))
bt5.grid(row=1, column=0, padx=20, pady=40)
dict_cards[bt5] = ""

bt6 = Button(f2, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt6))
bt6.grid(row=1, column=1, padx=20, pady=40)
dict_cards[bt6] = ""

bt7 = Button(f2, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt7))
bt7.grid(row=1, column=2, padx=20, pady=40)
dict_cards[bt7] = ""

bt8 = Button(f2, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt8))
bt8.grid(row=1, column=3, padx=20, pady=40)
dict_cards[bt8] = ""

# third frame_
f3 = Frame(root)
f3.pack()

bt9 = Button(f3, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt9))
bt9.grid(row=1, column=0, padx=20, pady=40)
dict_cards[bt9] = ""

bt10 = Button(f3, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt10))
bt10.grid(row=1, column=1, padx=20, pady=40)
dict_cards[bt10] = ""

bt11 = Button(f3, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt11))
bt11.grid(row=1, column=2, padx=20, pady=40)
dict_cards[bt11] = ""

bt12 = Button(f3, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt12))
bt12.grid(row=1, column=3, padx=20, pady=40)
dict_cards[bt12] = ""

# forth frame_
f4 = Frame(root)
f4.pack()

bt13 = Button(f4, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt13))
bt13.grid(row=1, column=0, padx=20, pady=40)
dict_cards[bt13] = ""

bt14 = Button(f4, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt14))
bt14.grid(row=1, column=1, padx=20, pady=40)
dict_cards[bt14] = ""

bt15 = Button(f4, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt15))
bt15.grid(row=1, column=2, padx=20, pady=40)
dict_cards[bt15] = ""

bt16 = Button(f4, font=(fonts), width="5", height="3", command=lambda: bttn_clicked(bt16))
bt16.grid(row=1, column=3, padx=20, pady=40)
dict_cards[bt16] = ""

######### USED FUNCTIONS #########

# this function to set random data to our cards
def random_text():
    # record if the data has occurred twice
    occurrences = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0}
    for btn in dict_cards:
        if len(data) > 0:
            random.shuffle(data)
            x = data[0]
            dict_cards[btn] = x
            occurrences[x] = occurrences[x] + 1
            if occurrences[x] == 2:
                data.remove(x)

# this function is called when we click a card
def bttn_clicked(btn):
    global clicked_cards
    global fst_
    global scnd_
    clicked_cards = clicked_cards + 1
    if clicked_cards == 1:
        fst_ = btn
        btn.configure(text=dict_cards[btn], state=DISABLED)
    if clicked_cards == 2:
        scnd_ = btn
        btn.configure(text=dict_cards[btn], state=DISABLED)
        root.after(500, check_same)

# this function to check if the two cards are similar
def check_same():
    global clicked_cards
    global fst_
    global scnd_
    global game_end
    global data_length
    if scnd_['text'] != fst_['text']:
        fst_.configure(text="", state="normal")
        scnd_.configure(text="", state="normal")
    else:
        game_end = game_end + 1
        if game_end == data_length:
            elapsed_time = int(time.time() - start)
            player_name = input("Enter your name: ")  # Prompt the player for their name
            
            # Determine the player's score based on elapsed time
            for (min_time, max_time), score in timing_scores.items():
                if min_time <= elapsed_time < max_time:
                    player_score = score
                    break
            else:
                player_score = 0  # Default score if none of the time ranges match
            
            # Store the player's name and score in the MongoDB collection
            document = {
                "player_name": player_name,
                "elapsed_time": elapsed_time,
                "player_score": player_score,
            }
            collection.insert_one(document)
            root.destroy()
    clicked_cards = 0


# calling the function random_text
random_text()
# run our window
root.mainloop()
