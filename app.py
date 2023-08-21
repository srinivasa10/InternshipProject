from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file and preprocess the dataset
def load_dataset(file_path):
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    return df

train_dataset = load_dataset("questions.csv")
valid_dataset = load_dataset("valid.csv")

# Function to generate an answer given a question or prompt
def generate_answer(question_or_prompt):
    question_or_prompt = question_or_prompt.lower()

    if question_or_prompt in ["thank you", "thanks", "thankyou"]:
        # Generate a thank you response
        thank_you_message = "You're welcome! If you have any more questions, feel free to ask."
        return thank_you_message

    if question_or_prompt in ["hi", "hello"]:
        greeting_message = "Welcome to the Medicine related Q&A bot! How can I assist you today?"
        return greeting_message

    # Search for the question in the dataset
    answer = valid_dataset[valid_dataset['question'].str.lower() == question_or_prompt]['answer'].iloc[0]

    if pd.notnull(answer):
        precaution_caption = "Precaution: Please consult with a healthcare professional for personalized advice."
        answer_with_precaution = f"{answer}\n\n{precaution_caption}"
        return answer_with_precaution
    else:
        return "I'm sorry, I couldn't find an answer to that question in the dataset."

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for processing user messages
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    bot_response = generate_answer(user_message)

    if bot_response == "":
        bot_response = "I'm sorry, I couldn't generate a reply for that."

    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
