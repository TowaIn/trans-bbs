# Dockerfile

# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY deploy/requirements.txt requirements.txt

# 依存関係をインストール
# --no-cache-dir: キャッシュを使用しない
# --upgrade pip: pip自体をアップグレード
# -r requirements.txt: requirements.txt に基づいてインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY source/ /app/

# アプリケーションがリッスンするポートを公開
EXPOSE 5000

# コンテナ起動時に実行するコマンド
# gunicornを使うのが一般的だが、ここでは簡易的にpython直接実行
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]
