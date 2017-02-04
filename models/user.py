import os

from . import ReprMixin
from . import db
from . import utctime


class User(db.Model, ReprMixin):
    # 类的属性就是数据库表的字段
    # 这些都是内置的 __tablename__ 是表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text())
    password = db.Column(db.Text())
    img = db.Column(db.Text(), default='/uploads/default.png')
    # qq = db.Column(db.Text())
    # email = db.Column(db.Text())
    # signature = db.Column(db.Text())

    credit = db.Column(db.Integer, default=100)
    created_time = db.Column(db.Integer)
    # 
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    questions = db.relationship('Question', backref='user')
    answers = db.relationship('Answer', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = utctime()
        # self.email = form.get('email', '')
        # self.signature = form.get('signature', '')
        # self.qq = form.get('qq', '')

    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        return username_equals and password_equals

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def _update(self, form):
        print('user.update, ', form)
        self.password = form.get('password', self.password)


def test():
    form = {
        'username': 'gua1',
        'password': '123',
    }
    User.new(form)


if __name__ == '__main__':
    test()
