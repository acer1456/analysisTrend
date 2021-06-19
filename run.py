import webbrowser
import os
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template
from ptt import ptt_run
from dcard import dcard_run
from cop import cop_run

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name, path=fn))
    return tree

ptt_data = ptt_run()
dcard_data = dcard_run()
cop_data = cop_run()

app = Flask(__name__,static_folder='web/',template_folder='web/templates')
run_with_ngrok(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/ptt_data')
def ptt_data():
    path = 'web/PTT'
    return render_template('files.html', tree=make_tree(path))

@app.route('/Cop_data')
def Cop_data():
    path = 'web/Cop'
    return render_template('files.html', tree=make_tree(path))

@app.route('/Dcard_data')
def Dcard_data():
    path = 'web/Dcard'
    return render_template('files.html', tree=make_tree(path))

@app.route("/ptt")
def ptt():
    return ptt_data

@app.route("/dcard")
def dcard():
    return dcard_data

@app.route("/cop")
def cop():
    return cop_data

if __name__ == "__main__":
    # webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()