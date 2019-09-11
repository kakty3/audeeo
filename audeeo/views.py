import os
import tempfile
import uuid

from flask import request, flash, redirect, render_template, Blueprint
from flask import current_app as app
from flask_login import current_user
from flask_security import login_required

from audeeo import models, forms, utils
from audeeo.database import db


FEED_KEY = 'feed.xml'

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_feed = current_user.feeds.first()

    upload_form = forms.UploadFileForm(prefix='upload_form')
    feed_info_form = forms.FeedInfoForm(prefix='feed_info_form')

    if feed_info_form.submit.data and feed_info_form.validate_on_submit():
        user_feed.title = feed_info_form.title.data
        user_feed.description = feed_info_form.description.data
        db.session.commit()

    if upload_form.submit.data and upload_form.validate_on_submit():
        file = upload_form.file.data
        if not utils.is_audio(file):
            message = 'Not audio file'
            flash(message, 'error')
            app.logger.info(message)

            return redirect(request.url)

        app.logger.info('Upload file')
        file_key = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        response = app.ia_client.upload(identifier=user_feed.ia_identifier, file=file, key=file_key)

        file_url = app.ia_client.get_file_url(user_feed.ia_identifier, file_key)
        message = 'Episode uploaded: {url}'.format(url=file_url)
        app.logger.info(message)
        flash(message, 'info')

        file_size = int(response.request.headers['Content-Length'])
        title = os.path.splitext(file.filename)[0].strip()
        episode = models.Episode(title=title, url=file_url, file_size=file_size)
        app.logger.debug('Episode: %s', episode)
        user_feed.episodes.append(episode)
        # db.session.add(episode)
        db.session.commit()

        app.logger.info('Update feed')
        user_feed_rss = user_feed.get_rss()
        # TODO: try use SpooledTemporaryFile
        with tempfile.TemporaryFile() as temp_file:
            temp_file.write(user_feed_rss)
            temp_file.seek(0)
            app.ia_client.upload(
                identifier=user_feed.ia_identifier,
                file=temp_file,
                key=FEED_KEY,
                force=True
            )

    feed_url = app.ia_client.get_file_url(user_feed.ia_identifier, FEED_KEY)
    episodes = user_feed.episodes.order_by(models.Episode.created_at.desc()).all()

    return render_template(
        'index.html',
        episodes=episodes,
        upload_form=upload_form,
        feed_info_form=feed_info_form,
        feed=user_feed,
        feed_url=feed_url)


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'
