from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key for sessions

boggle_game = Boggle()

@app.route('/')
def index():
    """Return homepage."""
    return render_template("index.html")

@app.route('/board_game')
def display_board():
    """Display the Boggle board."""
    board = boggle_game.make_board()
    session['board'] = board  # Save the board in session
    session['guessed_words'] = []  # Initialize guessed words as an empty list
    return render_template("board.html", board=board)

@app.route('/check_word', methods=['POST'])
def check_word():
    """Check if a word is valid."""
    word = request.json['word']
    board = session['board']
    guessed_words = session.get('guessed_words', [])
    
    if word in guessed_words:
        return jsonify({'result': 'duplicate'})
    
    result = boggle_game.check_valid_word(board, word)
    guessed_words.append(word)
    session['guessed_words'] = guessed_words
    
    return jsonify({'result': result})

@app.route('/end_game', methods=['POST'])
def end_game():
    """End the game and update statistics."""
    score = request.json['score']
    plays = session.get('plays', 0)
    high_score = session.get('high_score', 0)

    # Update statistics
    plays += 1
    if score > high_score:
        high_score = score

    session['plays'] = plays
    session['high_score'] = high_score

    return jsonify({'plays': plays, 'high_score': high_score})

if __name__ == '__main__':
    app.run(debug=True)
