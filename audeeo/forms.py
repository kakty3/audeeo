from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

AUDIO_EXTENSIONS = {'wav', 'mp3', 'aac', 'ogg', 'oga', 'flac'}

class FeedInfoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Length(min=0, max=255)])
    submit = SubmitField('Submit')

class UploadFileForm(FlaskForm):
    file = FileField(
        'Audio file',
        validators=[
            FileRequired(),
            FileAllowed(AUDIO_EXTENSIONS, 'Audio files only')
        ]
    )
    submit = SubmitField('Upload')
