from . import utctime
from . import ReprMixin
from . import db


class Question(db.Model, ReprMixin):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    solved = db.Column(db.Boolean(), default=False)
    created_time = db.Column(db.Integer, default=utctime())
    updated_time = db.Column(db.Integer, default=utctime())
    views = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean(), default=False)

    title = db.Column(db.Text())
    expectation = db.Column(db.Text())
    thinking = db.Column(db.Text())
    procedure = db.Column(db.Text())
    problems = db.Column(db.Text())
    code = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='question')

    def __init__(self, form):
        print('question init', form)
        self.title = form.get('title', '')
        self.expectation = form.get('expectation', '')
        self.thinking = form.get('thinking', '')
        self.procedure = form.get('procedure', '')
        self.problems = form.get('problems', '')
        self.code = form.get('code', '')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.is_hidden = True
        self.save()

    def _update(self, form):
        for key in form:
            if key in self.__dict__:
                updated_value = form.get(key, '')
                if updated_value != '':
                    setattr(self, key, updated_value)
        print('question update', form)
        self.updated_time = utctime()
        self.save()


class Answer(db.Model, ReprMixin):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=utctime())
    updated_time = db.Column(db.Integer, default=utctime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, form):
        print('answer init', form)
        self.content = form.get('content', '')
        self.question_id = form.get('question_id', '')
        # question = Question.query.get(self.question_id)
        # question.updated_time = utctime()

    def _update(self, form):
        print('answer update', form)
        self.content = form.get('content', '')
        self.updated_time = utctime()
        self.question.updated_time = utctime()
        self.save()
