# 人生の名言表示アプリケーション

## プロジェクト内容

Web APIから取得したランダムな人生の名言を表示するGUIデスクトップアプリケーションです。HTTP通信によるデータ取得、JSON形式でのデータ処理、tkinterを使用したグラフィカルユーザーインターフェースの実装まで一連の処理を統合し、実用的なデスクトップアプリケーションを作成しました。PythonによるWeb API連携とGUI開発技術を学習することを目的として実装しました。

## プロジェクト構成

```
wisdom_quotes_app/
├── quote_display_app.py        # メインアプリケーション
├── requirements.txt            # 依存関係管理
├── README.md                   # プロジェクト説明書
└── .gitignore                  # Git除外ファイル設定
```

## 必要要件/開発環境

- **Python 3.7以上**
- **VSCode** (開発環境)
- **Git** (バージョン管理)
- **インターネット接続** (API通信のため)

### 使用ライブラリ

- **requests** HTTP通信とWeb API連携処理
- **tkinter** GUIアプリケーション作成
- **json** JSON形式データの処理
- **time** API負荷軽減のための待機処理

## 機能

- **Web API連携** Advice Slip APIからランダムな名言を取得
- **リアルタイムデータ表示** 取得した名言をGUIで即座に表示
- **エラーハンドリング** ネットワークエラーやAPI障害への適切な対応
- **ユーザーフレンドリーなGUI** 直感的に操作できるデスクトップインターフェース
- **接続テスト機能** アプリケーション起動時のAPI接続確認
- **ステータス表示** 取得処理の進行状況と名言情報の表示
- **ウィンドウ管理** 画面中央配置と終了確認ダイアログ
- **レスポンシブデザイン** ウィンドウサイズ変更に対応した動的レイアウト

## 実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/wisdom_quotes_app.git
cd wisdom_quotes_app
```

### 2. 仮想環境の作成・アクティベート

**Windows**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. アプリケーションの実行

```bash
python quote_display_app.py
```

実行後、GUIウィンドウが起動し、「名言を取得」ボタンをクリックすることで新しい名言が表示されます。

## 使用API

- **Advice Slip API** (https://api.adviceslip.com/)
  - 無料で利用可能な名言提供API
  - JSON形式でランダムな名言を返却
  - レート制限あり（適切な間隔での利用を推奨）

## 開発者

YuYu