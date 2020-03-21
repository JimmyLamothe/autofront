import sys
from flask import Flask, redirect, url_for, render_template
sys.path.insert(1, '/Users/jimmy/Programming/Python/spotify')
from decorators import redirect_print
import Player
app = Flask(__name__)

player = Player.Player()

def clear_display():
    with open('display.txt', 'w') as out:
        pass

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/functions')
def functions():    
    with open('display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return render_template('functions.html', title = 'functions', display = display,
                           func_dicts = [{'link':'playnext', 'title':'Play next album'},
                                         {'link':'playcurrent', 'title':'Play current album'},
                                         {'link':'nexttrack', 'title':'Play next track'},
                                         {'link':'prevtrack', 'title':'Play previous track'},
                                         {'link':'showcurrent', 'title':'Show current track'},
                                         {'link':'playrandom', 'title':'Play random album'},
                                         {'link':'stop', 'title':'Stop play'},
                                         {'link':'follow', 'title':'Follow current artist'},
                                         {'link':'unfollow', 'title':'Unfollow current artist'}])

@app.route('/playnext')
def playnext():
    clear_display()
    @redirect_print
    def playnext():
        player.play_next_album()
    playnext()
    return redirect(url_for('functions'))

@app.route('/playcurrent')
def playcurrent():
    clear_display()
    @redirect_print
    def playcurrent():
        player.play_current_album()
    playcurrent()
    return redirect(url_for('functions'))

@app.route('/nexttrack')
def nexttrack():
    clear_display()
    @redirect_print
    def nexttrack():
        player.play_next_track()
    nexttrack()
    return redirect(url_for('functions'))

@app.route('/prevtrack')
def prevtrack():
    clear_display()
    @redirect_print
    def prevtrack():
        player.play_previous_track()
    prevtrack()
    return redirect(url_for('functions'))

@app.route('/showcurrent')
def showcurrent():
    clear_display()
    @redirect_print
    def showcurrent():
        player.show_current_track()
    showcurrent()
    return redirect(url_for('functions'))

@app.route('/playrandom')
def playrandom():
    clear_display()
    @redirect_print
    def playrandom():
        player.play_random_album()
    playrandom()
    return redirect(url_for('functions'))

@app.route('/stop')
def stop():
    clear_display()
    @redirect_print
    def stop():
        player.stop()
    stop()
    return redirect(url_for('functions'))

@app.route('/follow')
def follow():
    clear_display()
    @redirect_print
    def follow():
        player.follow()
    follow()
    return redirect(url_for('functions'))

@app.route('/unfollow')
def unfollow():
    clear_display()
    @redirect_print
    def unfollow():
        player.unfollow()
    unfollow()
    return redirect(url_for('functions'))


app.run(host='0.0.0.0', port = 5000)
