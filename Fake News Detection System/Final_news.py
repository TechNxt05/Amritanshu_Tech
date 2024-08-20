import tkinter as tk
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Create the Tkinter window
window = tk.Tk()
window.title("Fake News Detection System")

# Create a frame for the header
header_frame = tk.Frame(window, bg="#333333", padx=20, pady=20)
header_frame.pack(fill="x")

# Create the header label
heading = tk.Label(header_frame, text="Fake News Detection System", font=("Helvetica", 16, "bold"), fg="#FFFFFF", bg="#333333")
heading.pack()

# Create a frame for the content
content_frame = tk.Frame(window, padx=20, pady=20)
content_frame.pack()

# Load the data
data = pd.read_csv("news.csv")
x = np.array(data["title"])
y = np.array(data["label"])

# Initialize the model and vectorizer
cv = CountVectorizer()
x = cv.fit_transform(x)
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(xtrain, ytrain)

# Define the predict function
def predict_news():
    news_headline = entry.get()
    data = cv.transform([news_headline]).toarray()
    prediction = model.predict(data)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Predicted Label: " + str(prediction[0]))

# Create the content elements
label = tk.Label(content_frame, text="Enter a news headline:", font=("Helvetica", 12, "bold"))
label.pack()

entry = tk.Entry(content_frame, width=50, font=("Helvetica", 12, "bold"))
entry.pack()

predict_button = tk.Button(content_frame, text="Predict", command=predict_news, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#FFFFFF")
predict_button.pack(pady=10)

output_text = tk.Text(content_frame, height=2, width=40, font=("Helvetica", 12, "bold"))
output_text.pack()

window.mainloop()
