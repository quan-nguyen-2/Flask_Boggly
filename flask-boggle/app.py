from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def start():
    session['board'] = boggle_game.make_board()
    board = session['board']
    top = session.get('top', 0)
    played = session.get('played', 0)
    return render_template('index.html', board=board, top=top, played=played)

@app.route('/submission')
def check_word():
    word = request.args['word']
    word = word.lower()
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"result": response})

@app.route('/endgame', methods=["POST"])
def end_game():
    score = request.json['score']
    top = session.get('top', 0)
    played = session.get('played', 0)
    session['played'] = played + 1
    session['top'] = max(score, top)
    played = session['played']
    top = session['top']
    return jsonify({"top": top})