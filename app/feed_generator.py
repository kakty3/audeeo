from feedgen.feed import FeedGenerator

from . import models


def generate_feed():
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
