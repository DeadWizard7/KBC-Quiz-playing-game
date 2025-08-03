import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json

QUESTIONS = [
    ("What is the capital of Bangladesh?", ["Tokyo", "Dhaka", "Delhi", "London"], "b"),
    ("What is the value 4*3/2?", ["9", "12", "6", "23"], "c"),
    ("How many days are in one year?", ["345", "365", "278", "578"], "b"),
    ("What is the value of 5^2 - 2*5*5 - 5^2?", ["3", "0", "6", "4"], "b"),
    ("When did Bangladesh get independence?", ["1970", "1971", "1974", "1973"], "b"),
    ("Where is the Saskatchewan University located?", ["Toronto", "Vancouver", "Montreal", "Ottawa"], "a"),
    ("What is the result of 23*2?", ["46", "47", "48", "49"], "a"),
    ("Who is the Prime Minister of Bangladesh?", ["Narendra Modi", "Sheikh Hasina", "Khaleda Zia", "Ziaur Rahman"], "b"),
    ("What is a 'cell' in wireless communication?", ["A minimum area", "A maximum area", "A dedicated area", "A reserved area"], "c")
]

BANK = [500, 1000, 1500, 5000, 10000, 10000, 20000, 50000, 60000]
def use_5050_lifeline(question, radio_buttons):
    _, options, correct = question
    correct_index = ord(correct) - 97
    incorrect_indices = [i for i in range(4) if i != correct_index]
    remove_two = random.sample(incorrect_indices, 2)
    for i in remove_two:
        radio_buttons[i].config(state=tk.DISABLED)

def ask_audience_lifeline(question):
    _, _, correct = question
    percentages = [random.randint(5, 30) for _ in range(4)]
    correct_index = ord(correct) - 97
    percentages[correct_index] = 100 - sum(percentages) + percentages[correct_index]
    result = "Audience Poll Results:\n"
    for i in range(4):
        result += f"{chr(97+i)}) {percentages[i]}%\n"
    messagebox.showinfo("Ask the Audience", result)

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


class KBCQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("KBC Quiz Game")
        self.root.geometry("650x500")

        self.player_name = simpledialog.askstring("Player Name", "Enter your name:")
        if not self.player_name:
            self.player_name = "Anonymous"

        self.questions = QUESTIONS
        self.bank = BANK
        self.current_index = 0
        self.winnings = []
        self.used_5050 = False
        self.used_audience = False

        self.setup_widgets()
        self.load_question()

    def setup_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=600, justify="left")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.var, value=chr(97 + i), font=("Arial", 12))
            rb.pack(anchor="w")
            self.radio_buttons.append(rb)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_answer, font=("Arial", 12), bg="green", fg="white")
        self.submit_button.pack(pady=10)

        self.lifeline_button = tk.Button(self.root, text="Use 50:50", command=self.use_5050, font=("Arial", 12), bg="orange", fg="white")
        self.lifeline_button.pack(pady=5)

        self.audience_button = tk.Button(self.root, text="Ask the Audience", command=self.ask_audience, font=("Arial", 12), bg="blue", fg="white")
        self.audience_button.pack(pady=5)

        self.leaderboard_button = tk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard, font=("Arial", 12), bg="gray", fg="white")
        self.leaderboard_button.pack(pady=5)

    def load_question(self):
        if self.current_index < len(self.questions):
            q_text, options, _ = self.questions[self.current_index]
            self.question_label.config(text=f"Q{self.current_index+1}: {q_text}")
            for i in range(4):
                self.radio_buttons[i].config(text=f"{chr(97+i)}) {options[i]}", state=tk.NORMAL)
            self.var.set(None)
        else:
            self.winnings.append(2000)
            total = sum(self.winnings)
            save_score(self.player_name, total)
            messagebox.showinfo("Congratulations!", f"{self.player_name}, you've completed the quiz!\nTotal Winnings: ${total}")
            self.root.quit()

    def submit_answer(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer.")
            return

        _, _, correct = self.questions[self.current_index]
        if selected == correct:
            self.winnings.append(self.bank[self.current_index])
            self.current_index += 1
            self.used_5050 = False
            self.used_audience = False
            self.load_question()
        else:
            total = sum(self.winnings)
            save_score(self.player_name, total)
            messagebox.showerror("Wrong Answer", f"Oops! Wrong answer.\nTotal Winnings: ${total}")
            self.root.quit()

    def use_5050(self):
        if self.used_5050:
            messagebox.showinfo("Lifeline Used", "You have already used the 50:50 lifeline.")
            return
        self.used_5050 = True
        use_5050_lifeline(self.questions[self.current_index], self.radio_buttons)

    def ask_audience(self):
        if self.used_audience:
            messagebox.showinfo("Lifeline Used", "You have already used Ask the Audience.")
            return
        self.used_audience = True
        ask_audience_lifeline(self.questions[self.current_index])

    def show_leaderboard(self):
        view_leaderboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = KBCQuizGame(root)
    root.mainloop()
