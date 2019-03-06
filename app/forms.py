from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired

AUDIO_EXTENSIONS = {'wav', 'mp3', 'aac', 'ogg', 'oga', 'flac'}

class UploadFileForm(FlaskForm):
    file = FileField(
        'Audio file',
        validators=[
            FileRequired(),
            FileAllowed(AUDIO_EXTENSIONS, 'Audio files only')
        ]
    )
    submit = SubmitField('Upload')
