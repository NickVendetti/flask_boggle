from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Setup a test client and a fresh Boggle game."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.boggle_game = Boggle()

    def test_index_page(self):
        """Test the homepage."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Boggle Game', response.data)

    def test_display_board(self):
        """Test if the Boggle board is displayed correctly."""
        with self.client as client:
            response = client.get('/board_game')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boggle Game', response.data)
            self.assertIn(b'Enter your guess', response.data)

    def test_check_word_valid(self):
        """Test if a valid word is checked correctly."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            valid_word = 'TEST'
            response = client.post('/check_word', json={'word': valid_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

    def test_check_word_not_on_board(self):
        """Test if a word not on the board is handled correctly."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            invalid_word = 'INVALID'
            response = client.post('/check_word', json={'word': invalid_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_word_not_a_word(self):
        """Test if a non-dictionary word is handled correctly."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            not_a_word = 'XZY'
            response = client.post('/check_word', json={'word': not_a_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

    def test_end_game(self):
        """Test the end game statistics update."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            score = 10
            response = client.post('/end_game', json={'score': score})
            self.assertEqual(response.status_code, 200)
            self.assertGreaterEqual(response.json['plays'], 1)
            self.assertEqual(response.json['high_score'], max(score, session.get('high_score', 0)))

    def test_duplicate_word(self):
        """Test that duplicate words are not counted twice."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            valid_word = 'TEST'
            # Submit the word once
            client.post('/check_word', json={'word': valid_word})
            # Submit the word again
            response = client.post('/check_word', json={'word': valid_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')
            # Check that the score is not incremented again
            self.assertEqual(session.get('score', 0), len(valid_word))

    def test_timer(self):
        """Test if the timer functionality is working (simulate a 60s timer)."""
        with self.client as client:
            client.get('/board_game')  # Ensure board is initialized
            # The client side has to handle the timer, so this might be more complex to test directly
            # You may need to test if the game ends properly or simulate time in the client-side JavaScript
            pass

if __name__ == "__main__":
    import unittest
    unittest.main()
