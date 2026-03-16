import time
import tkinter as tk

class StopwatchApp:

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
                
        self.root = root
        self.root.configure(bg="#fffacd")
        self.root.title("Stopwatch App")
        self.root.geometry("500x500")
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


        # タイマーの初期化処理
        self.start_time = 0
        self.elapsed_time = 0
        self.runningflag = False
        self.after_id = None    #予約したアフター管理用ID

        # -------------------------
        # mainフレーム内の要素
        # -------------------------        
        # タイム表示
        self.stopwatch_label = tk.Label(self.main_frame, text="00:00:00", font=("Arial", 40), bg="#fffacd")
        self.stopwatch_label.pack(pady=(50.50))

        # start
        self.start_button = tk.Button(self.main_frame, text="START", command=self.start ,bg="#fa8072", fg="#696969")
        self.start_button.pack(side="left", padx=(20,20))
        # stop
        self.stop_button = tk.Button(self.main_frame, text="STOP",command=self.stop,bg="#add8e6", fg="#696969")
        self.stop_button.pack(side="left", padx=(20,20))

        # reset
        self.reset_button = tk.Button(self.main_frame, text="RESET", command=self.reset, bg="#98fb98", fg="#696969")
        self.reset_button.pack(side="left", padx=(20,20))

    def update_time(self):
        # runningフラグが真なら実行
        if self.runningflag:
            #経過時刻を計算(現在時刻-startを押下した時刻+stopを押下するまでに経過していた時間)
            # 例: 現在時刻(120) - startを押下した時刻(80) + stopを押下するまでに経過していた時間(30)
            now = time.time() - self.start_time + self.elapsed_time

            #分ミリ秒整形
            # divmod は、「割り算の商」と「余り」を同時に出してくれる関数。
            mins, secs = divmod(now, 60)                                #今の時間を60で割って分と秒に分ける
            milli = int((secs - int(secs)) * 100)                       #ミリ秒を取り出す secs(小数点以下あり) - int(secs(小数点以下無し)で計算し、小数点以下のみの値を算出し下2桁を*100でint型とする
            time_str = f"{int(mins):02d}:{int(secs):02d}.{milli:02d}"   #02d ⇒2桁（2 digits）で表示して、足りない所は 0 で埋める。 分と秒とミリ秒の2桁の数字が1桁の数字だった場合、0で埋めた文字列とする
            self.stopwatch_label['text'] = time_str

            #10ミリ秒後に自分を呼び出す(このidを持っている限り、after処理を行う)
            self.after_id = self.main_frame.after(10, self.update_time)

    #startを押下してからの時刻を取得
    def start(self):
        if not self.runningflag:
            self.runningflag = True
            # 開始時刻を取得 > エポック（通常は1970年1月1日 00:00:00 UTC）からの経過時間を 浮動小数点数（float） で返却
            self.start_time = time.time()
            self.update_time()
            #トグルボタン(時刻を計測している間、ボタンを無効にする)
            self.toggle_buttons("running")

    #stopが押されるまでの時刻を取得、保持
    def stop(self):
        if self.runningflag:
            self.runningflag = False
            # stopを押下するまでの経過時間を取得
            # 今までの経過時間 + 現在の時間 - startボタン押下時間
            self.elapsed_time += time.time() - self.start_time

            #after_cancelで予約を取り消し、idを初期化(None)する
            if self.after_id:
                self.main_frame.after_cancel(self.after_id)
                self.after_id = None
            #トグルボタン(時刻を計測していない間、ボタンを無効にする)
            self.toggle_buttons("stopped")

    def reset(self):
        self.stop()
        self.elapsed_time = 0
        self.stopwatch_label['text'] = "00:00:00"
        self.toggle_buttons("reset")

    def toggle_buttons(self, state):
        #ボタンの切り替え
        if state == "running":
            self.start_button['state'] = "disabled"
            self.stop_button['state']="normal"
        elif state == "stopped" or state == "reset":
            self.start_button['state']="normal"
            self.stop_button['state']="disabled"


# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #TrainingAppのインスタンスを生成⇒initを実行(1回)
    app = StopwatchApp(root)
    #イベント待ちループ開始
    root.mainloop()

