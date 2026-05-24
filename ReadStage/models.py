from flask import abort
import pymysql
from util.DB import DB
#辞書（Dict）形式で取得したいため
import pymysql.cursors

# 初回起動時にコネクションプールインスタンスを取得
db_pool = DB.init_db_pool()

class Book:
  @classmethod
  def get_all(cls, search_dict):
    conn = db_pool.get_conn()
    try:
      # DictCursorを使って、結果を辞書形式で返す
      with conn.cursor(pymysql.cursors.DictCursor) as cur:
        # 1. 書籍の基本情報とキーワードを取得
          #キーワードがない書籍の未取得をさけるためにLEFT JOIN(外部結合)を使用
        sql_books = """
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
          LEFT JOIN book_keywords AS bk ON
            b.id = bk.book_id
          LEFT JOIN keywords AS k ON
            bk.keyword_id = k.id
        """

        # WHERE句が必要な場合は組み立て
        use_where = False
        params = []

        # 検索条件を指定している場合
        if search_dict is not None:
          # カテゴリ・キーワード検索
          if "word" in search_dict:
            search_category_keyword = search_dict["word"]
            if search_category_keyword:
              sql_books += " WHERE (c.category LIKE %s OR k.keyword LIKE %s)"
              params.append("%" + search_category_keyword + "%")
              params.append("%" + search_category_keyword + "%")
              use_where = True
          
          # 学習レベル検索（※評価は固定で4以上）
          if "status" in search_dict:
            search_status = search_dict["status"]
            if search_status:
              if use_where:
                # すでにWHERE句を追加済みなので、ANDから始める
                sql_books += " AND "
              else:
                # WHERE句の指定がないので、WHERE句から始める
                sql_books += " WHERE "
              # サブクエリで指定学習レベルが4以上のものに絞り込む
              sql_books += """
              b.id IN (SELECT book_id FROM recommends 
                       WHERE status=%s AND delete_flag=0 
                       GROUP BY book_id HAVING AVG(evaluation) >= 4)
              """
              params.append(search_status)
              use_where = True

        # 最後に並び順を追加
        sql_books += "ORDER BY b.id ASC;"

        cur.execute(sql_books, params)
        #辞書のリストとして取得
        rows = cur.fetchall()
        #1つのbook_idに対して複数のキーワードがあるため、辞書リストを整理する
        books_data = {}
        for row in rows:
            book_id = row['id']
            if book_id not in books_data:
                # 初めてのbook_idの場合、新しいエントリを作成
                books_data[book_id] = {
                    'id': row['id'],
                    'title': row['title'],
                    'category': row['category'], # categoryは1つと仮定
                    'introduction': row['introduction'],
                    'keywords': [] # キーワードはリストとして保持
                }
            # 該当書籍のキーワードリストに現在のキーワードを追加
            books_data[book_id]['keywords'].append(row['keyword'])
        #辞書の値をリストの中に入れて返す
        # final_books_list = [ {書籍1の辞書}, {書籍2の辞書}, ... ]
        #例：書籍1の辞書{'id': 1, 'title': 'Python入門', 'category': 'プログラミング', ...}
        #例：[{id:1, title:*, category:*, introduction:*, keywords:[*,*,*]}]
        final_books_list = list(books_data.values())
        
        # 2. すべての書籍の平均評価点を取得
        sql_evaluations = """
          SELECT
            book_id,
            status,
            ROUND(AVG(evaluation), 1) AS average_evaluation
          FROM recommends
          WHERE delete_flag=0
          GROUP BY
            book_id, status;
        """
        cur.execute(sql_evaluations)
        average_evaluations_list = cur.fetchall()

        # 3. 取得した平均評価点をbook_idごとにデータを辞書型で整理
        evaluations_by_book_id = {}
        for eval_item in average_evaluations_list:
            book_id = eval_item['book_id']
            status = eval_item['status']
            avg_eval = eval_item['average_evaluation']

            if book_id not in evaluations_by_book_id:
            # 初めてのbook_idの場合、新しいエントリを作成
              evaluations_by_book_id[book_id] = {}
            #2重の辞書型のデータ{1: {'START/入門': 3.5, 'BASIC/基礎': 3.5}, ...}
            evaluations_by_book_id[book_id][status] = avg_eval

        # final_books_list = [{辞書1の書籍},{辞書2の書籍}]の中に平均評価点をGETメソッドで格納
        for book in final_books_list:
            book_id = book['id']
            # 平均評価点を追加、または該当する評価がなければ空の辞書をセット
            book['average_evaluations'] = evaluations_by_book_id.get(book_id, {})
            #final_books_listの中身はbook_idごとの辞書型で整理
            #[{id:1, title:書籍名, category:カテゴリ名, introduction:まえがき, keywords:[*,*,*],
            # 'average_evaluations': {'START/入門': 3.5, 'BASIC/基礎': 3.5, ...}}]
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
        sql = 'SELECT id FROM recommends WHERE user_id=%s AND book_id=%s AND delete_flag=0;'
        cur.execute(sql, (user_id, book_id))
        recommend = cur.fetchone()
        return recommend
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

  @classmethod
  def get_book_recommends(cls, user_id, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = '''
        SELECT id, user_id, (user_id=%s) AS is_current_user, evaluation, status, message, created_at 
        FROM recommends WHERE book_id=%s AND delete_flag=0 
        ORDER BY created_at DESC;
        '''
        cur.execute(sql, (user_id, book_id))
        recommends = cur.fetchall()
        return recommends
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

  @classmethod
  def get_edit_recommend(cls, recommend_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = '''
        SELECT id, user_id, evaluation, status, message, updated_at 
        FROM recommends WHERE id=%s AND delete_flag=0;
        '''
        cur.execute(sql, (recommend_id,))
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

  @classmethod
  def delete(cls, recommend_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = "UPDATE recommends SET delete_flag = 1, deleted_at = NOW() WHERE id = %s;"
        cur.execute(sql, (recommend_id, ))
        conn.commit()
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)

  @classmethod
  def edit(cls, recommend_id, evaluation, status, message):
    conn = db_pool.get_conn()
    try:
      with conn.cursor() as cur:
        sql = 'UPDATE recommends SET evaluation=%s, status=%s, message=%s WHERE id=%s;'
        cur.execute(sql, (evaluation, status, message, recommend_id ))
        conn.commit()
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)


class Category:
  @classmethod
  def get_category(cls, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor(pymysql.cursors.DictCursor) as cur:
        sql = '''
        SELECT c.category FROM categories AS c 
        INNER JOIN book_categories AS bc ON bc.category_id = c.id
        WHERE bc.book_id=%s;
        '''
        cur.execute(sql, (book_id, ))
        category = cur.fetchone()
        return category
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)
      
class Keyword:
  @classmethod
  def get_keywords(cls, book_id):
    conn = db_pool.get_conn()
    try:
      with conn.cursor(pymysql.cursors.DictCursor) as cur:
        sql = '''
        SELECT k.keyword FROM keywords AS k 
        INNER JOIN book_keywords AS bk ON bk.keyword_id = k.id
        WHERE bk.book_id=%s;
        '''
        cur.execute(sql, (book_id, ))
        keywords = cur.fetchall()
        return keywords
    except pymysql.Error as e:
      print(f'エラーが発生しています：{e}')
      abort(500)
    finally:
      db_pool.release(conn)