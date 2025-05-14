import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('mood_feedback.db')  # Create or open the database file
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 mood TEXT,
                 feedback TEXT)''')  # Create a table if not exists
    conn.commit()
    conn.close()

# Call init_db when starting the app
init_db()

@app.route('/')
def home():
    return "Flask is running!"

# Endpoint to save mood and feedback
@app.route('/submit', methods=['POST'])
def submit_feedback():
    data = request.get_json()  # Get data from frontend
    mood = data.get('mood')
    feedback = data.get('feedback')

    # Save to database
    conn = sqlite3.connect('mood_feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (mood, feedback) VALUES (?, ?)', (mood, feedback))
    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
