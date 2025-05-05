import os
import json
import random
from tkinter import *
from tkinter import messagebox

class QuizUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.current_user = None
        self.current_category = None
        self.current_level = None
        self.score = 0
        self.current_question = 0
        self.questions = []
        self.time_left = 0
        self.timer = None
        self.unlocked_levels = ["easy"]

        self.bg_color = "#F0F8FF"
        self.btn_color = "#4682B4"
        self.text_color = "#2F4F4F"

        self.root.configure(bg=self.bg_color)

        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/questions"):
            os.makedirs("data/questions")

        self.scores_file = "data/scores.json"
        self.load_scores()

        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_home_screen()

    def on_closing(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.root.destroy()

    def load_scores(self):
        try:
            with open(self.scores_file, "r") as f:
                self.scores_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.scores_data = {"users": {}}

    def save_scores(self):
        with open(self.scores_file, "w") as f:
            json.dump(self.scores_data, f, indent=4)

    def create_home_screen(self):
        self.clear_screen()
        title = Label(self.root, text="Quiz Game", font=("Arial", 32, "bold"),
                      bg=self.bg_color, fg=self.text_color)
        title.pack(pady=30)

        btn_frame = Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        new_user_btn = Button(btn_frame, text="New Player", font=("Arial", 14),
                              bg=self.btn_color, fg="white", width=20,
                              command=self.new_user_screen)
        new_user_btn.pack(pady=10)

        existing_user_btn = Button(btn_frame, text="Existing Player", font=("Arial", 14),
                                  bg=self.btn_color, fg="white", width=20,
                                  command=self.existing_user_screen)
        existing_user_btn.pack(pady=10)

        quit_btn = Button(btn_frame, text="Quit", font=("Arial", 14),
                          bg="#CD5C5C", fg="white", width=20,
                          command=self.root.quit)
        quit_btn.pack(pady=10)

        footer = Label(self.root, text="Developed by Martix \n(Dembele Gaëtan , Paré Joseph , Sawadogo Azael , Zarani Kader ) \n @Copyrigth  2025", font=("Arial", 20), bg=self.bg_color, fg="gray")

        footer.pack(side=BOTTOM, pady=10)
        footer = Label(self.root, text="@Copyrigth 2025", font=("Arial", 5), bg=self.bg_color, fg="gray")        

    def new_user_screen(self):
        self.clear_screen()
        title = Label(self.root, text="New Player", font=("Arial", 24, "bold"),
                      bg=self.bg_color, fg=self.text_color)
        title.pack(pady=20)

        Label(self.root, text="Enter your name:", font=("Arial", 12),
              bg=self.bg_color).pack(pady=10)

        self.user_entry = Entry(self.root, font=("Arial", 14), width=30)
        self.user_entry.pack(pady=10)

        btn_frame = Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        confirm_btn = Button(btn_frame, text="Confirm", font=("Arial", 12),
                             bg=self.btn_color, fg="white",
                             command=self.create_new_user)
        confirm_btn.pack(side=LEFT, padx=10)

        back_btn = Button(btn_frame, text="Back", font=("Arial", 12),
                          bg="#CD5C5C", fg="white",
                          command=self.create_home_screen)
        back_btn.pack(side=LEFT, padx=10)

    def create_new_user(self):
        username = self.user_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        if username in self.scores_data["users"]:
            messagebox.showerror("Error", "This username already exists")
            return

        self.scores_data["users"][username] = {
            "scores": {},
            "stats": {
                "games_played": 0,
                "correct_answers": 0,
                "total_questions": 0
            }
        }
        self.save_scores()
        self.current_user = username
        self.category_selection_screen()

    def existing_user_screen(self):
        self.clear_screen()
        title = Label(self.root, text="Existing Player", font=("Arial", 24, "bold"),
                      bg=self.bg_color, fg=self.text_color)
        title.pack(pady=20)

        if not self.scores_data["users"]:
            Label(self.root, text="No registered players", font=("Arial", 12),
                  bg=self.bg_color).pack(pady=20)
            back_btn = Button(self.root, text="Back", font=("Arial", 12),
                              bg="#CD5C5C", fg="white",
                              command=self.create_home_screen)
            back_btn.pack(pady=10)
            return

        user_list_frame = Frame(self.root, bg=self.bg_color)
        user_list_frame.pack(pady=10)

        for i, username in enumerate(self.scores_data["users"].keys()):
            user_btn = Button(user_list_frame, text=username, font=("Arial", 12),
                              bg=self.btn_color, fg="white", width=20,
                              command=lambda u=username: self.select_existing_user(u))
            user_btn.grid(row=i, column=0, pady=5)

        back_btn = Button(self.root, text="Back", font=("Arial", 12),
                          bg="#CD5C5C", fg="white",
                          command=self.create_home_screen)
        back_btn.pack(pady=20)

    def select_existing_user(self, username):
        self.current_user = username
        self.unlocked_levels = ["easy"]
        user_scores = self.scores_data["users"][username].get("scores", {})
        for key in user_scores:
            if key.endswith("easy") and user_scores[key] >= 50:
                self.unlocked_levels.append("medium")
            if key.endswith("medium") and user_scores[key] >= 100:
                self.unlocked_levels.append("hard")
        self.category_selection_screen()

    def category_selection_screen(self):
        self.clear_screen()
        title = Label(self.root, text=f"Welcome, {self.current_user}!\nChoose a category:",
                      font=("Arial", 24, "bold"), bg=self.bg_color, fg=self.text_color)
        title.pack(pady=20)
        categories_path = "data/questions"
        categories = [d for d in os.listdir(categories_path) if os.path.isdir(os.path.join(categories_path, d))]
        if not categories:
            Label(self.root, text="No categories found!", font=("Arial", 14), bg=self.bg_color, fg="red").pack(pady=10)
            return
        cat_frame = Frame(self.root, bg=self.bg_color)
        cat_frame.pack(pady=20)
        for i, cat in enumerate(categories):
            Button(cat_frame, text=cat, font=("Arial", 14), bg=self.btn_color, fg="white", width=20,
                   command=lambda c=cat: self.level_selection_screen(c)).grid(row=i, column=0, pady=10)
        back_btn = Button(self.root, text="Back", font=("Arial", 12),
                          bg="#CD5C5C", fg="white", command=self.create_home_screen)
        back_btn.pack(pady=20)

    def level_selection_screen(self, category):
        self.current_category = category
        self.clear_screen()
        title = Label(self.root, text=f"Category: {self.current_category}\nWelcome, {self.current_user}!",
                      font=("Arial", 24, "bold"), bg=self.bg_color, fg=self.text_color)
        title.pack(pady=20)

        Label(self.root, text="Choose a level:", font=("Arial", 16),
              bg=self.bg_color).pack(pady=10)

        level_frame = Frame(self.root, bg=self.bg_color)
        level_frame.pack(pady=20)

        levels = ["easy", "medium", "hard"]
        level_names = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}

        for i, level in enumerate(levels):
            btn_state = NORMAL if level in self.unlocked_levels else DISABLED
            level_btn = Button(level_frame, text=level_names[level],
                               font=("Arial", 14), bg=self.btn_color, fg="white",
                               width=15, state=btn_state,
                               command=lambda l=level: self.start_quiz(self.current_category, l))
            level_btn.grid(row=i, column=0, pady=10, padx=20)

        score_frame = Frame(self.root, bg=self.bg_color)
        score_frame.pack(pady=20)

        Label(score_frame, text="Your best scores:", font=("Arial", 14, "bold"),
              bg=self.bg_color).grid(row=0, column=0, columnspan=2, pady=5)

        user_scores = self.scores_data["users"][self.current_user].get("scores", {})
        for i, level in enumerate(levels, start=1):
            score_key = f"{self.current_category}-{level}"
            Label(score_frame, text=f"{level_names[level]}:", font=("Arial", 12),
                  bg=self.bg_color).grid(row=i, column=0, sticky="e", padx=5)
            Label(score_frame,
                  text=str(user_scores.get(score_key, 0)),
                  font=("Arial", 12), bg=self.bg_color).grid(row=i, column=1, sticky="w")

        back_btn = Button(self.root, text="Back", font=("Arial", 12),
                          bg="#CD5C5C", fg="white",
                          command=self.category_selection_screen)
        back_btn.pack(pady=20)

    def start_quiz(self, category, level):
        file_path = f"data/questions/{category}/{level}.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.questions = data["questions"]
                random.shuffle(self.questions)
                self.questions = self.questions[:10]
        except FileNotFoundError:
            messagebox.showerror("Error", f"Question file not found for {category} - {level}")
            return

        self.score = 0
        self.current_question = 0
        self.time_left = 60 if level == "easy" else 45 if level == "medium" else 25
        self.current_level = level

        self.show_question()

    def show_question(self):
        self.clear_screen()
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

        if self.current_question >= len(self.questions):
            self.end_quiz()
            return

        question_data = self.questions[self.current_question]

        info_frame = Frame(self.root, bg=self.bg_color)
        info_frame.pack(pady=10)

        Label(info_frame, text=f"Question {self.current_question + 1}/{len(self.questions)}",
              font=("Arial", 12), bg=self.bg_color).pack(side=LEFT, padx=20)
        Label(info_frame, text=f"Score: {self.score}", font=("Arial", 12),
              bg=self.bg_color).pack(side=LEFT, padx=20)

        self.timer_label = Label(info_frame, text=f"Time: {self.time_left}s",
                                 font=("Arial", 12), bg=self.bg_color)
        self.timer_label.pack(side=LEFT, padx=20)
        self.start_timer()

        question_frame = Frame(self.root, bg=self.bg_color)
        question_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        Label(question_frame, text=question_data["question"],
              font=("Arial", 16, "bold"), bg=self.bg_color, wraplength=700).pack(pady=20)

        options_frame = Frame(question_frame, bg=self.bg_color)
        options_frame.pack(pady=10)

        self.selected_option = IntVar()
        self.selected_option.set(-1)

        for i, option in enumerate(question_data["options"]):
            Radiobutton(options_frame, text=option, font=("Arial", 14),
                        variable=self.selected_option, value=i, bg=self.bg_color,
                        selectcolor=self.bg_color).grid(row=i, column=0, sticky="w", pady=5)

        next_btn = Button(question_frame, text="Next", font=("Arial", 14),
                          bg=self.btn_color, fg="white", width=15,
                          command=self.check_answer)
        next_btn.pack(pady=20)

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.time_left -= 1
            self.timer = self.root.after(1000, self.start_timer)
        else:
            self.timer_label.config(text="Time's up!")
            if self.root.winfo_exists():
                messagebox.showinfo("Time's up", "Time is over! The quiz will end now.")
            self.end_quiz()

    def check_answer(self):
        question_data = self.questions[self.current_question]
        selected = self.selected_option.get()

        if selected == -1:
            messagebox.showwarning("Warning", "Please select an answer")
            return

        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

        if selected == question_data["correct_answer"]:
            self.score += 10 * (3 if self.current_level == "hard" else 2 if self.current_level == "medium" else 1)
            messagebox.showinfo("Correct!", f"Good answer!\n\n{question_data.get('explanation', '')}")
        else:
            correct_answer = question_data["options"][question_data["correct_answer"]]
            messagebox.showinfo("Incorrect",
                                f"Wrong answer. The correct answer was: {correct_answer}\n\n{question_data.get('explanation', '')}")

        self.current_question += 1
        self.show_question()

    def end_quiz(self):
        user_scores = self.scores_data["users"][self.current_user]["scores"]
        score_key = f"{self.current_category}-{self.current_level}"
        if self.score > user_scores.get(score_key, 0):
            user_scores[score_key] = self.score

        user_stats = self.scores_data["users"][self.current_user]["stats"]
        user_stats["games_played"] += 1
        user_stats["total_questions"] += len(self.questions)
        user_stats["correct_answers"] += self.score // (10 * (3 if self.current_level == "hard" else 2 if self.current_level == "medium" else 1))

        self.save_scores()

        if self.current_level == "easy" and self.score >= 50 and "medium" not in self.unlocked_levels:
            self.unlocked_levels.append("medium")
            messagebox.showinfo("Level unlocked", "Congratulations! You unlocked the medium level!")
        elif self.current_level == "medium" and self.score >= 100 and "hard" not in self.unlocked_levels:
            self.unlocked_levels.append("hard")
            messagebox.showinfo("Level unlocked", "Congratulations! You unlocked the hard level!")

        self.clear_screen()
        title = Label(self.root, text="Quiz Finished!", font=("Arial", 24, "bold"),
                      bg=self.bg_color, fg=self.text_color)
        title.pack(pady=20)

        result_frame = Frame(self.root, bg=self.bg_color)
        result_frame.pack(pady=20)

        Label(result_frame, text=f"Your final score: {self.score}",
              font=("Arial", 18), bg=self.bg_color).grid(row=0, column=0, pady=10)

        Label(result_frame, text=f"Level: {self.current_level}",
              font=("Arial", 16), bg=self.bg_color).grid(row=1, column=0, pady=5)

        btn_frame = Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20)

        replay_btn = Button(btn_frame, text="Replay", font=("Arial", 14),
                            bg=self.btn_color, fg="white", width=15,
                            command=lambda: self.start_quiz(self.current_category, self.current_level))
        replay_btn.pack(side=LEFT, padx=10)

        levels_btn = Button(btn_frame, text="Choose Levels", font=("Arial", 14),
                            bg=self.btn_color, fg="white", width=15,
                            command=lambda: self.level_selection_screen(self.current_category))
        levels_btn.pack(side=LEFT, padx=10)

        home_btn = Button(btn_frame, text="Home", font=("Arial", 14),
                          bg="#CD5C5C", fg="white", width=15,
                          command=self.create_home_screen)
        home_btn.pack(side=LEFT, padx=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
