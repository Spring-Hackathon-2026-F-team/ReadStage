from flask import abort
import pymysql
from util.DB import DB
#辞書（Dict）形式で取得したいため
import pymysql.cursors

# 初回起動時にコネクションプールインスタンスを取得
db_pool = DB.init_db_pool()

class Book:
  @classmethod
  def get_all(cls):
    conn = db_pool.get_conn()
    try:
      # DictCursorを使って、結果を辞書形式で返す
      with conn.cursor(pymysql.cursors.DictCursor) as cur:
#        書籍一覧、詳細・コメントページに必要な書籍データを取得
        sql = """
          SELECT
            b.id,
            b.title,
            c.category,
            k.keyword,
            b.introduction
          FROM books AS b
          JOIN book_categories AS bc ON
            b.id = bc.book_id
          JOIN categories AS c ON
            bc.category_id = c.id
          JOIN book_keywords AS bk ON
            b.id = bk.book_id
          JOIN keywords AS k ON
            bk.keyword_id = k.id
          ORDER BY
            b.id ASC;
        """
        cur.execute(sql)
        #辞書のリストとして取得
        rows = cur.fetchall()
        #1つのbook_idに対して複数のキーワードがあるため、辞書リストを整理する
        books_data = {}
        for row in rows:
            book_id = row['id']
            if book_id not in books_data:
                # 初めての書籍IDの場合、新しいエントリを作成
                books_data[book_id] = {
                    'id': row['id'],
                    'title': row['title'],
                    'category': row['category'], # categoryは1つと仮定
                    'introduction': row['introduction'],
                    'keywords': [] # キーワードはリストとして保持
                }
            # 該当書籍のキーワードリストに現在のキーワードを追加
            books_data[book_id]['keywords'].append(row['keyword'])

        # 辞書の値をリストに変換して返す
        # [{id:1, title:*, category:*, introduction:*, keywords:[*,*,*]}]
        final_books_list = list(books_data.values())
      return final_books_list
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

  @classmethod
  def get_book(cls, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'SELECT id, title FROM books WHERE id=%s;'
        cur.execute(sql, (book_id,))
        book = cur.fetchone()
      return book
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

class Recommend:
  @classmethod
  def get_recommend(cls, user_id, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'SELECT id FROM recommends WHERE user_id=%s AND book_id=%s;'
        cur.execute(sql, (user_id, book_id))
        recommend = cur.fetchone()
        return recommend
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)


  @classmethod
  def get_book_recommend(cls, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'SELECT id, ... FROM recommends WHERE book_id=%s;'
        cur.execute(sql, (book_id, ))
        recommend = cur.fetchone()
        return recommend
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

  @classmethod
  def create(cls, user_id, book_id, evaluation, status, message):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = '''
          INSERT INTO recommends (user_id, book_id, evaluation, status, message) 
          VALUES (%s, %s, %s, %s, %s);
          '''
        cur.execute(sql, (user_id, book_id, evaluation, status, message))
        conn.commit()
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

class Category:
  pass;