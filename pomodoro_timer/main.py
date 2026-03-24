import tkinter as tk
# from tkinter import ttk
import winsound

class TimerApp:

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
                
        self.root = root
        self.root.title("Pomodoro Timer App")
        self.root.geometry("500x500")
        self.root.configure(bg="#fffacd")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.main_frame.configure(bg="#fffacd")

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

        # タイマーの初期化処理
        self.runningflag = False    #起動中or停止中の判定フラグ

        self.mode = "work"              # or break
        self.remaining_work_seconds = 1500   # 25分(1500)固定値
        self.remaining_break_seconds = 300   # 5分(300)固定値
        self.remaining_seconds = 1500   # 初期値は25分(1500)にあわせる
        self.set_count = 0              # 今何回目か
        self.max_sets = 4               # ループ回数

        # -------------------------
        # mainフレーム内の要素
        # -------------------------
        # ポモドーロカウント(デフォルト 1/4回)
        self.pomodoro_label = tk.Label(self.main_frame, text="ポモドーロタイマー", font=("Arial"), bg="#fffacd")
        self.pomodoro_label.pack(pady=10)
        self.pomodoro_count_label = tk.Label(self.main_frame, text=f"{self.set_count + 1}/{self.max_sets}回", font=("Arial", 20), bg="#fffacd")
        self.pomodoro_count_label.pack(pady=(0,20))

        # タイム表示(デフォルト25分表示)
        self.worktime_label = tk.Label(self.main_frame, text="作業時間", font=("Arial"), bg="#fffacd")
        self.worktime_label.pack(pady=10)
        self.countdown_label = tk.Label(self.main_frame, text=f"{self.remaining_work_seconds//60:02}:00", font=("Arial", 40), bg="#fffacd")
        self.countdown_label.pack(pady=(0,20))

        # タイム表示(デフォルト5分表示)
        self.breaktime_label = tk.Label(self.main_frame, text="休憩時間", font=("Arial"), bg="#fffacd")
        self.breaktime_label.pack()
        self.breaktime_time = tk.Label(self.main_frame, text=f"{self.remaining_break_seconds//60:02}:00", font=("Arial", 40), bg="#fffacd")
        self.breaktime_time.pack(pady=(0,20))

        #ポモドーロの詳細設定は現状没⇒TODO いつか実装予定
        # #ポモドーロのラベル
        # self.pomodoro_label = tk.Label(self.main_frame, text="ポモドーロ回数", bg="#fffacd")
        # self.pomodoro_label.pack()
        # #コンボボックスでポモドーロの設定
        # self.pomodoro_conbobox = ttk.Combobox(self.main_frame, values=["1回","2回","3回","4回"])
        # self.pomodoro_conbobox.pack(pady=(20,20))

        # 分設定ボタン横並べの為のフレーム
        # self.button_frame = tk.Frame(self.main_frame, bg="#fffacd")
        # self.button_frame.pack()
        # # プラス5分
        # self.one_minutes_button = tk.Button(self.button_frame, text="＋5分", command=None ,bg="#f0ffff", fg="#000000")
        # self.one_minutes_button.pack(side="left", padx=(20,20), pady=(20,20))
        # # マイナス5分
        # self.ten_seccond_button = tk.Button(self.button_frame, text="-5分", command=None,bg="#f0ffff", fg="#000000")
        # self.ten_seccond_button.pack(side="left", padx=(20,20), pady=(20,20))

        # start
        self.start_button = tk.Button(self.main_frame, text="START", command=self.start ,bg="#fa8072", fg="#696969")
        self.start_button.pack(side="left", padx=(20,20))

        # reset
        self.reset_button = tk.Button(self.main_frame, text="RESET", command=self.reset, bg="#98fb98", fg="#696969")
        self.reset_button.pack(side="left", padx=(20,20))

        # resetボタンを無効にしておく
        self.toggle_buttons(False)


    def start(self):
        #起動フラグをTrueへ
        self.runningflag = True
        # 起動フラグがTureなら実行(念のためif)
        if self.runningflag:
            self.toggle_buttons(True)
            self.tick()
        return
    
    def reset(self):
        #起動フラグをFalseへ
        self.runningflag = False
        # 起動フラグがFalseなら実行(念のためif)
        if not self.runningflag:        # タイマーの初期化処理
            self.runningflag = False    #起動中or停止中の判定フラグ

            self.mode = "work"              # or break
            self.remaining_seconds = 1500   # 25分(1500)固定値(残り時間)
            self.set_count = 0              # 今何回目か
            self.max_sets = 4               # ループ回数
            self.pomodoro_count_label.config(text=f"{self.set_count + 1}/{self.max_sets}回")
            self.countdown_label.config(text=f"{self.remaining_work_seconds//60:02}:00")
            self.breaktime_time.config(text=f"{self.remaining_break_seconds//60:02}:00")
            # startボタンを有効化
            self.toggle_buttons(False)

            return

    def update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        if self.mode == "work":
            self.countdown_label.config(text=f"{minutes:02}:{seconds:02}")
        elif self.mode == "break":
            self.breaktime_time.config(text=f"{minutes:02}:{seconds:02}")
        return        

    def tick(self):
        # runningフラグが真なら実行
        if self.runningflag:
            self.remaining_seconds -= 1
        else:
            #フラグはFalseなら処理しない
            return

        if self.remaining_seconds <= 0:
            
            # システムアスタリスク音（ポーン）
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

            if self.mode == "work":
                self.mode = "break"
                self.remaining_seconds = 300 # 5分(300)
                # mode切り替わりでラベルの初期化を行う
                self.countdown_label.config(text=f"{self.remaining_work_seconds//60:02}:00")

            else:
                # set_countを1つ進める
                self.set_count += 1

                # set_countがmax_setsと同数以上なら処理を終える
                if self.set_count >= self.max_sets:
                    self.runningflag = False
                    # ラベルの初期化
                    self.countdown_label.config(text=f"{self.remaining_work_seconds//60:02}:00")
                    self.breaktime_time.config(text=f"{self.remaining_break_seconds//60:02}:00")
                    return
                
                #ポモドーロの回数ラベルを更新
                self.pomodoro_count_label.config(text=f"{self.set_count + 1}/{self.max_sets}回")
                self.mode = "work"
                self.remaining_seconds = 1500 # 25分(1500)
                # mode切り替わりでラベルの初期化を行う
                self.breaktime_time.config(text=f"{self.remaining_break_seconds//60:02}:00")

        print(self.mode, self.remaining_seconds, self.set_count)
        self.update_display()

        root.after(1000, self.tick)
    
    def toggle_buttons(self, flag):
        if flag:
            self.start_button.config(state="disabled")
            self.reset_button.config(state="normal")
        else:
            self.start_button.config(state="normal")
            self.reset_button.config(state="disabled")



# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #TrainingAppのインスタンスを生成⇒initを実行(1回)
    app = TimerApp(root)
    #イベント待ちループ開始
    root.mainloop()

