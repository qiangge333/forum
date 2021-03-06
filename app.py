from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.node import Node
from models.user import User
from models.question import Question
from models.question import Answer
from models.topic import Topic
from models.topic import Comment


app = Flask(__name__)
manager = Manager(app)


def configured_app():
    # 这一句是套路, 不加会有 warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 设置上传文件的最大尺寸为 2M
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    # 如果你上传过大的文件, flask 会生成一个 413 响应
    # 413 Request Entity Too Large（请求实体太大）
    # secret key 和 数据库配置都放在 config.py 里面
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    # 初始化 db
    db.init_app(app)
    # 注册路由
    register_routes(app)
    # 配置日志
    configure_log(app)
    # 返回配置好的 app 实例
    return app


def configure_log(app):
    # 设置 log, 否则输出会被 gunicorn 吃掉
    # 但是如果 app 是 debug 模式的话, 则不用这么搞
    if not app.debug:
        import logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def register_routes(app):
    """
    在这个函数里面 import 并注册蓝图
    """
    from routes.user import main as routes_user
    app.register_blueprint(routes_user, url_prefix='/user')

    from routes.question import main as routes_question
    app.register_blueprint(routes_question, url_prefix='/question')

    from routes.node import main as routes_node
    app.register_blueprint(routes_node, url_prefix='/board')

    from routes.topic import main as routes_topic
    app.register_blueprint(routes_topic, url_prefix='/topic')

    from routes.upload import main as routes_upload
    app.register_blueprint(routes_upload, url_prefix='/uploads')


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    """
    用原始的方法启动程序
    """
    app = configured_app()
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_manager()
    configured_app()
    manager.run()
