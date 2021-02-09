from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json


class FlaskTests(TestCase):
    """Tests for the flask back-end of the boggle app"""

    def test_load_home_page(self):
        """Test that page loads in root directory"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Word Snakes</h1>', html)

    def test_session_on_load(self):
        """Test that board is saved in session when root directory requested"""
        with app.test_client() as client:
            resp = client.get('/')

            self.assertIsInstance(session['board'], list)
            self.assertEqual(len(session["board"]), 5)
            self.assertEqual(len(session["board"][0]), 5)

    def test_word_check(self):
        """Test that word_check route works"""
        with app.test_client() as client:
            setup = client.get('/')
            resp = client.get('/check-word/run')
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('result', data)

    def test_check_gibberish(self):
        """Check that non-word is get 'not-word' response"""
        with app.test_client() as client:
            setup = client.get('/')
            resp = client.get('/check-word/asdfsdgdsa')
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-word', data)

    def test_check_long_word(self):
        """Check that real and long word not on board"""
        with app.test_client() as client:
            setup = client.get('/')
            resp = client.get('/check-word/individualism')
            data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-on-board', data)

    def test_final_score(self):
        """Check that final_score route works with no initial changes to session"""
        with app.test_client() as client:
            resp = client.post('/final-score', 
                               json={'score': 55})
            json_data = resp.get_data(as_text=True)
            data = json.loads(json_data)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data['high_score'], 55)
            self.assertEqual(data['congrats'], True)
            self.assertEqual(data['count'], 1)
    
    def test_final_score_preset(self):
        """Check that final_score route works with values already in session"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['count'] = 920
                change_session['high_score'] = 45

            resp = client.post('/final-score', 
                               json={'score': 30})
            json_data = resp.get_data(as_text=True)
            data = json.loads(json_data)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data['high_score'], 45)
            self.assertEqual(data['congrats'], False)
            self.assertEqual(data['count'], 921)



    

