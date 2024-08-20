from tkinter import *
from tkinter import ttk  # Import ttk module for Separator
import tkinter.messagebox as tmsg
from PIL import ImageTk, Image
import csv

root = Tk()
root.geometry("1000x700")
root.title("Login to Voting System")

voter_lst = ["Voter1", "Voter2", "Voter3", "Voter4", "Voter5"]
candidate_lst = ["AAM ADMI PARTY          ", "CONGRESS                    ", "SAMAJWADI PARTY       ", "BHARTIYA JANTA PARTY"]
votes = {candidate: 0 for candidate in candidate_lst}
voted = []

def login():
    entry_value = entry.get()
    if entry_value in voter_lst:
        tmsg.showinfo("Logged In", f"{entry_value} is logged in")
        lbl["text"] = f"{entry_value} is logged in."
        for button in vote_buttons.values():
            button["state"] = "normal"

        if entry_value in voted:
            lbl["text"] = f"{entry_value} is logged in."
            for button in vote_buttons.values():
                button["state"] = "disabled"
        else:
            voted.append(entry_value)

def vote(candidate):
    votes[candidate] += 1
    score_lbl[candidate]["text"] = f"Votes for {candidate} is: {votes[candidate]}"
    for button in vote_buttons.values():
        button["state"] = "disabled"

    # Write the vote results to a CSV file
    with open("voting_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Candidate", "Votes"])
        for candidate, vote_count in votes.items():
            writer.writerow([candidate, vote_count])

# Header frame
header_frame = Frame(root, borderwidth=4, bg="blue")
header_frame.pack(fill=X)

# Heading label
heading_label = Label(header_frame, text="Online Voting System", fg="white", bg="blue", font=("Arial", 20, "bold"))
heading_label.pack(pady=2)

f1 = Frame(root, borderwidth=7, bg="blue")
f1.pack(fill=X)
entry = Entry(f1, font=("Helvetica", 20, "bold"))
entry.pack()
login_btn = Button(root, text="Login", bg="blue", fg="white", font=("arial", 15, "bold"), command=login)
login_btn.pack(pady=3)

lbl = Label(root, text="", fg="lime", font=("arial", 15, "bold"))
lbl.pack()

candidate_photos = {
    "AAM ADMI PARTY          ": "AAP.jpg",
    "CONGRESS                    ": "CONG.jpg",
    "SAMAJWADI PARTY       ": "SAPA.jpg",
    "BHARTIYA JANTA PARTY": "BJP.jpg"
}

vote_buttons = {}
for i, candidate in enumerate(candidate_lst):
    # Load candidate photo
    candidate_photo = ImageTk.PhotoImage(Image.open(candidate_photos[candidate]).resize((80, 80)))

    # Create a frame to hold the candidate name and image
    candidate_frame = Frame(root)
    candidate_frame.pack(fill=X, pady=10)

    # Create a label for the candidate name with spacing
    candidate_label = Label(candidate_frame, text=candidate, font=("Helvetica", 15, "bold"))
    candidate_label.pack(side=LEFT, padx=300)  # Add padding to the left using padx

    # Create vote button with photo
    vote_buttons[candidate] = Button(candidate_frame, state="disabled", relief=RIDGE,
                                    font=("Helvetica", 15, "bold"), command=lambda candidate=candidate: vote(candidate))
    vote_buttons[candidate].config(image=candidate_photo, compound=RIGHT)
    vote_buttons[candidate].photo = candidate_photo
    vote_buttons[candidate].pack()

    # Add separator line
    if i < len(candidate_lst) - 1:
        separator = ttk.Separator(root, orient=HORIZONTAL)
        separator.pack(fill=X, padx=10, pady=5)

score_lbl = {}
for candidate in candidate_lst:
    score_lbl[candidate] = Label(root, text="", font=("arial", 20))
    score_lbl[candidate].pack()

root.mainloop()
