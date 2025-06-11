import requests
import json
import tkinter as tk
from tkinter import messagebox
import time

class AdviceAPIManager:
    """アドバイスAPIとの通信を管理するクラス"""
    
    def __init__(self):
        """クラスの初期化メソッド"""
        # 使用するアドバイスAPIのベースURL
        self.api_url = "https://api.adviceslip.com/advice"
        # リクエストのタイムアウト時間（秒）
        self.timeout = 10
        # HTTPヘッダー情報
        self.headers = {
            'User-Agent': 'WisdomQuotesApp/1.0'
        }
    
    def test_api_connection(self):
        """APIとの接続をテストするメソッド"""
        try:
            # APIに対してGETリクエストを送信
            response = requests.get(
                self.api_url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            # HTTPステータスコードが200番台かチェック
            response.raise_for_status()
            
            # レスポンスが正常に取得できた場合
            print("✓ API接続テスト成功")
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンス時間: {response.elapsed.total_seconds():.2f}秒")
            
            return True
            
        except requests.exceptions.Timeout:
            # タイムアウトエラーの処理
            print("✗ API接続エラー: タイムアウトが発生しました")
            return False
            
        except requests.exceptions.ConnectionError:
            # 接続エラーの処理
            print("✗ API接続エラー: インターネット接続を確認してください")
            return False
            
        except requests.exceptions.RequestException as e:
            # その他のHTTPエラーの処理
            print(f"✗ API接続エラー: {str(e)}")
            return False
    
    def fetch_random_advice(self):
        """ランダムなアドバイスを取得するメソッド"""
        try:
            # APIに対してGETリクエストを送信
            response = requests.get(
                self.api_url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            # HTTPステータスコードをチェック
            response.raise_for_status()
            
            # JSON形式のレスポンスを辞書型に変換
            advice_data = response.json()
            
            # AdviceSlip APIの形式に合わせてデータを整理
            slip_data = advice_data.get('slip', {})
            advice_text = slip_data.get('advice', 'アドバイスを取得できませんでした')
            
            formatted_advice = {
                'content': advice_text,
                'id': slip_data.get('id', 0),
                'length': len(advice_text),
                'category': 'life advice'
            }
            
            return formatted_advice
            
        except requests.exceptions.RequestException as e:
            # エラーが発生した場合のデフォルトデータを返す
            error_advice = {
                'content': 'エラーが発生しました。しばらくしてからもう一度お試しください。',
                'id': 0,
                'length': 0,
                'category': 'error'
            }
            print(f"アドバイス取得エラー: {str(e)}")
            return error_advice
    
    def display_advice_info(self, advice_data):
        """アドバイスデータを整形して表示するメソッド"""
        print("\n" + "="*60)
        print("💡 取得したアドバイス情報")
        print("="*60)
        
        # アドバイスの内容を表示
        print(f"💬 アドバイス: {advice_data['content']}")
        print(f"🔢 ID番号: {advice_data['id']}")
        print(f"📏 文字数: {advice_data['length']}文字")
        print(f"📂 カテゴリ: {advice_data['category']}")
        
        print("="*60 + "\n")
    
    def fetch_multiple_advice(self, count=3):
        """指定した数のアドバイスを取得するメソッド"""
        advice_list = []
        successful_requests = 0
        
        print(f"🔄 {count}個のアドバイスを取得中...")
        
        # 指定された回数だけアドバイスを取得
        for i in range(count):
            print(f"取得中... ({i+1}/{count})")
            
            # 1つずつアドバイスを取得
            advice = self.fetch_random_advice()
            
            # エラーでない場合はリストに追加
            if advice['category'] != 'error':
                advice_list.append(advice)
                successful_requests += 1
            
            # API負荷軽減のため少し待機
            time.sleep(0.5)
        
        print(f"✓ {successful_requests}個のアドバイスを正常に取得しました\n")
        return advice_list
    
    def calculate_advice_stats(self, advice_list):
        """アドバイスリストの統計情報を計算するメソッド"""
        if not advice_list:
            return None
        
        # 文字数のリストを作成
        lengths = [advice['length'] for advice in advice_list]
        
        # 統計情報を計算
        stats = {
            'total_count': len(advice_list),
            'avg_length': round(sum(lengths) / len(lengths), 1),
            'max_length': max(lengths),
            'min_length': min(lengths),
            'total_chars': sum(lengths)
        }
        
        return stats
    
    def display_stats(self, stats):
        """統計情報を表示するメソッド"""
        if not stats:
            print("統計情報がありません")
            return
        
        print("📊 アドバイス統計情報")
        print("-" * 30)
        print(f"総アドバイス数: {stats['total_count']}個")
        print(f"平均文字数: {stats['avg_length']}文字")
        print(f"最長文字数: {stats['max_length']}文字")
        print(f"最短文字数: {stats['min_length']}文字")
        print(f"総文字数: {stats['total_chars']}文字")
        print("-" * 30 + "\n")


class AdviceDisplayGUI:
    """アドバイス表示GUIを管理するクラス"""
    
    def __init__(self):
        """GUIクラスの初期化メソッド"""
        # APIマネージャーのインスタンスを作成
        self.api_manager = AdviceAPIManager()
        
        # メインウィンドウの作成と設定
        self.root = tk.Tk()
        self.setup_window()
        
        # GUI要素用の変数を初期化
        self.advice_text = tk.StringVar()
        self.advice_text.set("「アドバイスを取得」ボタンをクリックしてください")
        
        # ウィジェットを作成
        self.create_widgets()
        
        # レイアウトを設定
        self.setup_layout()
        
    def setup_window(self):
        """メインウィンドウの基本設定を行うメソッド"""
        # ウィンドウのタイトル設定
        self.root.title("人生のアドバイス表示アプリ")
        
        # ウィンドウサイズの設定
        self.root.geometry("600x400")
        
        # ウィンドウの最小サイズを設定
        self.root.minsize(500, 300)
        
        # ウィンドウの背景色を設定
        self.root.configure(bg='#f0f8ff')
        
        # ウィンドウを画面中央に配置
        self.center_window()
        
        # ウィンドウが閉じられる時の処理を設定
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """ウィンドウを画面中央に配置するメソッド"""
        # ウィンドウの更新を待つ
        self.root.update_idletasks()
        
        # 画面の幅と高さを取得
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # ウィンドウの幅と高さを取得
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        
        # 中央配置のための座標を計算
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # ウィンドウの位置を設定
        self.root.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """GUI要素（ウィジェット）を作成するメソッド"""
        # タイトルラベルの作成
        self.title_label = tk.Label(
            self.root,
            text="💡 人生のアドバイス 💡",
            font=("Arial", 20, "bold"),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        
        # アドバイス表示用のラベルを作成
        self.advice_label = tk.Label(
            self.root,
            textvariable=self.advice_text,
            font=("Arial", 12),
            bg='#ffffff',
            fg='#34495e',
            wraplength=450,
            justify='center',
            relief='ridge',
            bd=3,
            padx=20,
            pady=20
        )
        
        # アドバイス取得ボタンの作成
        self.get_advice_button = tk.Button(
            self.root,
            text="アドバイスを取得",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='black',
            activebackground='#2980b9',
            activeforeground='black',
            padx=30,
            pady=12,
            command=self.fetch_new_advice
        )
        
        # ステータス表示用のラベル
        self.status_label = tk.Label(
            self.root,
            text="準備完了",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#7f8c8d'
        )
        
    def setup_layout(self):
        """ウィジェットのレイアウトを設定するメソッド"""
        # タイトルラベルを上部に配置
        self.title_label.pack(pady=(20, 15))
        
        # アドバイス表示ラベルを中央に配置
        self.advice_label.pack(pady=25, padx=20, fill='both', expand=True)
        
        # アドバイス取得ボタンを中央に配置
        self.get_advice_button.pack(pady=15)
        
        # ステータスラベルを下部に配置
        self.status_label.pack(side='bottom', pady=15)
        
    def fetch_new_advice(self):
        """新しいアドバイスを取得してGUIに表示するメソッド"""
        # ステータス更新
        self.status_label.config(text="アドバイスを取得中...")
        self.get_advice_button.config(state='disabled')
        self.root.update()
        
        try:
            # APIからアドバイスを取得
            advice_data = self.api_manager.fetch_random_advice()
            
            # エラーチェック
            if advice_data['category'] == 'error':
                messagebox.showerror("エラー", advice_data['content'])
                self.status_label.config(text="エラーが発生しました")
                return
            
            # アドバイステキストを更新
            display_text = f'"{advice_data["content"]}"'
            self.advice_text.set(display_text)
            
            # ステータス更新
            self.status_label.config(text=f"ID: {advice_data['id']} | 文字数: {advice_data['length']}")
            
        except Exception as e:
            messagebox.showerror("予期しないエラー", f"アドバイスの取得に失敗しました\n{str(e)}")
            self.status_label.config(text="エラーが発生しました")
        finally:
            # ボタンを再度有効化
            self.get_advice_button.config(state='normal')
    
    def on_closing(self):
        """ウィンドウが閉じられる時の処理"""
        result = messagebox.askquestion("終了確認", "アプリケーションを終了しますか？")
        if result == 'yes':
            self.root.destroy()
            
    def run_application(self):
        """GUIアプリケーションを実行するメソッド"""
        print("🖥️  GUIアプリケーションを起動中...")
        
        # 初期接続テストを実行
        if not self.api_manager.test_api_connection():
            messagebox.showwarning(
                "接続警告", 
                "APIサーバーに接続できません。\nインターネット接続を確認してください。"
            )
        
        # メインループを開始
        self.root.mainloop()
        
        print("アプリケーションが終了しました")

def main():
    """GUIアプリケーションを起動するメイン関数"""
    # GUIアプリケーションのインスタンスを作成
    app = AdviceDisplayGUI()
    
    # アプリケーションを実行
    app.run_application()

# プログラムのエントリーポイント
if __name__ == "__main__":
    main()