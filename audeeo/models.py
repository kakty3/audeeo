from email.utils import formatdate
from hashlib import md5
from uuid import uuid4

from feedgen.feed import FeedGenerator
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, event, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now as sql_now

from audeeo.database import db


feed_episode_table = Table('feeds_episodes', db.Model.metadata,
    Column('feed_id', Integer, ForeignKey('feed.id')),
    Column('episode_id', Integer, ForeignKey('episode.id'))
)

class Episode(db.Model):
    __tablename__ = 'episode'

    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    url = Column(String(), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql_now())
    pub_date = Column(DateTime(timezone=True), server_default=sql_now())
    file_size = Column(Integer, server_default=text('0'))

    def __repr__(self):
        return '<Title {}, url {}>'.format(self.title, self.url)

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    feeds = relationship('Feed', backref='owner', lazy='dynamic')

@event.listens_for(User, 'init')
def receive_init(target, args, kwargs):
    feed = Feed(title='Feed',
                owner_id=target.id,
                ia_identifier=str(uuid4()),
                description=f'My default feed')
    target.feeds.append(feed)

class Feed(db.Model):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    episodes = relationship('Episode', secondary=feed_episode_table, lazy='dynamic')
    ia_identifier = Column(String(50), nullable=False)

    def get_rss(self, pretty=False):
        """Generate podcast RSS feed
        Spec: iTunes Podcast RSS: https://github.com/simplepie/simplepie-ng/wiki/Spec:-iTunes-Podcast-RSS

        :return: Contents of podcast RSS feed
        :rtype: bytes
        """

        fg = FeedGenerator()
        fg.load_extension('podcast')

        fg.title(self.title)
        fg.description(self.description)
        link = 'https://example.com'
        fg.link(href=link, rel='self')
        fg.image(url=self.artwork(), title=self.title, link=link)
        author = self.owner.username or 'Unknown'
        fg.podcast.itunes_author(author)
        fg.podcast.itunes_owner(author, self.owner.email)

        for episode in self.episodes:
            fe = fg.add_entry()
            fe.id(episode.url)
            fe.title(episode.title)
            fe.enclosure(episode.url, str(episode.file_size), 'audio/mpeg')
            fe.pubDate(formatdate(episode.created_at.timestamp()))

        return fg.rss_str(pretty=pretty)

    def artwork(self, size=128):
        digest = md5(self.title.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
