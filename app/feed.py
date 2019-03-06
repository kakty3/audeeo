import tempfile

from feedgen.feed import FeedGenerator

from . import models, ia_client


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

    for file in models.File.query.all():
        fe = fg.add_entry()
        fe.id(file.url)
        fe.title(file.filename)
        fe.enclosure(file.url, 0, 'audio/mpeg')

    return fg.rss_str(pretty=True)

def update_feed(ia_identifier):
    feed_ia_key = 'feed.xml'
    feed_body = generate_feed()
    
    with tempfile.TemporaryFile() as fp:
        fp.write(feed_body)
        fp.seek(0)
        ia_client.upload(
            identifier=ia_identifier,
            file=fp,
            key=feed_ia_key,
            force=True
        )
