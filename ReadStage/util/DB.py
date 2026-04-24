import os
import pymysql
from pymysqlpool.pool import Pool

class DB:
  @classmethod
  def init_db_pool(cls):
    pool = Pool(
      # DB接続情報をENVファイルから取得
      host=os.getenv('DB_HOST'),
      user=os.getenv('DB_USER'),
      password=os.getenv('DB_PASSWORD'),
      database=os.getenv('DB_DATABASE'),
      # 最大接続数
      max_size=5,
      charset='utf8mb4',
      cursorclass=pymysql.cursors.DictCursor,
      autocommit=True
    )

    # コネクションプール初期化し、poolインスタンスを返す。
    # get_conn()、release()はmodels側でそれぞれ行う。
    pool.init()
    return pool
