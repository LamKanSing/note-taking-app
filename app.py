from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='devkey'
Bootstrap(app)


class MyForm(Form):
    idea = StringField('idea', validators=[DataRequired()])
    submit_button = SubmitField('add idea')

@app.route("/")
def hello():
    form = MyForm()
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)