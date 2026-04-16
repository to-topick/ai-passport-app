import re

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-free3.html', 'r', encoding='utf-8') as f:
    free_lines = f.readlines()

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'r', encoding='utf-8') as f:
    paid_lines = f.readlines()

# 1. CSS抽出（行49-63）
css = ''.join(free_lines[48:64])

# 2. ボタンHTML抽出（行456-465）
btn_html = ''.join(free_lines[455:465])

# 3. JS抽出（行714-750）
js = ''.join(free_lines[713:752])

# CSS挿入：行398の</style>の直前に挿入
paid_lines.insert(397, css)

# 挿入後に行番号がずれるので再検索
paid = ''.join(paid_lines)

# ボタン挿入（#s2-simpleの直後）
paid = re.sub(
    r'(<div class="explanation-text" id="s2-simple"></div>)',
    r'\1\n' + btn_html.strip() + '\n',
    paid
)

# JS挿入：</script>の直前（最後の1個）
last_script = paid.rfind('</script>')
paid = paid[:last_script] + js + '\n' + paid[last_script:]

# audioFile追加
count = 0
def replacer(m):
    global count
    count += 1
    return m.group(0) + f"\n        audioFile: 'audio/q{count}.mp3',"

paid = re.sub(r"(simple: `[^`]*`,)", replacer, paid)

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'w', encoding='utf-8') as f:
    f.write(paid)

print(f"完了: audioFile {count}問, CSS/ボタン/JS移植済み")
