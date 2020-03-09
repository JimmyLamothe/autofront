from flask import Flask, redirect, url_for, render_template
import func
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/functions')
def functions():
    return render_template('functions.html', title = 'functions',
                           func_dicts = [{'link':'a', 'title':'aaaaaa'},
                                         {'link':'b', 'title':'bbbbbb'},
                                         {'link':'c', 'title':'cccccc'}])

@app.route('/a')
def a():
    func.a()
    return redirect(url_for('functions'))

@app.route('/b')
def b():
    func.b()
    return redirect(url_for('functions'))

@app.route('/c')
def c():
    func.c()
    return redirect(url_for('functions'))
