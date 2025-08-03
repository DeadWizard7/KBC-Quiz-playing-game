import json
from tkinter import messagebox

def save_score(player_name, score):
    try:
        with open("kbc_leaderboard.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.append({"name": player_name, "score": score})
    with open("kbc_leaderboard.json", "w") as file:
        json.dump(scores, file)

def view_leaderboard():
    try:
        with open("kbc_leaderboard.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.sort(key=lambda x: x['score'], reverse=True)
    board = "Leaderboard:\n\n"
    for entry in scores[:5]:
        board += f"{entry['name']}: ${entry['score']}\n"
    messagebox.showinfo("Leaderboard", board)
