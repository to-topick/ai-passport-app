with open('ai-passport-paid.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. saveProgressにcurrentQIdxを追加
html = html.replace(
    'function saveProgress(chapterId, answers, completed) {\n  try {\n    localStorage.setItem(`ch${chapterId}_progress`, JSON.stringify({ answers, completed }));',
    'function saveProgress(chapterId, answers, completed, qIdx) {\n  try {\n    localStorage.setItem(`ch${chapterId}_progress`, JSON.stringify({ answers, completed, qIdx: qIdx || 0 }));'
)

# 2. startChapterのcurrentQIdx = 0; の前に復元ロジックを追加
html = html.replace(
    '''currentQuestionList = ch.questions.map((q, i) => ({ ...q, _origIdx: i }));
  currentQIdx = 0;
  sessionAnswers = [];
  selectedChoice = null;''',
    '''currentQuestionList = ch.questions.map((q, i) => ({ ...q, _origIdx: i }));
  const savedProgress = getProgress(chapterIdx);
  const savedQIdx = savedProgress.qIdx || 0;
  if (savedQIdx > 0 && !savedProgress.completed) {
    const resume = confirm(`${savedQIdx + 1}問目まで進んでいます。\\n続きから再開しますか？\\n\\n「キャンセル」で最初から始めます。`);
    currentQIdx = resume ? savedQIdx : 0;
  } else {
    currentQIdx = 0;
  }
  sessionAnswers = [];
  selectedChoice = null;'''
)

with open('ai-passport-paid.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("完了")
