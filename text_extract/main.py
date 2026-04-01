import os
import unicodedata
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox


class TextExtractApp:
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
                
        self.root = root
        self.root.configure(bg="#191919")
        self.root.title("Text Extract App")
        self.root.geometry("1500x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = tk.Frame(self.root, bg="#191919")
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

        #変数宣言(エラーにならないように宣言)
        self.filepaht = ""
        self.exact_match_flag = False
        self.result = []

        # フォルダ選択を促すラベル
        self.folder_label = tk.Label(self.main_frame, text="選択されたファイル内から検索文字列を含む行を探します",bg="#191919",fg="#ffffff")
        self.folder_label.pack()

        # ***************************************************************************************************
        # about_frame
        # リストボックス用のラベルとリストボックス自体の表示用フレーム
        self.about_frame = tk.Frame(self.main_frame,bg="#191919")
        self.about_frame.pack()

        # ファイルを行うボタン
        self.file_button = tk.Button(self.about_frame, text="ファイルを選択", command=self.select_file)
        self.file_button.pack(side="left",pady=(10,10),padx=(0,10))

        # ディレクトリのパス表示
        self.dir_path = tk.Label(self.about_frame, text="path:",bg="#191919",fg="#ffffff")
        self.dir_path.pack(side="left",pady=(10,10))
        # ***************************************************************************************************

        # ***************************************************************************************************
        # search_frame
        # 検索文字列入力フレーム
        self.search_frame = tk.Frame(self.main_frame, bg="#191919")
        self.search_frame.pack()

        # 検索文字列の入力ラベル
        self.search_word_label = tk.Label(self.search_frame, text="検索文字列入力")
        self.search_word_label.pack(side="left", pady=(20,20),padx=(20,20))
        # 検索文字列入力欄
        self.search_word = tk.Entry(self.search_frame)
        self.search_word.pack(side="left", pady=(20,20),padx=(20,20))

        # チェックボックスの状態を保持する変数
        self.chk_exact_match_state = tk.BooleanVar()
        # 完全一致のチェック
        self.chk_exact_match = tk.Checkbutton(self.search_frame,
                                                    text="完全一致で検索する場合はチェックを入れてください",
                                                    variable=self.chk_exact_match_state,
                                                    selectcolor="#313131",
                                                    bg="#191919",
                                                    fg="#ffffff")
        self.chk_exact_match.pack(pady=10)

        # 大文字小文字を区別するかのチェック
        self.chk_is_case_sensitive_state = tk.BooleanVar()     
        self.chk_is_case_sensitive = tk.Checkbutton(self.search_frame,
                                                    text="大文字小文字を区別しない場合はチェックを入れてください",
                                                    variable=self.chk_is_case_sensitive_state,
                                                    selectcolor="#313131",
                                                    bg="#191919",
                                                    fg="#ffffff")
        self.chk_is_case_sensitive.pack(pady=10)

        # ***************************************************************************************************

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.text_area_frame = tk.Frame(self.main_frame, bg="#191919")
        self.text_area_frame.pack()

        # テキストエリア
        self.text_area_before = tk.Text(self.text_area_frame,state='disabled')
        self.text_area_before.pack(side="left", pady=(20,20),padx=(20,20))
        # テキストエリアの大きさ調整の為コメントアウト。後でpack(width=50, height=50,expand=True, fill="both")
        # ⇒
        self.arrow_label = tk.Label(self.text_area_frame, text="⇒",bg="#191919",fg="#ffffff")
        self.arrow_label.pack(side="left", padx=(5,5))
        # 検索結果
        self.text_area_after = tk.Text(self.text_area_frame)
        self.text_area_after.pack(side="left", pady=(20,20),padx=(20,20))
        # テキストエリアの大きさ調整の為コメントアウト。後でpack(width=50, height=50, expand=True, fill="both")
        # ***************************************************************************************************
        
        # ***************************************************************************************************
        # button_frame
        # ボタン用のフレーム
        self.button_frame = tk.Frame(self.main_frame,bg="#191919")
        self.button_frame.pack()

        # 対象ファイルから検索文字列を含む行を抜き出す
        self.preview_button = tk.Button(self.button_frame, text="検索開始",command=self.read_line_file)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # ファイルへ出力
        self.execute_extension_button = tk.Button(self.button_frame, text="ファイルへ出力",command=self.output_file)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = tk.Button(self.button_frame, text="ファイル/テキストエリアのクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))
        # ***************************************************************************************************

    # ファイルを開く
    def select_file(self):

        # 今までの入力値をクリア
        self.clear_data()

        self.filepath = filedialog.askopenfilename(
          defaultextension=".txt",
          filetypes=[("All files", "*.*")],
          title="ファイルを開く"
      )
        if self.filepath:
            try:
                with open(self.filepath, mode='r', encoding="utf-8") as f:
                    content = f.read()
                    # print(content)
                    # テキストエリアを一度空にしてから読み込んだ内容を挿入
                    self.text_area_before.config(state="normal")
                    self.text_area_before.delete("1.0", "end") #1行目から最後まで削除
                    self.text_area_before.insert("1.0", content) #1行目に挿入
                    self.text_area_before.config(state="disabled")

                # オプション 今開いているファイル名をタイトルに表示
                self.root.title(f"Text Extract App - {self.filepath}")

                # selfにファイルパスを持たせておく
                self.dir_path.config(text=self.filepath)

            except Exception as e:
                  messagebox.showerror("エラー",e)

    
    # ファイルを一行ずつ読み込み、検索文字列業を抜き出す
    def read_line_file(self):
        # resultを初期化
        self.result = []

        # 検索対象文字列の有無を確認。入力されていないならエラー
        self.get_word = self.search_word.get()

        if self.get_word == "":
            messagebox.showerror("エラー","検索対象文字が入力されていません。")
            return

        # 読み込みモードr
        with open(self.filepath, 'r',encoding='utf-8') as f:
            # 新しい処理
            for i, line in enumerate(f, start=1):
                # 大文字小文字を区別するかのチェックボックスを確認
                if self.chk_is_case_sensitive_state.get():
                    # 区別しない場合、全て小文字にして確認
                    self.get_word = self.get_word.lower()
                    self.line_search(i,line.strip().lower())
                else:
                    self.line_search(i,line.strip())

        # ファイルの読み込み終了後
        # テキストエリアを書き込める状態にし、既存内容を削除
        self.text_area_after.config(state="normal")
        self.text_area_after.delete("1.0", "end") #1行目から最後まで削除    
        # 検索結果があればテキストエリアにインサート
        if self.result:
            insert_num = 0
            for r in self.result:
                insert_num += 1
                self.text_area_after.insert(f"{insert_num}.0", f"{r[2]}\n")
        else:
            messagebox.showerror("エラー","検索文字との一致が見つけられませんでした。")
        # 処理が終わったらテキストエリアの書き込めない状態にする
        self.text_area_after.config(state="disabled")


    # 一列受け取って、文字列を含むかどうかの判定
    def line_search(self, num, line):
        # 完全一致のチェックボックスがチェックされているか確認
        if self.chk_exact_match_state.get():
            # 完全一致の場合
            if self.get_word == line:
                self.result.append((self.filepath, num, line))
        else:
            # 部分一致の場合
            if self.get_word in line:
                self.result.append((self.filepath, num, line))

    # 検索結果をファイルへ書き込み
    def output_file(self):
        try:
            # text_areaの情報を取得
            # "end-1c"で余計な改行を削除
            content = self.text_area_after.get("1.0", "end-1c")
            print(f"コンテンツ:{content}")
            
            # 検索を行っていない場合、処理しない
            if not content:
                messagebox.showwarning("エラー","検索を実行してください。")
                return

            # 時刻取得
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filepath = filedialog.asksaveasfilename(
                defaultextension = ".csc",
                initialfile=f"{self.get_word}_{date}.csv", 
                filetypes=[("csv files", "*.csv")],
                title="textファイルを保存"
                )
            if filepath:
                # カラム行作成
                column = ["filepath","line_num","content"]

            #新規書き込みw,追記モードaで使い分け
                with open(filepath, mode='w', newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    # ヘッダー書き込み
                    writer.writerow(column)
                    # resultの書き込み
                    for row in self.result:
                        writer.writerow(row)

        except Exception as e:
            messagebox.showerror("エラー",e)

       
    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.filepaht = ""
        self.exact_match_flag = False
        self.result = []

        # 画面に表示したパスをクリア
        self.dir_path.config(text="path:")

        # 検索対象文字列をクリア
        self.search_word.delete(0, tk.END)

        # チェックボックスを初期化
        self.chk_exact_match_state.set(False)
        self.chk_is_case_sensitive_state.set(False)

        # textareaの初期化
        self.text_area_before.config(state="normal")
        self.text_area_before.delete("1.0", "end") #1行目から最後まで削除
        self.text_area_before.config(state="disabled")
        self.text_area_after.config(state="normal")
        self.text_area_after.delete("1.0", "end") #1行目から最後まで削除
        self.text_area_after.config(state="disabled")

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #TextExtractAppのインスタンスを生成⇒initを実行(1回)
    app = TextExtractApp(root)
    #イベント待ちループ開始
    root.mainloop()
