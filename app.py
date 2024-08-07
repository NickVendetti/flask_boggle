from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

boggle_game = Boggle()

@app.route('/')
def home():
    """Render the home page with a link to start the game."""
    return render_template('home.html')

@app.route('/board_game')
def display_board():
    """Display the Boggle board."""
    board = boggle_game.make_board()
    session['board'] = board  # Save the board in session
    session['guessed_words'] = []  # Initialize guessed words as an empty list (now using list)
    return render_template("board.html", board=board)

@app.route('/check_word', methods=['POST'])
def check_word():
    """Check if a word is valid and handle duplicates."""
    word = request.json['word']
    board = session['board']
    guessed_words = session.get('guessed_words', [])

    if word in guessed_words:
        return jsonify({'result': 'duplicate'})

    result = boggle_game.check_valid_word(board, word)
    if result == 'ok':
        guessed_words.append(word)
        session['guessed_words'] = guessed_words

    return jsonify({'result': result})

@app.route('/end_game', methods=['POST'])
def end_game():
    """Handle end of the game: increment plays and update high score."""
    score = request.json['score']
    plays = session.get('plays', 0)
    high_score = session.get('high_score', 0)

    session['plays'] = plays + 1
    if score > high_score:
        session['high_score'] = score

    return jsonify({'plays': session['plays'], 'high_score': session['high_score']})
