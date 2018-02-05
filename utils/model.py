from utils.exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid

'''定义模型，建立关系'''
# Model_demo
# class UserModel(db.Model):
#     # 定义表名
#     __tablename__ = 'user'
#     # 定义列对象
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(100),nullable=False)
#     telephone = db.Column(db.String(11),nullable=False)
#     password = db.Column(db.String(100),nullable=False)
#
#     # 密码加密
#     def __init__(self,*args,**kwargs):
#         telephone = kwargs.get('telephone')
#         username = kwargs.get('username')
#         password = kwargs.get('password')
#
#         self.telephone = telephone
#         self.username = username
#         self.password = generate_password_hash(password)
#
#     # 解密
#     def check_password(self,raw_password):
#         result = check_password_hash(self.password,raw_password)
#         return result
#
# class QuestionModel(db.Model):
#     __tablename__ = 'question'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     # now()获取的是服务器第一次运行的时间
#     # now就是每次创建一个模型的时候，都获取当前的时间
#     # 添加外键关系
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     #添加反转关系
#     author = db.relationship('UserModel', backref=db.backref('questions'))
#
# class AnswerModel(db.Model):
#     __tablename__ = 'answer'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     # 排序
#     question = db.relationship('QuestionModel', backref=db.backref('answers', order_by=id.desc()))
#     author = db.relationship('UserModel', backref=db.backref('answers'))