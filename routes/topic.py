from models.node import Node
from models.topic import Topic
from models.topic import Comment
from routes import *


main = Blueprint('topic', __name__)

Model = Topic


xfrs_dict = {
    'd40a58205d884331aa7f2a7304ad6345': 0,
}


def random_string():
    import uuid
    return str(uuid.uuid4())


@main.route('/<int:id>')
def detail(id):
    m = Model.query.get(id)
    cs = m.comments
    u = current_user()
    return render_template('topic/detail.html', topic=m, comments=cs, user=u)


@main.route('/new/<int:id>')
@login_required
def new(id):
    u = current_user()
    return render_template('topic/new.html', id=id, user=u)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.user_id = current_user().id
    m.save()
    return redirect(url_for('topic.detail', id=m.id))


@main.route('/edit/<int:id>')
def edit(id):
    m = Model.query.get(id)
    u = current_user()
    if m.user_id == u.id:
        return render_template('topic/edit.html', topic=m, user=u)
    else:
        return redirect(url_for('topic.detail', id=id))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    Model.update(id, form)
    return redirect(url_for('topic.detail', id=id))


@main.route('/answer', methods=['POST'])
@login_required
def comments():
    form = request.form
    c = Comment(form)
    c.user_id = current_user().id
    c.save()
    return redirect(url_for('topic.detail', id=c.topic_id))
