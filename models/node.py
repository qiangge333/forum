from . import db
from . import ReprMixin


class Node(db.Model, ReprMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    content = db.Column(db.Text())
    keywords = db.Column(db.Text())
    permit = db.Column(db.Text())
    master = db.Column(db.Text())
    parent_id = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', backref='board')

    def __init__(self, form):
        self.name = form.get('name', '')
        self.content = form.get("content", '')
        self.keywords = form.get("keywords", '板块')
        self.master = form.get('master', '')
        self.permit = form.get("permit", '')

    def _update(self, form):
        print('board.update, ', form)
