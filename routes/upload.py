from models.user import User
from routes import *

import os
import flask


main = Blueprint('uploads', __name__)

Model = User


def file_name(filename):
    count = len(os.listdir('uploads')) + 1
    name = str(count) + '.' + filename.split('.')[-1]
    print(name)
    return name


@main.route('/add', methods=['POST'])
@login_required
def add():
    # 通过 request.files 访问上传的文件
    # uploaded 是上传时候的文件名
    f = request.files.get('uploaded')
    print(request)
    print('upload, ', request.files)
    if f:
        filename = f.filename
        ext = filename.split('.')[-1]
        valid_filetypes = ('png', 'jpg', 'jpeg', 'gif', 'apng')
        if ext in valid_filetypes:
            filename = file_name(filename)
            print('filename, ', filename)
            path = 'uploads/' + filename
            print(path)
            print(os.getcwd())
            f.save(path)
            u = current_user()
            u.img = '/' + path
            u.save()
            return redirect(url_for('user.profile'))
        else:
            return '<h1>文件类型或大小不对</h1>'
    else:
        return '<h1>没有上传</h1>'


@main.route('/<filename>')
def read(filename):
    # 用这个函数直接返回文件的响应
    return flask.send_from_directory('uploads/', filename)
