# coding=utf8
import mysql.connector
import configparser as cfp  #导入 configparser包
import logging.config
import sys

logging.config.fileConfig(sys.path[1] + "/config/logging.conf")
logger = logging.getLogger("main")

conf = cfp.ConfigParser()  #创建一个 管理对象。
conf.read('/config/.prodConfig')  #把 文件导入管理对象中，把文件内容load到内存中
mysql_section = conf['mysql']
host = mysql_section['host']
user = mysql_section['user']
password = mysql_section['password']
port = mysql_section['port']
database = mysql_section['database']
charset = mysql_section['charset']

config = {'host': host,
          'user': user,
          'password': password,
          'port': port,
          'database': database,
          'charset': charset
          }


def get_db_connection():
    db = mysql.connector.connect(**config)
    return db


def close_db(cursor, db):
    if cursor is not None and db is not None:
        cursor.close()
        db.close()


def get_result_by_sql(sql):
    db = None
    cursor = None
    results = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        logger.exception("message")
    finally:
        close_db(cursor, db)
        return results


def update_by_sql(sql):
    db = None
    cursor = None
    results = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        logger.exception("message")
        db.rollback()
    finally:
        close_db(cursor, db)
        return results


if __name__ == '__main__':
    sql = 'select * from sp_user where id=85937'
    results = get_result_by_sql(sql)
    print(results)