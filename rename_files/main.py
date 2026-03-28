import os
import tkinter as tk
from tkinter import filedialog, messagebox


class RenameFilesApp:
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
                
        self.root = root
        self.root.configure(bg="#233B6C")
        self.root.title("Rename Files App *.txt")
        self.root.geometry("800x400")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = tk.Frame(self.root, bg="#233B6C")
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
        file_menu.add_command(label="フォルダを選択", command=self.select_folder)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=root.quit)

        #変数宣言(エラーにならないように宣言)
        self.before_name = ""
        self.after_name = ""
        self.folder = None
        self.files = None
        self.preview_result = []

        # フォルダ選択を促すラベル
        self.folder_label = tk.Label(self.main_frame, text="対象フォルダ以下のファイルを一括で名前を変更します。",bg="#233B6C",fg="#ffffff")
        self.folder_label.pack()

        # リストボックス用のラベルとリストボックス自体の表示用フレーム
        self.about_frame = tk.Frame(self.main_frame,bg="#233B6C")
        self.about_frame.pack()

        # フォルダ選択を行うボタン
        self.folder_button = tk.Button(self.about_frame, text="フォルダを選択", command=self.select_folder)
        self.folder_button.pack(side="left",pady=(10,10),padx=(0,10))

        # ディレクトリのパス表示
        self.dir_path = tk.Label(self.about_frame, text="path:",bg="#233B6C",fg="#ffffff")
        self.dir_path.pack(side="left",pady=(10,10))


        # 変更前後の文字列入力欄のフレーム
        self.list_label_frame = tk.Frame(self.main_frame,bg="#233B6C")
        self.list_label_frame.pack()

        # 変更前ファイル名入力欄
        self.before_label = tk.Label(self.list_label_frame, text="変更前の文字列入力欄",bg="#233B6C",fg="#ffffff")
        self.before_label.pack(side="left", pady=(10,10),padx=(0,0))
        self.before_entry = tk.Entry(self.list_label_frame)
        self.before_entry.pack(side="left", pady=(10,10), padx=(20,50))

        # 変更前ファイル名入力欄
        self.after_label = tk.Label(self.list_label_frame, text="変更後の文字列入力欄",bg="#233B6C",fg="#ffffff")
        self.after_label.pack(side="left", pady=(10,10), padx=(50,20))
        self.after_entry = tk.Entry(self.list_label_frame)
        self.after_entry.pack(side="left", pady=(10,10), padx=(0,0))

        # リストボックス用のフレーム
        self.list_frame = tk.Frame(self.main_frame,bg="#233B6C")
        self.list_frame.pack()
        #履歴表示用リストボックス
        # ビフォー
        self.before_listbox = tk.Listbox(self.list_frame, width=50)
        self.before_listbox.pack(side="left",fill=tk.BOTH, expand=True, padx=10, pady=5)
        # ⇒
        self.arrow_label = tk.Label(self.list_frame, text="⇒",bg="#233B6C",fg="#ffffff")
        self.arrow_label.pack(side="left", padx=(5,5))
        # アフター
        self.after_listbox = tk.Listbox(self.list_frame, width=50)
        self.after_listbox.pack(side="left",fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ボタン用のフレーム
        self.button_frame = tk.Frame(self.main_frame,bg="#233B6C")
        self.button_frame.pack()

        # 対象件数表示ラベル
        self.rename_len_label = tk.Label(self.button_frame, text="リネーム対象はありません",bg="#233B6C",fg="#ffffff")
        self.rename_len_label.pack(pady=(20,20))

        # プレビューボタン
        self.preview_button = tk.Button(self.button_frame, text="プレビュー",command=self.preview)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # 実行ボタン
        self.execute_rename_button = tk.Button(self.button_frame, text="ファイル名一括変換実行",command=self.execute_rename)
        self.execute_rename_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = tk.Button(self.button_frame, text="選択/入力内容のクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))


    # フォルダを選択
    def select_folder(self):
        # フォルダを選択しなおしたとき等、画面上を一旦クリアする
        self.clear_data()

        self.folder = filedialog.askdirectory()
        print(self.folder)
        if not self.folder:
          messagebox.showerror("エラー","フォルダが選択されていません。")
          return

        # 画面にパスを表示 pathが長い時用に,anchor="w"の設定を追加
        self.dir_path.config(text=f"path:{self.folder}",anchor="w")

        self.files = os.listdir(self.folder)
        self.before_listbox.delete(0,tk.END)
        for f in self.files:
          self.before_listbox.insert(tk.END,f)

    # プレビュー
    # フォルダが選択されている時、プレビューボタンを押下することで変更後を表示する
    def preview(self):
        if not self.folder:
            messagebox.showerror("エラー","フォルダが選択されていません。")
            return

        # リネーム後、プレビューを押下されたとき用にもう一度、フォルダからファイルの状態を読み込む
        self.files = os.listdir(self.folder)
        self.before_listbox.delete(0,tk.END)
        for f in self.files:
          self.before_listbox.insert(tk.END,f)

        # 変更対象の文字列を取得
        self.before_name = self.before_entry.get()
        if self.before_name == "":
            messagebox.showwarning("警告","変更前の名前を入力してください。")
            return 
        
        # 変更後の文字列を取得
        self.after_name = self.after_entry.get()
        # 変更後は、単に単語を削除したい時があるので空欄を許容する
        # if self.after_name == "":
        #     messagebox.showwarning("警告","変更後の名前を入力してください。")
        #     return

        # listboxとプレビュー結果格納変数の初期化
        self.after_listbox.delete(0,tk.END)
        self.preview_result = []

        for f in self.files:
            self.preview_result.append((f,self.rename_preview(f)))
            self.after_listbox.insert(tk.END,self.rename_preview(f))
        
        # 変更対象が存在しない時、エラーメッセージを表示し、プレビューの結果を削除する
        preview_count = 0
        for old, new in self.preview_result:
            # 一つでもoldとnewの相違があれば、flagをTureとする
            if old != new:
                preview_count += 1

        # 上記で変更対象が見つからず、flagがfalseだった時、エラーメッセージを表示する
        if preview_count == 0:
            messagebox.showerror("エラー","変更対象が存在しません")
            self.after_listbox.delete(0,tk.END)
            self.preview_result = []

        # rename対象件数を表示
        self.rename_len_label.config(text=f"リネーム対象は{preview_count} 件です")

    # 名前変更
    def rename_preview(self,filename):
        # 処理確認用
        # print(f"ビフォーアフター:{self.before_name},{self.after_name}")
        # print(f"リプレイス:{filename.replace(self.before_name,self.after_name)}")
        return filename.replace(self.before_name,self.after_name)

    # ファイル名変換処理
    def execute_rename(self):
        try:
            # プレビューを実行していない場合、処理しない
            if not self.preview_result:
                messagebox.showwarning("エラー","プレビューを実行してください。")
                return

            # プレビュー状況との相違を確認
            # もしプレビューの状態と今の入力状況に相違がある場合、ファイル名変換処理はエラーとする
            if self.before_name != self.before_entry.get() or self.after_name != self.after_entry.get():
                # 簡易確認用
                # print("変更前:",self.before_name)
                # print("変更前:",self.before_entry.get())
                # print("変更後:",self.after_name)
                # print("変更後:",self.after_entry.get())
                messagebox.showwarning("エラー","プレビュー状況と入力状況が一致しません。")
                return 

            rename_flag = False
            for old,new in self.preview_result:
                #確認用
                #print(f"変換前:{old} ⇒変換後:,{new}")

                #一致していたら変換処理をする意味がないので処理対象外とする
                if old != new:
                    old_path = os.path.join(self.folder, old)
                    new_path = os.path.join(self.folder, new)
                    os.rename(old_path, new_path)
                    rename_flag = True
            if rename_flag:
                messagebox.showinfo("Successful","対象ファイルのリネームに成功しました。")
            else:
                messagebox.showerror("エラー","リネーム対象が存在しません")

        except Exception as e:
            messagebox.showerror(f"エラー",e)


    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.before_name = ""
        self.after_name = ""
        self.folder = None
        self.files = None

        # 画面に表示したパスをクリア
        self.dir_path.config(text="path:")

        #件数ラベルを初期化
        self.rename_len_label.config(text="リネーム対象はありません")

        # listboxの初期化
        self.before_entry.delete(0,tk.END)
        self.after_entry.delete(0,tk.END)
        self.before_listbox.delete(0,tk.END)
        self.after_listbox.delete(0,tk.END)
       
# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #TrainingAppのインスタンスを生成⇒initを実行(1回)
    app = RenameFilesApp(root)
    #イベント待ちループ開始
    root.mainloop()
