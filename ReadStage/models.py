from flask import abort
import pymysql
from util.DB import DB

# 初回起動時にコネクションプールインスタンスを取得
db_pool = DB.init_db_pool()

class Book:
  @classmethod
  def get_all(cls):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'SELECT * FROM books ORDER BY id DESC;'
        cur.execute(sql)
        books = cur.fetchall()
      return books
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

class User:
  # メールアドレスに合致するユーザーIDとパスワードのみを返却
  @classmethod
  def find_user_by_email(cls, email):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'SELECT id, password FROM users WHERE email=%s;'
        cur.execute(sql, (email,))
        user = cur.fetchone()
      return user
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)
    
  # DB登録後ユーザーIDを返却
  @classmethod
  def create(cls, email, hashed_password):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'INSERT INTO users (email, password) VALUES (%s, %s);'
        cur.execute(sql, (email, hashed_password))
        conn.commit()

      # insertしたユーザーIDを取得
      # user_idがautoincrementなのでcur.lastrowidでも良いが、
      # UUIDに変更した時のために再取得して返却する
      user = cls.find_user_by_email(email)
      if user is not None:
        return user['id']

      # insertしたデータのユーザーが取れない（＝イレギュラーケース）は500エラーに流す
      raise
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)
