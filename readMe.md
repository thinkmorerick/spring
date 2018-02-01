1. run.py 工程的入口
2. mannage.py 迁移数据库入口  
* python3 manage.py db init  
* python3 manage.py db migrate
* python3 manage.py db upgrade
3. api_server.py 接口服务器  
4. requirements.txt 虚拟环境依赖  
* pip install -r requirements.txt  
5. utils/exts.py 连接数据库模块  
6. utils/model.py 实体模型类  
7. test/ 测试类文件夹 -> 参见test_command.md
8. templates 前端视图
9. static 静态文件
10. sql 存放sql文件夹
11. migrations 迁移数据库文件(系统自动生成)
12. log 日志文件夹
13. constant/ResultEnum.py 常量等存放文件夹/返回值枚举类
14. config/db_config.py 数据库配置文件
15. config/logger.conf 日志配置文件
16. requirements_dev.txt 比requirements.txt多的是单元测试依赖库  
17. scripts/ 项目用到的各种脚本
18. docs/ 项目文档
19. wiki/ wiki文档
20. extras/ 扩展，不属于项目必需的部分，但是与项目相关的sample、poc等，下面给出4个  
* 例子：  
        dev_example/  
        production_example/  
        test1_poc/  
        test2_poc/  
21. .gitignore git忽略文件
22. author.md 作者
