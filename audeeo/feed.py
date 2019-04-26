from email.utils import formatdate
import tempfile

from feedgen.feed import FeedGenerator

from audeeo import models


FEED_KEY = 'feed.xml'


def generate_feed():
    """Generate podcast RSS feed
    Spec: iTunes Podcast RSS: https://github.com/simplepie/simplepie-ng/wiki/Spec:-iTunes-Podcast-RSS
    
    :return: Contents of podcast RSS feed
    :rtype: bytes
    """

    fg = FeedGenerator()
    fg.load_extension('podcast')

    fg.title('Audeeo')
    fg.description('Audeeo test feed description')
    fg.link(href='https://exmaple.com', rel='self')

    for episode in models.Episode.query.all():
        fe = fg.add_entry()
        fe.id(episode.url)
        fe.title(episode.title)
        fe.enclosure(episode.url, str(episode.file_size), 'audio/mpeg')
        fe.pubDate(formatdate(episode.created_at.timestamp()))

    return fg.rss_str(pretty=True)

def update_feed(ia_identifier, ia_client):
    feed_body = generate_feed()
    
    with tempfile.TemporaryFile() as fp:
        fp.write(feed_body)
        fp.seek(0)
        return ia_client.upload(
            identifier=ia_identifier,
            file=fp,
            key=FEED_KEY,
            force=True
        )