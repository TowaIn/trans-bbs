# app.py
# -*- coding: utf-8 -*-

# 必要なモジュールをインポート
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup, escape # HTMLエスケープと安全なマークアップのためにインポート

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 投稿データを一時的に保存するためのリスト (インメモリ)
posts = []
# 投稿に一意のIDを割り振るためのカウンター
post_id_counter = 0

# --- ▼▼▼ nl2br カスタムフィルタの定義と登録 ▼▼▼ ---
def nl2br(value):
    """
    文字列内の改行文字をHTMLの<br>タグに変換するカスタムフィルタ。
    安全のため、まずHTMLエスケープを行ってから改行を置換し、
    最後にMarkupオブジェクトとして返す。
    """
    if value:
        # 1. 入力文字列をHTMLエスケープする
        escaped_value = escape(value)
        # 2. エスケープされた文字列中の改行コード (\r\n, \r, \n) を <br>\n に置換する
        #    (\n を末尾に追加するのは生成されるHTMLソースの可読性のため)
        formatted_value = escaped_value.replace('\r\n', '<br>\n').replace('\r', '<br>\n').replace('\n', '<br>\n')
        # 3. 変換後の文字列を Markup オブジェクトでラップする
        #    これにより、Jinja2が <br> タグを再度エスケープするのを防ぐ
        return Markup(formatted_value)
    # 値がない場合は空文字列を返す
    return ""

# 作成した nl2br 関数を 'nl2br' という名前で Jinja2 テンプレートエンジンにフィルタとして登録
app.jinja_env.filters['nl2br'] = nl2br
# --- ▲▲▲ nl2br カスタムフィルタの定義と登録 ▲▲▲ ---


# ルートURL ('/') にアクセスがあった場合に実行される関数
@app.route('/')
def index():
    """
    投稿一覧ページを表示する。
    posts リストを逆順にして、新しい投稿が上に表示されるようにテンプレートに渡す。
    """
    # 'index.html' テンプレートをレンダリングして返す
    # posts=reversed(posts) で投稿リストをテンプレートに渡す
    return render_template('index.html', posts=reversed(posts))


# '/post' URL に POST メソッドでアクセスがあった場合に実行される関数
@app.route('/post', methods=['POST'])
def post():
    """
    新しい投稿を受け取り、リストに追加してトップページにリダイレクトする。
    """
    # グローバル変数のカウンターを変更するため global宣言
    global post_id_counter

    # フォームから送信された 'username' と 'message' を取得
    # username が空の場合は '名無しさん' をデフォルト値とする
    username = request.form.get('username', '名無しさん')
    message = request.form.get('message')

    # メッセージが空でない場合のみ投稿を処理
    if message:
        # 投稿IDをインクリメント
        post_id_counter += 1
        # 新しい投稿データを辞書として作成し、posts リストに追加
        posts.append({
            'id': post_id_counter,
            'username': username if username else '名無しさん', # usernameが空文字の場合も考慮
            'message': message
        })

    # 投稿処理後、トップページ ('/') にリダイレクトする
    return redirect(url_for('index'))


# このスクリプトが直接実行された場合にのみ以下のコードを実行
if __name__ == '__main__':
    # Flask の開発用サーバーを起動する
    # host='0.0.0.0' はコンテナ内から外部のアクセスを受け付けるために必要
    # port=5000 は Flask のデフォルトポート (変更可能)
    # debug=True は開発時にエラー表示や自動リロードを有効にする (本番環境では False にする)
    app.run(host='0.0.0.0', port=5000, debug=True)
