import os
from openai import OpenAI

client = OpenAI()

texts = {
    "q1": "AI（人工知能）という言葉は、1956年にアメリカで開かれた「ダートマス会議」で初めて使われました。提唱したのはジョン・マッカーシーという研究者で、この会議がAI研究という分野の出発点とされています。",
    "q2": "AIとロボットは別の概念です。AIは知覚・認識・学習・問題解決などの知能を再現するソフトウェアやアルゴリズム。ロボットは物理的な動作を行う機械。ロボットにAIが搭載されることもありますが、すべてのロボットにAIが入っているわけではありません。",
    "q3": "ルールベースのAIは、人間が「もし○○なら△△する」というルールをすべて書いておき、その通りに動く仕組みです。ルールが明確な場面では正確に動きますが、ルールに書かれていない想定外の状況には対応できないという弱点があります。"
}

os.makedirs("audio/paid", exist_ok=True)

for key, text in texts.items():
    output_path = f"audio/paid/{key}.mp3"
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text,
        speed=1.15,
        instructions="やさしく、ゆっくりと、学習者に語りかけるように話してください"
    )
    response.stream_to_file(output_path)
    print(f"生成完了: {output_path}")

print("全て完了しました")
