import sys
import os
import tkinter as tk
import logging
from logging.handlers import RotatingFileHandler

# =====================================
# 実行ディレクトリを取得
# exe化時対応用
# =====================================
def get_base_path():
    if getattr(sys,'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# =====================================
# logs及びDBディレクトリを作成
# =====================================
def mkdir_logs():
    base_path = get_base_path()
    
    log_dir = os.path.join(base_path, "logs")

    # フォルダが既に存在していてもエラーにはならない
    os.makedirs(log_dir, exist_ok=True)

    log_path= os.path.join(log_dir, "app.log")
    
    return log_path

#======================================
# logging 設定
#======================================
#ディレクトリがなければ作成
mkdir_logs()
# Logger 作成
logger = logging.getLogger("resale_app")
logger.setLevel(logging.INFO)

# handler 作成
log_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes = 1024 * 1024, # 1MBでローテーション
        backupCount = 3,        # 古いログを3世代保持
        encoding = "utf-8"
    )

# formatter
log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
log_handler.setFormatter(log_formatter)

# handler 登録(重複防止)
if not logger.handlers:
    logger.addHandler(log_handler)


class CounterApp:

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
        logger.info("__init__ start")
        self.root = root
        self.count = 0
        self.root.title("Counter App")
        self.root.geometry("300x300")
        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        #初期表示
        self.create_main_frame()

    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_main_frame(self):
        logger.info("create_main_frame start")
        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(root)

        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=root.quit)
        #区切り線を出すための記述
        # file_menu.add_separator()

        # -------------------------
        # mainフレーム内の要素
        # -------------------------
        # カウント表示用ラベル
        self.display_count = tk.Label(self.main_frame, text='0', font=('Arial', 40))
        self.display_count.pack()

        #加算用ボタン
        btn_plus = tk.Button(self.main_frame, text="+1", command=self.plus)
        btn_plus.pack(side="left", padx=(10,10))

        #減算用ボタン
        btn_minus = tk.Button(self.main_frame, text="-1", command=self.minus)
        btn_minus.pack(side="left", padx=(10,10))

        #reset用ボタン
        btn_reset = tk.Button(self.main_frame, text="Reset", command=self.reset)
        btn_reset.pack(side="left", padx=(10,10))

    def plus(self):
        logger.info("cont : plus")
        self.count +=1
        self.display_count['text'] = self.count
    
    def minus(self):
        logger.info("cont : minus")
        self.count -= 1
        self.display_count['text'] = self.count
    
    def reset(self):
        logger.info("cont : reset")
        self.count = 0
        self.display_count['text'] = self.count

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    logger.info("start main")
    #ウィンドウを作る
    root = tk.Tk()
    #CounterAppのインスタンスを生成⇒initを実行(1回)
    app = CounterApp(root)
    #イベント待ちループ開始
    root.mainloop()

