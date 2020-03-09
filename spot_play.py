import sys, contextlib, datetime
from flask import Flask, redirect, url_for, render_template
import func
sys.path.insert(1, '/Users/jimmy/Programming/Python/spotify')
import Player
app = Flask(__name__)

player = Player.Player()
#player.play_next_album()

def redirect_print(func):
    def inner1():
        with open('test.txt', 'a') as out:
            print(datetime.datetime.now())
            with contextlib.redirect_stdout(out):
                print(datetime.datetime.now())
                print(func.__name__)
                return func()
    return inner1


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/functions')
def functions():
    return render_template('functions.html', title = 'functions',
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

with open('test.txt', 'w') as out:
    with contextlib.redirect_stdout(out):
        app.run(host='0.0.0.0', port = 5000)
