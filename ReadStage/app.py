from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import Book, User, Recommend

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30
PASSWORD_MIN_LEN = 8

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

csrf = CSRFProtect(app)


# ルートページのリダイレクト処理
@app.route("/", methods=["GET"])
def index():
    #user_idがない場合、login.htmlへリダイレクト
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('books_view'))


# サインアップページの表示
@app.route("/signup", methods=["GET"])
def signup_view():
    #user_idがある場合、books.htmlへリダイレクト
    if session.get("user_id") is not None:
        return redirect(url_for('books_view'))
    return render_template('auth/signup.html')


# サインアップ処理
@app.route("/signup", methods=["POST"])
def signup_process():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    password_confirmation = request.form.get("password_confirmation", "")

    # 空チェック
    if not email or not password or not password_confirmation:
        flash("空のフォームがあります" , 'error')
        return redirect(url_for('signup_view'))

    # パスワード桁数チェック
    if len(password) < PASSWORD_MIN_LEN:
        flash(f"パスワードは{PASSWORD_MIN_LEN}文字以上で設定してください。" , 'error')
        return redirect(url_for('signup_view'))

    # パスワード一致チェック
    if password != password_confirmation:
        flash("二つのパスワードの値が違っています。", "error")
        return redirect(url_for('signup_view'))

    # メール形式チェック
    if re.match(EMAIL_PATTERN, email) is None:
        flash("正しいメールアドレスの形式ではありません。", "error")
        return redirect(url_for('signup_view'))

    # 既存ユーザーチェック
    registered_user = User.find_user_by_email(email)
    if registered_user is not None:
        flash("既に登録されているメールアドレスです。", "error")
        return redirect(url_for('signup_view'))

    #パスワードのハッシュ化
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # ユーザーを作成してuser_idを取得、セッションにセットする
    user_id = User.create(email, hashed_password)
    session["user_id"] = user_id

    return redirect(url_for('books_view'))


# ログインページの表示
@app.route("/login", methods = ["GET"])
def login_view():
    if session.get("user_id") is not None:
        return redirect(url_for('books_view'))
    return render_template('auth/login.html')


# ログイン処理
@app.route("/login", methods = ["POST"])
def login_process():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("メールアドレスorパスワードが空です。", "error")
    else:
        # メールアドレスからユーザー情報を取得
        user = User.find_user_by_email(email)
        if user is None:
            flash("メールアドレスもしくはパスワードが違います。", "error")
        else:
            # 入力されたパスワードをSHA256でハッシュ化、
            # この値とDBに保存していたパスワード値を比較して認証を行う
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if hashPassword != user["password"]:
                flash("メールアドレスもしくはパスワードが違います。", "error")
            else:
                session["user_id"] = user["id"]
                return redirect(url_for('books_view'))
    return redirect(url_for('login_view'))


# ログアウト処理
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_view'))


# トップページ(書籍一覧)の表示
@app.route("/books", methods=["GET"])
def books_view():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        # Bookモデルクラスに整形された書籍データのリストを渡す
        # ほしい情報(タイトル、カテゴリ、キーワード、まえがき)
        books = Book.get_all()
        return render_template('book/books.html', books=books)


# 評価詳細ページ表示
@app.route("/book/<int:book_id>", methods=["GET"])
def book_id_view(book_id):

    return render_template('book/book_detail.html')


# 書籍コメントページ表示
@app.route("/book/<int:book_id>/comment", methods=["GET"])
def book_comment_view(book_id):
    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(404)

    # 対象書籍に該当ユーザーがすでにコメント済みの場合は404エラーとする
    recommend = Recommend.get_recommend(user_id, book_id)
    if recommend is not None:
        abort(404)

    return render_template('book/create_comment.html', book=book)


# 書籍評価投稿処理
@app.route("/book/<int:book_id>/comment", methods=["POST"])
def create_comment(book_id):
    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(404)
    
    # 対象書籍に該当ユーザーがすでにコメント済みの場合は400エラーとする
    recommend = Recommend.get_recommend(user_id, book_id)
    if recommend is not None:
        abort(400)



# 188～207行目、create_comment.htmlのフラッシュメッセージ 仮作成（おにちゃん）
    # フォームデータの取得
    evaluation_raw = request.form.get("evaluation", "").strip()
    status = request.form.get("status", "").strip()
    message = request.form.get("message", "")

    # バリデーションチェック（未選択チェック）
    if evaluation_raw == "" or status == "":
        flash("「評価」と「学習者レベル」は必須入力です。", "error")
        # リダイレクトではなく、bookデータを渡して同じページを再表示
        return render_template('book/create_comment.html', book=book)
    
    # int型に変換
    evaluation = int(evaluation_raw)

    # 書籍評価情報を登録
    Recommend.create(user_id=user_id,
                     book_id=book_id,
                     evaluation=evaluation,
                     status=status,
                     message=message)
    


    # 書籍評価情報を登録
    evaluation = int(request.form.get("evaluation"))
    status = request.form.get("status")
    message = request.form.get("message")
    Recommend.create(user_id=user_id,
                     book_id=book_id,
                     evaluation=evaluation,
                     status=status,
                     message=message);

    # 詳細・コメントページにリダイレクト
    return redirect(url_for('book_id_view', book_id=book_id))


# 書籍検索


#書籍投稿削除


#書籍投稿修正

#エラーハンドラー404
@app.errorhandler(404)
def page_not_found(Error):
    return render_template('error/404.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
