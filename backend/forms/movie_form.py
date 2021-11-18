from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    release_date = DateField('release_date', validators=[DataRequired()])
