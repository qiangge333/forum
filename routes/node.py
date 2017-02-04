from models.node import Node
from routes import *


main = Blueprint('node', __name__)

Model = Node


xfrs_dict = {
    'd40a58205d884331aa7f2a7304ad6345': 0,
}


def random_string():
    import uuid
    return str(uuid.uuid4())


@main.route('/<int:id>')
def index(id):
    u = current_user()
    m = Model.query.get(id)
    ts = m.topics
    return render_template('topic/index.html', topics=ts, node=m, user=u)


@main.route('/new')
@login_required
def new():
    u = current_user()
    if u.id == 1:
        return render_template('node/new.html')
    else:
        redirect(url_for('user.index'))


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    Model.new(form)
    name = form.get('name')
    m = Model.query.filter_by(name=name).first()
    return redirect(url_for('node.index', id=m.id))
