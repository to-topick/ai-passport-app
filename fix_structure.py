with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'r', encoding='utf-8') as f:
    html = f.read()

old = '        <div class="simple-explanation">\n            <div class="explanation-title">かんたん解説</div>\n            <div class="explanation-text" id="s2-simple"></div>\n<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">\n            <div class="explanation-title" style="margin-bottom:0;">かんたん解説</div>\n'

new = '        <div class="simple-explanation">\n<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">\n            <div class="explanation-title" style="margin-bottom:0;">かんたん解説</div>\n'

if old in html:
    html = html.replace(old, new)
    # s2-simpleをbuttonの後に追加
    html = html.replace(
        '        </button>\n\n        </div>\n',
        '        </button>\n        </div>\n            <div class="explanation-text" id="s2-simple"></div>\n'
    )
    print("置換成功")
else:
    print("置換対象が見つかりません")

with open('/Users/tomo/Desktop/ai-passport-app/ai-passport-paid.html', 'w', encoding='utf-8') as f:
    f.write(html)
