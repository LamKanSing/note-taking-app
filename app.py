from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields import FloatField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf.recaptcha import RecaptchaField

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

RECAPTCHA_PUBLIC_KEY = '6Lc0vgcTAAAAAG4YGZ60-Cox3OYt-qOg4O1rxVbR'
RECAPTCHA_PRIVATE_KEY = '6Lc0vgcTAAAAAKePomdmMUBX8UCf3LOpho64_1jO'

Bootstrap(app)

db = SQLAlchemy(app)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idea_name = db.Column(db.String(256), unique=True)

    def __init__(self, idea):
        self.idea_name = idea

    def __repr__(self):
        return '<Idea %r>' % self.id

db.create_all()

class IdeaForm(Form):
    idea_name = StringField('idea', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    testing = StringField('testing', validators=[DataRequired()])
    submit_button = SubmitField('add idea')

@app.route("/", methods=["GET", "POST"])
def index():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(form.idea_name.data)
        db.session.add(idea)
        db.session.commit()

    idealist = Idea.query.all()
    return render_template("index.html", form=form, idealist = idealist)

if __name__ == "__main__":
    app.run(debug=True)