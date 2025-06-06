# ベースとなるPythonイメージを選択
FROM python:3.9-slim

# apt-getを非対話モードで実行する設定
ENV DEBIAN_FRONTEND=noninteractive

# Open JTalkと日本語辞書をインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# Pythonライブラリのリストをコピー
COPY requirements.txt requirements.txt

# Pythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトの全ファイルをコピー
COPY . .

# APIサーバーを起動
# Railwayは自動的にPORT環境変数を設定します
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]