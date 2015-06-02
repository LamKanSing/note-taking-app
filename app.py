from flask import Flask, redirect
from flask import render_template
from flask_bootstrap import Bootstrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields import FloatField
from wtforms.validators import DataRequired, Optional, NumberRange, Email
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devkey'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


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
    testing = FloatField('price', validators=[NumberRange
                                              (min=0.3, max=10.3, message='between 0.3 to 10.3, inclusive')])
    email = StringField('email', validators=[Email(), 'it is not an email'])
    submit_button = SubmitField('add idea')
    #how about a custom validator.....


@app.route("/", methods=["GET", "POST"])
def index():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(form.idea_name.data)
        db.session.add(idea)
        db.session.commit()
    elif form.is_submitted() and not form.validate():
        return redirect("http://www.google.com", code=302)

    idealist = Idea.query.all()
    return render_template("index.html", form=form, idealist = idealist)

if __name__ == "__main__":
    app.run(debug=True)