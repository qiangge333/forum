from models.question import Question
from models.question import Answer
from routes import *


main = Blueprint('question', __name__)

Model = Question


xfrs_dict = {
    'd40a58205d884331aa7f2a7304ad6345': 0,
}


def random_string():
    import uuid
    return str(uuid.uuid4())


@main.route('/')
def index():
    ms = Model.query.all()
    u = current_user()
    return render_template('question/index.html', questions=ms, user=u)


@main.route('/user/<int:id>')
def user_index(id):
    u = current_user()
    ms = Model.query.filter_by(user_id=id).all()
    return render_template('question/user_index.html', questions=ms, user=u)


@main.route('/<int:id>')
def detail(id):
    m = Model.query.get(id)
    answers = m.answers
    u = current_user()
    return render_template('question/detail.html', question=m, answers=answers, user=u)


@main.route('/new')
@login_required
def new():
    u = current_user()
    return render_template('question/new.html', user=u)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.user_id = current_user().id
    m.save()
    return redirect(url_for('question.detail', id=m.id))


@main.route('/edit/<int:id>')
@login_required
def edit(id):
    m = Model.query.get(id)
    u = current_user()
    if m.user_id == u.id:
        return render_template('question/edit.html', question=m, user=u)
    else:
        return redirect(url_for('question.detail', id=id))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    Model.update(id, form)
    return redirect(url_for('question.detail', id=id))


@main.route('/answer', methods=['POST'])
@login_required
def answer():
    form = request.form
    a = Answer(form)
    a.user = current_user()
    a.save()
    return redirect(url_for('question.detail', id=a.question_id))
