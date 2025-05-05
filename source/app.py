# app.py
# -*- coding: utf-8 -*-

import os # secret_key やパスワードを環境変数から読み込むため
from functools import wraps # デコレータ作成のため
from flask import Flask, render_template, request, redirect, url_for, session, flash # session, flash を追加
from markupsafe import Markup, escape # HTMLエスケープと安全なマークアップのため
from pygments import highlight
from pygments.lexers import get_lexer_by_name # 指定された言語のLexerを取得
from pygments.formatters import HtmlFormatter # HTML形式で出力
from pygments.util import ClassNotFound     # 指定された言語が見つからない場合のエラー

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# --- セッションとパスワードの設定 ---
# 重要: このキーは絶対に秘密にし、複雑なランダム文字列にしてください。
# 環境変数 FLASK_SECRET_KEY が設定されていなければ、'...' の部分が使われます。
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-very-secret-and-random-key-change-me')
# 掲示板アクセス用のパスワード
# 環境変数 BBS_PASSWORD が設定されていなければ、'password' が使われます。
BBS_PASSWORD = os.environ.get('BBS_PASSWORD', 'password') # 'password' を安全なパスワードに変更

# 投稿データを一時的に保存するためのリスト (インメモリ)
posts = []
# 投稿に一意のIDを割り振るためのカウンター
post_id_counter = 0

# --- nl2br カスタムフィルタ ---
def nl2br(value):
    """改行文字を<br>タグに変換するカスタムフィルタ"""
    if value:
        escaped_value = escape(value)
        formatted_value = escaped_value.replace('\r\n', '<br>\n').replace('\r', '<br>\n').replace('\n', '<br>\n')
        return Markup(formatted_value)
    return ""
# Jinja2 環境にカスタムフィルタを登録
app.jinja_env.filters['nl2br'] = nl2br

# --- Pygments Formatter (ハイライト済みHTML生成用) ---
# 行番号を表示(linenos), ラッパーdivにクラス名を指定(cssclass), カラースキームを指定(style)
pygments_formatter = HtmlFormatter(linenos=True, cssclass="codehilite", style='default')


# --- ログイン必須をチェックするデコレータ ---
def login_required(f):
    """アクセス時にログイン状態をチェックし、未ログインならログインページへリダイレクトするデコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('この操作を行うにはログインが必要です。', 'warning')
            # redirect 先として元のURLを next パラメータで渡す (ログイン後に戻れるように)
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# --- ルート定義 ---

# 掲示板トップページ (閲覧はログイン不要)
@app.route('/')
# @login_required # デコレータを削除したので誰でもアクセス可能
def index():
    """投稿一覧を表示する"""
    # Pygments CSS が外部ファイルの場合はここで渡す必要なし
    return render_template('index.html', posts=reversed(posts))

# 投稿処理 (書き込みはログイン必須)
@app.route('/post', methods=['POST'])
@login_required # ログイン必須デコレータを適用
def post():
    """新しい投稿を受け付ける"""
    global post_id_counter
    username = request.form.get('username', '名無しさん')
    message = request.form.get('message')
    code_snippet = request.form.get('code_snippet')
    language = request.form.get('language', 'text')
    highlighted_code = None

    # コードスニペットがあればハイライト処理
    if code_snippet:
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except ClassNotFound:
            lexer = get_lexer_by_name('text', stripall=True) # 不明な言語は text 扱い
        # highlight 関数で HTML を生成
        highlighted_code = highlight(code_snippet, lexer, pygments_formatter)

    # メッセージまたはコードがあれば投稿を追加
    if message or code_snippet:
        post_id_counter += 1
        posts.append({
            'id': post_id_counter,
            'username': username if username else '名無しさん',
            'message': message,
            'highlighted_code': highlighted_code
        })

    # 投稿後はトップページにリダイレクト
    return redirect(url_for('index'))

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン処理を行う"""
    # すでにログイン済みならトップページへリダイレクト
    if session.get('logged_in'):
        return redirect(url_for('index'))

    # POSTリクエスト（フォームが送信された）の場合
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        # 設定したパスワードと一致するか検証
        if password_attempt == BBS_PASSWORD:
            # 一致したらセッションにログイン済みフラグを立てる
            session['logged_in'] = True
            flash('ログインしました。', 'success')
            # next パラメータがあればそこへ、なければトップページへ
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))
        else:
            # パスワードが間違っていたらエラーメッセージを表示
            flash('パスワードが間違っています。', 'danger')

    # GETリクエストまたは認証失敗時はログインフォームを表示
    return render_template('login.html')

# ログアウト処理
@app.route('/logout')
def logout():
    """ログアウト処理を行う"""
    # セッションからログイン情報を削除
    session.pop('logged_in', None)
    flash('ログアウトしました。', 'info')
    # ログインページへリダイレクト
    return redirect(url_for('login'))


# スクリプトとして直接実行された場合
if __name__ == '__main__':
    # Flask 開発サーバーを起動
    # debug=True は開発時のみ。本番環境では Gunicorn などを使う。
    app.run(host='0.0.0.0', port=5000, debug=True)
