# ai-passport-app

## プロジェクト概要
生成AIパスポート資格試験の学習アプリ。
単一HTMLファイル（ai-passport-paid.html）で動作する。

## ターゲットユーザー
AI用語に躓いた非IT系の初学者。
既存の問題集やネット検索の解説が「ある程度わかっている前提」で書かれているため、
どんなに調べても理解できない人に届けることを目的としている。

## ファイル構成
ai-passport-paid.html  # メインファイル（CSS・JS・問題データをすべて含む）
audio/free/            # 無料問題の音声
audio/paid/            # 有料問題の音声
.claude/rules/         # 判断の上位原則（作業前に必ず参照）
.claude/skills/        # 実行ノウハウ（解説生成・実装の具体的な手順）

## 問題構成
5章・80問
各問のフィールド：chapter / type / elimination / question / choices /
correct / intro / simple / deepdive / summary / related / anki /
audioFile / eliminationReasons

## 作業ルール
- 作業前に必ず .claude/rules/philosophy.md を参照すること
- 実装・変更前にユーザーに確認すること。独断で進めない
- タスク単位の作業指示書（mdファイル）はルートに置く
  使い終わったら削除する。ルートに残っているmdは作業中のもの

## 将来の展開
他の資格試験アプリへのシリーズ展開を想定している。
再利用性を意識した設計を心がける。
