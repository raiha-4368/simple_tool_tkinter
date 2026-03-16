import tkinter as tk

class CounterApp:

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#fffacd")
        self.count = 0
        self.root.title("Counter App")
        self.root.geometry("300x300")
        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = tk.Frame(self.root, bg="#fffacd")
        self.main_frame.pack()

        #初期表示
        self.create_main_frame()

    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_main_frame(self):
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
        self.display_count = tk.Label(self.main_frame, text='0', font=('Arial', 40),bg="#fffacd")
        self.display_count.pack()

        #加算用ボタン
        btn_plus = tk.Button(self.main_frame, text="+1", command=self.plus, font=('Arial', 20), bg="#fa8072", fg="#696969")
        btn_plus.pack(side="left", padx=(10,10))

        #減算用ボタン
        btn_minus = tk.Button(self.main_frame, text="-1", command=self.minus, font=('Arial', 20), bg="#add8e6", fg="#696969")
        btn_minus.pack(side="left", padx=(10,10))

        #reset用ボタン
        btn_reset = tk.Button(self.main_frame, text="Reset", command=self.reset, font=('Arial', 20), bg="#98fb98", fg="#696969")
        btn_reset.pack(side="left", padx=(10,10))

    def plus(self):
        self.count +=1
        self.display_count['text'] = self.count
    
    def minus(self):
        self.count -= 1
        self.display_count['text'] = self.count
    
    def reset(self):
        self.count = 0
        self.display_count['text'] = self.count

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #CounterAppのインスタンスを生成⇒initを実行(1回)
    app = CounterApp(root)
    #イベント待ちループ開始
    root.mainloop()

