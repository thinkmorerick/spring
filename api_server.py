from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify,flash
from utils.model import UserModel,QuestionModel,AnswerModel
from utils.exts import db
import config.db_config
from sqlalchemy import or_
import json
from werkzeug.contrib.cache import MemcachedCache
import logging
import logging
import logging.config
import memcache

app = Flask(__name__)
app.config.from_object(config.db_config)
db.init_app(app)
cache = MemcachedCache(['0.0.0.0:12000'])
logging.config.fileConfig("config/logger.conf")
logger = logging.getLogger("spring")

# 测试页
@app.route('/')
def index():
    app.logger.info('info log')
    app.logger.warning('warning log')
    flash('index successfully!')
    return render_template('index.html')

# MemcachedCache_demo
@app.route('/memcache/')
def index_memcache():
    cache.set("name", "python", timeout=5 * 60)
    value_ = cache.get('name')
    app.logger.info('info log')
    return 'memcache: %s' % value_

# json_demo
@app.route('/json/')
def index_json():
    data = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    # return jsonify(data)
    app.logger.info('info log')
    return json.dumps(data)

# mysql_demo
@app.route('/mysql/')
def index_mysql():
    # 查
    # select * from user where user.id='1';
    user_ = UserModel.query.filter(UserModel.telephone == '555').first()
    app.logger.info('info log')
    return 'username: %s' % user_.username

# add_data_mysql
@app.route('/add_data_mysql/')
def add_data_mysql():
    # 增加：
    user_ = UserModel(username='username555', telephone='555', password="222")
    db.session.add(user_)
    # 事务
    db.session.commit()
    app.logger.info('info log')
    return redirect('/')

# error_demo
@app.route('/error/')
def error_demo():
    app.logger.info('info log')
    result = 9/0
    return redirect('/')

# if __name__ == '__main__':
    # app.run(port=9000)
