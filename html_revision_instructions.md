# HTML改修指示書：第2章ストーリーモード実装

対象ファイル：`ai-passport-paid.html`

---

## 概要

第2章だけ「導入ステップ」を追加した5ステップ構成に変更する。
第1・3・4・5章は現在の4ステップのまま維持する。

### 現在の構成（全章共通）
- STEP 1：問題を読む
- STEP 2：解説を読む（かんたん解説 / 詳しい解説）
- STEP 3：問題を解く
- STEP 4：答え合わせ

### 変更後の構成（第2章のみ）
- STEP 0：導入（日常の「なぜ？」）← 新規追加
- STEP 1：問題を見る（答えは選ばなくてOK）
- STEP 2：解説を読む
- STEP 3：問題に挑戦
- STEP 4：答え合わせ

---

## 作業1：`chapters`配列に`style`フラグを追加

**対象行（約2156〜2162行）：**

```js
// 変更前
const chapters = [
  { id: 1, title: 'AI（人工知能）', subtitle: '第1章', questions: ch1Questions, color: '#f4a7b9', fillColor: '#e8849a', emoji: '🤖' },
  { id: 2, title: '生成AI（ジェネレーティブAI）', subtitle: '第2章', questions: ch2Questions, color: '#a8d5c2', fillColor: '#7bbfa8', emoji: '✨' },
  ...
];

// 変更後
const chapters = [
  { id: 1, title: 'AI（人工知能）', subtitle: '第1章', questions: ch1Questions, color: '#f4a7b9', fillColor: '#e8849a', emoji: '🤖', style: 'standard' },
  { id: 2, title: '生成AI（ジェネレーティブAI）', subtitle: '第2章', questions: ch2Questions, color: '#a8d5c2', fillColor: '#7bbfa8', emoji: '✨', style: 'story' },
  { id: 3, title: '生成AIの動向', subtitle: '第3章', questions: ch3Questions, color: '#c4b5e8', fillColor: '#9d8cd4', emoji: '🔥', style: 'standard' },
  { id: 4, title: 'リテラシー・ガイドライン・AI新法', subtitle: '第4章', questions: ch4Questions, color: '#f7c4a0', fillColor: '#e09060', emoji: '⚖️', style: 'standard' },
  { id: 5, title: 'プロンプト制作と実例', subtitle: '第5章', questions: ch5Questions, color: '#b0d4f1', fillColor: '#6aaee8', emoji: '💬', style: 'standard' },
];
```

---

## 作業2：`step0`パネルをHTMLに追加

**挿入位置：** 514行目の `<!-- STEP 1: View question -->` の直前

```html
<!-- STEP 0: Introduction (第2章のみ) -->
<div class="card hidden" id="step0">
  <div class="step-tag" style="background:var(--mint-light); color:var(--mint-deep);">🌱 はじめに — 今日の「なぜ？」</div>
  <div class="explanation-text" id="s0-intro" style="font-size:15px; line-height:1.9; padding:8px 0;"></div>
  <button class="btn btn-primary" onclick="showStep(1)">問題を見てみる →</button>
</div>
```

---

## 作業3：`hideAllQuizPanels()`に`step0`を追加

**対象行（約2488〜2492行）：**

```js
// 変更前
function hideAllQuizPanels() {
  ['step1','step2','stepDeepDive','stepAnki','step3','step4','stepComplete'].forEach(id => {
    document.getElementById(id).classList.add('hidden');
  });
}

// 変更後
function hideAllQuizPanels() {
  ['step0','step1','step2','stepDeepDive','stepAnki','step3','step4','stepComplete'].forEach(id => {
    document.getElementById(id).classList.add('hidden');
  });
}
```

---

## 作業4：`showStep()`に第2章の条件分岐を追加

**対象行（約2494〜2513行）：**

```js
// 変更前
function showStep(n) {
  hideAllQuizPanels();
  updateProgressBar();
  const q = getCurrentQ();
  const total = currentQuestionList.length;
  const qLabel = `Q${currentQIdx + 1} / ${total}`;

  if (n === 1) {
    updateStepIndicator(1);
    document.getElementById('s1-qnum').textContent = qLabel;
    document.getElementById('s1-qtext').innerHTML = q.question;
    renderChoices('s1-choices', q.choices, false);
    document.getElementById('step1').classList.remove('hidden');
    window.scrollTo(0, 0);
  } else if (n === 2) {
    showStep2Internal(q, qLabel);
  } else if (n === 3) {
    showStep3Internal(q, qLabel);
  }
}

// 変更後
function showStep(n) {
  hideAllQuizPanels();
  updateProgressBar();
  const q = getCurrentQ();
  const total = currentQuestionList.length;
  const qLabel = `Q${currentQIdx + 1} / ${total}`;
  const isStory = currentChapterIdx !== null && chapters[currentChapterIdx].style === 'story';

  if (n === 0 && isStory) {
    // 第2章専用：導入ステップ
    document.getElementById('s0-intro').innerHTML = q.intro || '';
    document.getElementById('step0').classList.remove('hidden');
    window.scrollTo(0, 0);
  } else if (n === 1) {
    updateStepIndicator(1);
    document.getElementById('s1-qnum').textContent = qLabel;
    document.getElementById('s1-qtext').innerHTML = q.question;
    renderChoices('s1-choices', q.choices, false);
    document.getElementById('step1').classList.remove('hidden');
    window.scrollTo(0, 0);
  } else if (n === 2) {
    showStep2Internal(q, qLabel);
  } else if (n === 3) {
    showStep3Internal(q, qLabel);
  }
}
```

---

## 作業5：`startChapter()`の最後の`showStep(1)`を条件分岐に変更

**対象行（約2326行）：**

```js
// 変更前
  showStep(1);
}

// 変更後
  const isStory = chapters[chapterIdx].style === 'story';
  showStep(isStory ? 0 : 1);
}
```

---

## 作業6：シャッフル機能の削除

### 6-1. `startShuffle()`関数を削除
約2329〜2356行の`function startShuffle() { ... }`ブロック全体を削除する。

### 6-2. `retryChapter()`のシャッフル分岐を削除
約2364〜2370行：

```js
// 変更前
function retryChapter() {
  if (isShuffleMode) {
    startShuffle();
  } else {
    startChapter(currentChapterIdx);
  }
}

// 変更後
function retryChapter() {
  startChapter(currentChapterIdx);
}
```

### 6-3. `isShuffleMode`変数とシャッフルUI要素を削除
- `let isShuffleMode = false;`（約2172行）を削除
- HTMLの「全章シャッフルモード」ボタンまたはカード（`onclick="startShuffle()"`のある要素）を削除

---

## 作業7：第2章問題データに`intro`フィールドを追加

`ch2Questions`配列の各問題オブジェクトに`intro`フィールドを追加する。
内容は別ファイル`ch2_q1_q20_revised.md`の「**導入**」セクションのテキストを使うこと。

### データ形式（例：Q1）

```js
{
  chapter: '第2章 生成AI（ジェネレーティブAI）',
  question: '...（既存の問題文）...',
  choices: [...],
  correct: ...,
  intro: `YouTubeを見ていると、気づいたら1時間経っていた——そんな経験はありませんか？<br><br>あれは偶然ではありません。YouTubeのAIが「この人は次にこの動画を見る確率が高い」と予測しているからです。<br><br>では、AIはどうやってそれを学習しているのでしょう？`,
  simple: `...（既存のsimple）...`,
  ...
}
```

**Q1〜Q20の`intro`テキスト一覧（`ch2_q1_q20_revised.md`の「導入」セクションより）：**

---

### Q1
```
YouTubeを見ていると、気づいたら1時間経っていた——そんな経験はありませんか？<br><br>あれは偶然ではありません。YouTubeのAIが「この人は次にこの動画を見る確率が高い」と予測しているからです。<br><br>では、AIはどうやってそれを学習しているのでしょう？
```

### Q2
```
桃の花と桜の花、どちらも春に咲く白やピンクの花ですよね。<br><br>でもAIは写真を見るだけで、どちらかを正確に見分けることができます。<br><br>いったい何を手がかりに見分けているのでしょう？
```

### Q3
```
インスタなどの画像加工機能で、目の大きさや顔の輪郭をスライダーで調整したことはありませんか？<br><br>あの「顔の特徴を数値で操作する」という発想、実はAIの画像生成技術と深いところでつながっています。<br><br>どういうことでしょう？
```

### Q4
```
迷惑メールフォルダを見たことはありますか？<br><br>実は迷惑メールはどんどん巧妙になっています。フィルターをくぐり抜けようと進化する。フィルターもそれを見破ろうと進化する。<br><br>このいたちごっこ、AIの学習に応用したらどうなるでしょう？
```

### Q5
```
連続ドラマを第5話から見始めたら、人間関係がさっぱりわかりませんよね。<br><br>「この人、なんで泣いてるの？」「この2人、どういう関係？」<br><br>前の話を知っているかどうかで、理解度がまったく変わります。AIも同じ問題を抱えていました。
```

### Q6
```
メールに「例の件ですが」と書いてあったとき、それが何を指すかすぐわかりますよね。<br><br>でも何週間も前のやりとりを指していたら？メールが100通以上あったら？<br><br>人間は文脈を遡って理解できますが、AIにとってこれは長い間、難しい問題でした。
```

### Q7
```
同じ部署でも、企画書をスラスラ書ける人もいれば、膨大なデータを読み込んで分析するのが得意な人もいますよね。<br><br>GPTとBERTも同じです。どちらも同じTransformerから生まれたのに、得意なことがまったく違います。
```

### Q8
```
調べものをするとき、100冊の専門書を読み込んで深く理解する人もいれば、1冊の辞書でサッと要点をつかむ人もいますよね。<br><br>BERTを改良した2つのモデルも、まったく逆の方向に進化しました。
```

### Q9
```
ボルツマンマシン、CNN、RNN・LSTM、VAE、GAN、Transformer、GPT・BERT——ここまで8つの技術が登場しました。<br><br>それぞれの特徴、頭に入っていますか？
```

### Q10
```
「賢すぎて公開できない」——そんなことがあると思いますか？<br><br>2019年、OpenAIはAIを開発したのに「危険すぎる」という理由で完全公開を見送りました。<br><br>いったいどんなAIだったのでしょう？
```

### Q11
```
ゲームのキャラクターも、レベルが上がるほど強くなりますよね。<br><br>でもあるとき、「レベルが高すぎると、今まで使えなかったスキルが突然解放される」ことがあります。<br><br>AIにも同じことが起きました。
```

### Q12
```
新入社員が「仕事はできるけど、話し方が一方的で使いにくい」という状況、想像できますか？<br><br>頭はいい。でも一緒に仕事するのが難しい。<br><br>GPT-3もまさにそういう状態でした。
```

### Q13
```
「文字だけ読めるけど、写真は見られない」——そんな人がいたとしたら、できることはかなり限られますよね。<br><br>ChatGPTも長い間、テキストしか扱えませんでした。<br><br>GPT-4でそれが変わります。
```

### Q14
```
テストで「直感で答える人」と「じっくり考えてから答える人」、どちらが難問に強いでしょうか？<br><br>AIも同じ問いを抱えていました。そして「じっくり考える」専用のモデルが登場します。
```

### Q15
```
スマホのアプリも、「電話アプリ」「カメラアプリ」「地図アプリ」と、用途ごとに分かれていますよね。<br><br>OpenAIも、ChatGPT本体のほかに、用途別のツールをどんどん展開しています。<br><br>どれが何をするものか、整理できていますか？
```

### Q16
```
Excelで「データをグラフにして」と誰かに頼めたら楽ですよね。<br><br>しかも「レシピ提案専用のアシスタント」を自分で作れたら？<br><br>ChatGPTで、それが実際にできるようになっています。
```

### Q17
```
「このAI、絶対に嘘をつかない」——そう言い切れる人はいるでしょうか？<br><br>試験でも日常でも、この「断言」には要注意です。
```

### Q18
```
スマホはiPhoneとAndroidが二大勢力ですよね。<br><br>生成AIの世界も、ChatGPTひとり勝ちではありません。Google、Anthropic、Microsoftがそれぞれ独自のAIを展開しています。<br><br>開発元と名前、混同していませんか？
```

### Q19
```
「新しいアプリをわざわざ開く」のが面倒、と感じたことはありませんか？<br><br>MicrosoftはAIを「別のアプリ」ではなく、すでに使っているWordやExcelの中に溶け込ませました。<br><br>それが<strong>Copilot</strong>です。
```

### Q20
```
第2章では、生成AIの誕生から現在の主要モデルまでを一気に学んできました。<br><br>試験で狙われやすいのは「知っているようで混同しやすいポイント」です。<br><br>最後にそこを確認しましょう。
```

---

## 注意事項

- **第2章以外の章は一切触らないこと**
- `step0`パネルはシャッフルモード中は表示しない（`isStory`の条件で自動的に除外される）
- シャッフル機能削除後、`isShuffleMode`変数が残っていないか確認すること
- 既存の`simple`・`deepdive`・`summary`フィールドは変更しないこと

---

## 完了確認チェックリスト

- [ ] 第2章を開始すると「はじめに」パネルが表示される
- [ ] 「問題を見てみる →」で通常のSTEP 1に進む
- [ ] 第1・3・4・5章は従来通りSTEP 1から始まる
- [ ] シャッフルボタンが消えている
- [ ] シャッフルモード中は`step0`が表示されない
- [ ] LocalStorage進捗保存・TTS・答え合わせが正常動作する
