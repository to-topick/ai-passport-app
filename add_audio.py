import re

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'r', encoding='utf-8') as f:
    html = f.read()

count = 0
def replacer(m):
    global count
    count += 1
    return m.group(0) + f"\n        audioFile: 'audio/q{count}.mp3',"

html_new = re.sub(r"(simple: `[^`]*`,)", replacer, html)

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"{count}問にaudioFileを追加しました")
