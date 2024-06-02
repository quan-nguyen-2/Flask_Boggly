from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):


    def test_startup(self):
        with app.test_client() as client:
            resp = client.get('/boggle')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<span id='top'>0</span>", html)
            self.assertEqual(len(session['board']), 5)


    def test_submission(self):
        board = [['F', 'H', 'D', 'J', 'S'], ['L', 'H', 'D', 'G', 'S'], ['A', 'H', 'G', 'J', 'D'], ['G', 'J', 'D', 'K', 'D'], ['H', 'D', 'K', 'J', 'E']]
        with app.test_client() as client:
            resp = client.get('/submission?word=flag')
            json = resp.get_data(as_text=True)
            
            self.assertIn('{"response": "ok"}', json)


    def test_endgame(self):
        with app.test_client() as client:
            resp = client.post('/endgame', json={"score": 12})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['played'], 1)
            self.assertEqual(session['top'], 12)


    # TODO -- write tests for every view function / feature!
