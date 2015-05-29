from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devkey'
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
Bootstrap(app)

db = SQLAlchemy(app)
db.create_all()

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idea = db.Column(db.String(256), unique=True)

    def __init__(self, idea):
        self.idea = idea

    def __repr__(self):
        return '<Idea %r>' % self.id

class IdeaForm(Form):
    idea = StringField('idea', validators=[DataRequired()])
    submit_button = SubmitField('add idea')

@app.route("/", methods=["GET", "POST"])
def hello():
    form = IdeaForm()
    submitted_idea = '<empty idea field>'
    if form.validate_on_submit():
        submitted_idea=form.idea.data

    return render_template("index.html", form=form, submitted_idea=submitted_idea)

if __name__ == "__main__":
    app.run(debug=True)