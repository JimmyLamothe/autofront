import sys
from flask import Flask, redirect, url_for, render_template
import func
sys.path.insert(1, '/Users/jimmy/Programming/Python/spotify')
import Player
app = Flask(__name__)

player = Player.Player()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/functions')
def functions():
    with open('test.txt', 'r') as filepath:
        display = filepath.read()
    return render_template('functions.html', title = 'functions', display = display,
                           func_dicts = [{'link':'playnext', 'title':'Play next album'},
                                         {'link':'playcurrent', 'title':'Play current album'},
                                         {'link':'playrandom', 'title':'Play random album'},
                                         {'link':'stop', 'title':'Stop play'},
                                         {'link':'follow', 'title':'Follow current artist'},
                                         {'link':'unfollow', 'title':'Unfollow current artist'}])

@app.route('/playnext')
def playnext():
    player.play_next_album()
    return redirect(url_for('functions'))

@app.route('/playcurrent')
def playcurrent():
    player.play_current_album()
    return redirect(url_for('functions'))

@app.route('/playrandom')
def playrandom():
    player.play_random_album()
    return redirect(url_for('functions'))

@app.route('/stop')
def stop():
    player.stop()
    return redirect(url_for('functions'))

@app.route('/follow')
def follow():
    player.follow()
    return redirect(url_for('functions'))

@app.route('/unfollow')
def unfollow():
    player.unfollow()
    return redirect(url_for('functions'))


app.run(host='0.0.0.0', port = 5000)
