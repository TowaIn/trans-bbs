# Dockerfile

FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY deploy/requirements.txt requirements.txt

# 依存関係をインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY source/ /app/

# アプリケーションがlistenするポートを公開
EXPOSE 5000

# コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
