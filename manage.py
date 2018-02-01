from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api_server import app
from utils.exts import db
from utils.model import UserModel,QuestionModel,AnswerModel

#创建命令管理器
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app,db)

# 添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()