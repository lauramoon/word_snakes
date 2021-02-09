from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "mind-boggling"

boggle_game = Boggle()

@app.route('/')
def show_game():
    """create a new board, save it in session, show webpage"""
    board = boggle_game.make_board()
    session["board"] = board
    return render_template('index.html')

@app.route('/check-word/<word>')
def check_word(word):
    """determine if submitted word is valid, return result"""
    result = boggle_game.check_valid_word(session["board"], word)
    return jsonify({"result": result})

@app.route('/final-score', methods=['POST'])
def update_stats():
    """handle final score, save highest score and game count in session,
    return if new high score, highest score, and game count"""
    session['count'] = session.get('count', 0) + 1
    score = request.json['score']
    high_score = session.get('high_score', 0)
    congrats = False
    if score > high_score:
        session['high_score'] = score
        high_score = score
        congrats = True

    return jsonify({
        "count": session["count"],
        "high_score": high_score,
        "congrats": congrats
    })
    
