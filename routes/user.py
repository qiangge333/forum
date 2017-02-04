from models.user import User
from routes import *

import os


main = Blueprint('user', __name__)

Model = User


xfrs_dict = {
    'd40a58205d884331aa7f2a7304ad6345': 0,
}


def random_string():
    import uuid
    return str(uuid.uuid4())


@main.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method
    if method == 'GET':
        return render_template('user/login_views.html')
    else:
        form = request.form
        username = form.get('username', '')
        # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
        model = Model.query.filter_by(username=username).first()
        if model is not None and model.validate_auth(form):
            print('登录成功')
            session['user_id'] = model.id
            return redirect(url_for('node.index', id=1))
        else:
            print('登录失败')
            # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
            return redirect(url_for('user.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    method = request.method
    if method == 'GET':
        return render_template('user/register_views.html')
    else:
        form = request.form
        m = Model(form)
        # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
        model = Model.query.filter_by(username=m.username).first()
        if model is None and m.valid():
            print('注册成功')
            m.save()
            session['user_id'] = m.id
            return redirect(url_for('node.index', id=1))
        else:
            print('注册失败')
            # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
            return redirect(url_for('user.register'))


@main.route('/profile')
@login_required
def profile():
    m = current_user()
    lt = len(m.topics)
    lc = len(m.comments)
    lq = len(m.questions)
    return render_template('user/user_profile.html', user=m, lt=lt, lc=lc, lq=lq)


@main.route('/profile/<int:id>')
@login_required
def user_profile(id):
    u = current_user()
    m = Model.query.get(id)
    lt = len(m.topics)
    lc = len(m.comments)
    lq = len(m.questions)
    return render_template('user/profile.html', owner_user=m, user=u, lt=lt, lc=lc, lq=lq)


def file_name(filename):
    count = len(os.listdir('uploads')) + 1
    name = str(count) + '.' + filename.split('.')[-1]
    print(name)
    return name
