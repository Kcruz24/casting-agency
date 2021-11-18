from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired

from backend.enums.gender_enum import Gender


class ActorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    gender = SelectMultipleField('gender', validators=[DataRequired()],
                         choices=Gender.choices())
