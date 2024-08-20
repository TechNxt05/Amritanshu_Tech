import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import subprocess
import time
import json
import csv

class Quiz:
    def __init__(self, name, roll_no):
        self.q_no = 0
        self.display_title()
        self.display_question()
        self.opt_selected = tk.IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.data_size = len(question)
        self.correct = 0
        self.start_time = time.time()  # Start the timer
        self.name = name
        self.roll_no = roll_no

    def display_result(self):
        elapsed_time = round(time.time() - self.start_time)  # Calculate elapsed time
        timer_minutes = elapsed_time // 60
        timer_seconds = elapsed_time % 60
        timer = f"Time: {timer_minutes} minutes {timer_seconds} seconds"
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%\n{timer}"
        name = self.name
        roll_no = self.roll_no
        messagebox.showinfo("Name -", f"{name}\nResult: {result}\n{correct}\n{wrong}")
        with open('quiz_results.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(['Name', 'Roll No.', 'Correct Answers', 'Wrong Answers', 'Percentage', 'Time'])
            writer.writerow([name, roll_no, self.correct, wrong_count, score, f"{timer_minutes}m {timer_seconds}s"])

    def check_ans(self, q_no):
        if self.opt_selected.get() == answer[q_no]:
            return True

    def next_btn(self):
        if self.check_ans(self.q_no):
            self.correct += 1
        self.q_no += 1
        if self.q_no == self.data_size:
            self.display_result()
            gui.destroy()
        else:
            self.display_question()
            self.display_options()

    def buttons(self):
        next_button = tk.Button(gui, text="Next", command=self.next_btn,
                             width=10, bg="blue", fg="white", font=("Arial", 16, "bold"))
        next_button.place(x=350, y=380)
        quit_button = tk.Button(gui, text="Quit", command=gui.destroy,
                             width=5, bg="black", fg="white", font=("Arial", 16, " bold"))
        quit_button.place(x=700, y=50)

    def display_options(self):
        val = 0
        self.opt_selected.set(0)
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1

    def display_question(self):
        q_no = tk.Label(gui, text=question[self.q_no], width=60,
                     font=('Arial', 16, 'bold'), anchor='w')
        q_no.place(x=70, y=100)

    def display_title(self):
        title = tk.Label(gui, text="OOPS QUIZ",
                      width=50, bg="green", fg="white", font=("Arial", 20, "bold"))
        title.place(x=0, y=2)

    def radio_buttons(self):
        q_list = []
        y_pos = 150
        while len(q_list) < 4:
            radio_btn = tk.Radiobutton(gui, text=" ", variable=self.opt_selected,
                                    value=len(q_list) + 1, font=("Arial", 14))
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

def validate_login():
    username = username_entry.get().lower()
    password = password_entry.get().lower()

    if login_data.get(username) == password:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        root.destroy()
        show_instructions(username, password)
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

def show_instructions(username, password):
    window = tk.Tk()
    window.title("Quiz Instructions")
    window.geometry("400x400")
    window.configure(bg="lightblue")

    def start_quiz():
        window.destroy()
        start_quiz_with_username(username, password)

    # Create and place the instruction label
    instruction_label = tk.Label(window, text="Instructions", font=('Arial', 20, 'bold'), bg="lightblue")
    instruction_label.pack(pady=20)

    # Create a list of instructions
    instructions = [
        "1. Read each question carefully before answering.",
        "2. Select the correct option from the given choices.",
        "3. You cannot go back to a previous question once answered.",
        "4. Each question carries equal marks.",
        "5. Click the 'Next' button to proceed to the next question.",
        "6. Time Limit - 30  mins"
    ]

    # Create and place the instruction text labels
    for i, text in enumerate(instructions):
        label = tk.Label(window, text=text, font=('Arial', 12), bg="lightblue")
        label.pack(pady=5)

    # Create the "Next" button
    next_button = tk.Button(window, text="Next", font=('Arial', 12), command=start_quiz)
    next_button.pack(pady=20)

    # Start the tkinter event loop
    window.mainloop()

def start_quiz_with_username(username, password):
    global gui
    gui = tk.Tk()
    gui.geometry("800x500")
    gui.title("Quiz")
    with open('abc.json') as f:
        data = json.load(f)
    global question
    question = data['question']
    global options
    options = data['options']
    global answer
    answer = data['answer']
    quiz = Quiz(username, password)
    timer_label = tk.Label(gui, text="Time: 30:00", font=("Arial", 14, "bold"))
    timer_label.place(x=670, y=10)  # Position the timer label

    def update_timer():
        elapsed_time = round(time.time() - quiz.start_time)
        remaining_time = max(30 * 60 - elapsed_time, 0)
        timer_minutes = remaining_time // 60
        timer_seconds = remaining_time % 60
        timer_label.config(text=f"Time: {timer_minutes:02d}:{timer_seconds:02d}")
        if remaining_time > 0:
            gui.after(1000, update_timer)  # Update timer every second
        else:
            quiz.display_result()
            gui.destroy()

    update_timer()  # Start the timer
    gui.mainloop()

# Login page data (username: password)
login_data = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5"
}

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.configure(bg="#F5F5F5")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create the header frame
header_frame = tk.Frame(root, bg="#3399FF")
header_frame.pack(fill="x", padx=10, pady=20)

# Create and configure the header label with the image
header_image = ImageTk.PhotoImage(Image.open("LOGO.png"))
header_label = tk.Label(header_frame, image=header_image, bg="#3399FF")
header_label.image = header_image  # Retain reference to the image
header_label.pack(pady=10)

# Create and configure the heading label
heading_label = tk.Label(header_frame, text="Login Page", font=("Arial", 32, "bold"), bg="#3399FF", fg="#FFFFFF")
heading_label.pack(pady=10)

# Create the login frame
login_frame = tk.Frame(root, bg="#F5F5F5")
login_frame.pack(padx=10, pady=20)

# Create and configure the username label and entry
username_label = tk.Label(login_frame, text="Username:", font=("Arial", 20), bg="#F5F5F5", fg="#333333")
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
username_entry = tk.Entry(login_frame, font=("Arial", 18))
username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Create and configure the password label and entry
password_label = tk.Label(login_frame, text="Password:", font=("Arial", 20), bg="#F5F5F5", fg="#333333")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(login_frame, show="*", font=("Arial", 18))
password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Create and configure the login button
login_button = tk.Button(root, text="Login", command=validate_login, font=("Arial", 20, "bold"), bg="#4CAF50", fg="#FFFFFF")
login_button.pack(pady=20)

# Center the window on the screen
window_x = int((screen_width / 2) - (root.winfo_width() / 2))
window_y = int((screen_height / 2) - (root.winfo_height() / 2))
root.geometry(f"+{window_x}+{window_y}")
# Start the tkinter event loop
root.mainloop()
