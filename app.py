from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)

@app.route('/save', methods=['POST'])
def save_feedback():
    data = request.get_json()
    mood = data.get('mood')
    feedback_text = data.get('feedback')

    if not mood or not feedback_text:
        return jsonify({'error': 'Mood and feedback are required.'}), 400

    new_feedback = Feedback(mood=mood, feedback=feedback_text)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback saved successfully!'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # <-- inside app context
    app.run(debug=True)
