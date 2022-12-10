from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Ask')


class RedditForm(FlaskForm):
    subreddit = StringField('Subreddit', validators=[DataRequired()])
    limit = StringField('Number of Posts to Scrape',
                        validators=[DataRequired()])
    submit = SubmitField('Download')


class UploadForm(FlaskForm):
    file = StringField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
