from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for

from functools import wraps

from models.user import User


# 通过 session 来获取当前登录的用户
def current_user():
    uid = int(session.get('user_id', 0))
    u = User.query.get(uid)
    return u


# 套路, 直接复制即可, 这样就可以直接用了
# 这个参数 f 实际上就是路由函数
def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            # 用户未登录, 重定向到登录页面
            return redirect(url_for('user.index'))
        else:
            # 用户已经登录, 扔给路由函数处理
            return f(*args, **kwargs)
    return function
