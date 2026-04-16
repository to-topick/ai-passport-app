import re
import os
from openai import OpenAI

api_key = input("OpenAI APIキーを入力してください: ")
client = OpenAI(api_key=api_key)

with open(os.path.expanduser("~/Desktop/ai-passport-app/ai-passport-paid.html"), "r", encoding="utf-8") as f:
    html = f.read()

simples = re.findall(r'simple:\s*`([^`]*)`', html)
print(f"{len(simples)}問分のテキストを抽出しました")

audio_dir = os.path.expanduser("~/Desktop/ai-passport-app/audio")
os.makedirs(audio_dir, exist_ok=True)

for i, text in enumerate(simples, 1):
    clean = re.sub(r'<[^>]+>', '', text).strip()
    clean = re.sub(r'\s+', ' ', clean)
    out_path = f"{audio_dir}/q{i}.mp3"
    if os.path.exists(out_path):
        print(f"q{i}.mp3 スキップ（既存）")
        continue
    print(f"生成中: q{i}.mp3 ({len(clean)}文字)")
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=clean,
        speed=1.15,
        instructions="やさしく、ゆっくりと、学習者に語りかけるように話してください"
    )
    response.stream_to_file(out_path)
    print(f"✓ q{i}.mp3 保存完了")

print("全完了！")
