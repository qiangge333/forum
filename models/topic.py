from . import ReprMixin
from . import db
from . import utctime


class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=utctime())
    updated_time = db.Column(db.Integer, default=utctime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __init__(self, form):
        print('comment init', form)
        self.content = form.get('content', '')
        self.topic_id = form.get('topic_id', '')


class Topic(db.Model, ReprMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=utctime())
    updated_time = db.Column(db.Integer, default=utctime())
    views = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Integer, default=0)

    comments = db.relationship('Comment', backref='topic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        print('topic init', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.board_id = form.get('board_id', 0)

    def _update(self, form):
        print('topic update', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = utctime()
        self.save()
