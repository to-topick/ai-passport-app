import re

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-free3.html', 'r', encoding='utf-8') as f:
    free_lines = f.readlines()

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'r', encoding='utf-8') as f:
    paid = f.read()

# 1. CSS抽出（行49-63）
css = ''.join(free_lines[48:64])

# 2. ボタンHTML抽出（行456-465）
btn_html = ''.join(free_lines[455:465])

# 3. JS抽出（行714-750）
js = ''.join(free_lines[713:751])

# CSS挿入（</style>の直前）
paid = paid.replace('</style>', css + '\n</style>', 1)

# ボタン挿入（#s2-simpleの直後）
paid = re.sub(
    r'(<div class="explanation-text" id="s2-simple"></div>)',
    r'\1\n' + btn_html.strip(),
    paid
)

# JS挿入（</script>の直前）
paid = paid.replace('</script>', js + '\n</script>', 1)

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'w', encoding='utf-8') as f:
    f.write(paid)

print("CSS・ボタン・JS の移植完了")
