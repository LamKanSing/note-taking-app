__author__ = 'line'

from flask import Flask

app = Flask(__name__)

'''
testing comment
'''
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()