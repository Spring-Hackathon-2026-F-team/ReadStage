from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os
import unicodedata

from models import Book, User, Recommend, Category, Keyword

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30
PASSWORD_MIN_LEN = 8

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

csrf = CSRFProtect(app)


# ゲストページのリダイレクト処理
@app.route("/", methods=["GET"])
def guest_view():
    # ゲストページは未ログイン状態でアクセス可能。
    # 書籍を3冊限定で取得する
    books = Book.get_all(None)
    books_top3 = books[:3]
    return render_template('book/guest.html', books=books_top3)


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
 
    # URLクエリから検索情報を取得
    search_word = request.args.get("search_word", "")
    search_status = request.args.get("search_status", "")
    if search_word or search_status:
        # 検索ボタンからのリダイレクト時
        # 英数字は半角、カタカナは全角文字に変換して検索する
        word = unicodedata.normalize('NFKC', search_word)
        search_dict = { "word": word, "status": search_status }
        books = Book.get_all(search_dict)
    else:
        # 検索情報未設定時は検索未設定
        # Bookモデルクラスに整形された書籍データのリストを渡す
        # タイトル、カテゴリ、キーワード、まえがきを渡す
        # book_idごとの4つのレベルの評価点を渡す
        books = Book.get_all(None)
    return render_template('book/books.html', books=books, search_word=search_word, selected_status=search_status)

# 評価詳細ページ表示
@app.route("/book/<int:book_id>", methods=["GET"])
def book_id_view(book_id):
    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(400)
    
    # カテゴリ・キーワード・コメント一覧取得
    category = Category.get_category(book_id)
    keywords = Keyword.get_keywords(book_id)
    recommends = Recommend.get_book_recommends(user_id, book_id)

    # 書籍評価へボタン表示条件
    my_comment = Recommend.get_recommend(user_id, book_id)
    is_already_comment = False if my_comment else True

    return render_template('book/book_detail.html',
                           book=book,
                           category=category,
                           keywords=keywords,
                           recommends=recommends,
                           is_already_comment=is_already_comment)


# 書籍コメント投稿・編集ページ表示
@app.route("/book/<int:book_id>/comment", methods=["GET"])
@app.route("/book/<int:book_id>/comment/<int:recommend_id>/edit", methods=["GET"])
def book_comment_view(book_id, recommend_id=None):
    # レコメンドIDがあれば書籍評価編集判定
    is_edit = recommend_id is not None

    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(404)

    recommend = None
    if is_edit:
        # 編集時はレコメンドIDが一致しているかチェック
        recommend = Recommend.get_edit_recommend(recommend_id)
        if recommend['id'] != recommend_id:
            abort(404)
    else:
        # 新規投稿時
        # 対象書籍に該当ユーザーがすでにコメント済みの場合は404エラーとする
        recommend = Recommend.get_recommend(user_id, book_id)
        if recommend is not None:
            abort(404)

    return render_template('book/create_comment.html',  is_edit=is_edit, book=book, recommend=recommend)


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
        return render_template('book/create_comment.html',
                               is_edit=False,
                               book=book,
                               recommend=None,
                               form_data={
                                   "evaluation": evaluation_raw,
                                   "status": status,
                                   "message": message,
                               })
    
    # int型に変換
    evaluation = int(evaluation_raw)

    # 書籍評価情報を登録
    Recommend.create(user_id=user_id,
                     book_id=book_id,
                     evaluation=evaluation,
                     status=status,
                     message=message)

    # 評価詳細ページにリダイレクト
    return redirect(url_for('book_id_view', book_id=book_id))


# 書籍検索
@app.route('/books/search', methods=["POST"])
def search_books():
    # セッションチェック
    # 検索はTOPページからしか許容市内想定なので、未ログインの場合はログインに戻す
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 検索条件を取得して、書籍一覧にリダイレクト
    search_word = request.form.get("search-word")
    search_status = request.form.get("search-status")
    return redirect(url_for("books_view", search_word=search_word, search_status=search_status))


#書籍投稿削除
@app.route("/book/<int:book_id>/comment/<int:recommend_id>/delete", methods=["POST"])
def delete_comment(book_id, recommend_id):
    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(404)
    
    # コメント存在チェック
    recommend = Recommend.get_recommend(user_id, book_id)
    if recommend is None:
        abort(404)

    # 書籍評価情報にdelete_flagを設定
    Recommend.delete(recommend_id);

    # 詳細・コメントページにリダイレクト
    return redirect(url_for('book_id_view', book_id=book_id))


#書籍投稿修正
@app.route("/book/<int:book_id>/comment/<int:recommend_id>/edit", methods=["POST"])
def edit_comment(book_id, recommend_id):
    # セッションチェック
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for('login_view'))

    # 書籍存在チェック
    book = Book.get_book(book_id)
    if book is None:
        abort(404)
    
    # レコメンドIDが一致しているかチェック
    recommend = Recommend.get_edit_recommend(recommend_id)
    if recommend['id'] != recommend_id:
        abort(404)

    # バリデーションチェック（未選択チェック）
    evaluation = int(request.form.get("evaluation"))
    status = request.form.get("status")
    message = request.form.get("message")

    # イレギュラーケース：編集時は評価・学習者レベルともに未選択状態にできないはず
    if evaluation == "" or status == "":
        flash("「評価」と「学習者レベル」は必須入力です。", "error")
        return render_template('book/create_comment.html',
                               is_edit=False,
                               book=book,
                               recommend=None,
                               form_data={
                                   "evaluation": evaluation,
                                   "status": status,
                                   "message": message,
                               })

    # 書籍評価情報を登録
    Recommend.edit(recommend_id=recommend_id,
                   evaluation=evaluation,
                   status=status,
                   message=message);

    # 詳細・コメントページにリダイレクト
    return redirect(url_for('book_id_view', book_id=book_id))

#エラーハンドラー404
@app.errorhandler(404)
def page_not_found(Error):
    return render_template('error/404.html'), 404

#エラーハンドラー400
@app.errorhandler(400)
def bad_request(Error):
    return render_template('error/400.html'), 400

#意図的に４００エラーを発生させるルートを作る
@app.route('/books/400')
def trigger_400():
    abort(400) #ここで４００エラーを発生させる

#エラーハンドラー500
@app.errorhandler(500)
def internal_serber_error(Error):
    return render_template('error/500.html'), 500

# 意図的に５００エラーを発生させるルートを作る
@app.route('/books/500')
def trigger_500(): #ここで５００エラーを発生させる
    abort(500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)