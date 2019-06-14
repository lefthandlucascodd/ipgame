from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    favorite_ip = TextAreaField('Favorite IP', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username, this one be taken.')


class NoteForm(FlaskForm):
    note = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=280)])
    submit = SubmitField('Submit')


class IPForm(FlaskForm):
    name = StringField('Name your Intellectual Property:', validators=[DataRequired(), Length(min=1, max=120)])
    description = TextAreaField("What's it all about?", validators=[DataRequired(), Length(min=1, max=280)])
    clout = IntegerField('Set the starting clout:', validators=[DataRequired()])
    estimated_value = IntegerField("How much is it worth? $", validators=[DataRequired()])
    submit = SubmitField('Create it!')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
