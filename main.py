import subprocess
import tempfile
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# --- 定数設定 ---
# DockerfileでインストールしたHTSボイスファイルのパス
HTSVOICE_PATH = "/usr/share/open-jtalk/htsvoice/nitech_jp_atr503_m001.htsvoice"
# Dockerfileでインストールした辞書ディレクトリのパス
MECAB_DIC_PATH = "/var/lib/mecab/dic/open-jtalk/naist-jdic"

# リクエストボディの型定義
class TextToSpeechRequest(BaseModel):
    text: str

# レスポンス送信後に一時ファイルを削除する関数
def cleanup_files(files: list):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

@app.get("/")
def read_root():
    return {"message": "Welcome to Open JTalk API on Railway!"}

# @app.post("/synthesize")
# async def synthesize_speech(request: TextToSpeechRequest, background_tasks: BackgroundTasks):
#     """
#     テキストを受け取り、合成された音声(WAV)を返すエンドポイント
#     """
#     # 一時ファイルを作成して、受け取ったテキストを書き込む
#     with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt", encoding='utf-8') as input_file:
#         input_file.write(request.text)
#         input_filepath = input_file.name

#     # 出力用のWAVファイルパスを一時ファイルとして確保
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as output_file:
#         output_filepath = output_file.name

#     # Open JTalkを実行するコマンドを構築
#     command = [
#         'open_jtalk',
#         '-m', HTSVOICE_PATH,
#         '-x', MECAB_DIC_PATH,
#         '-ow', output_filepath,
#         input_filepath
#     ]

#     try:
#         # コマンドを実行して音声合成
#         subprocess.run(command, check=True, text=True, capture_output=True)
#     except subprocess.CalledProcessError as e:
#         # エラーが発生した場合は一時ファイルを削除してエラーレスポンスを返す
#         cleanup_files([input_filepath, output_filepath])
#         return {"error": "Failed to synthesize speech", "details": e.stderr}, 500

#     # レスポンスを送信した後に一時ファイルを削除するタスクを登録
#     background_tasks.add_task(cleanup_files, [input_filepath, output_filepath])

#     # 生成されたWAVファイルを返す
#     return FileResponse(
#         path=output_filepath,
#         media_type='audio/wav',
#         filename='speech.wav'
#     )