import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox


class ExtensionSortApp:
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, root):
                
        self.root = root
        self.root.configure(bg="#233B6C")
        self.root.title("Extension Sort App")
        self.root.geometry("800x500")

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
        file_menu.add_command(label="終了", command=root.quit)

        #変数宣言(エラーにならないように宣言)
        self.folder = None
        self.files = None
        self.preview_result = []
        self.error_result = []
        self.ext_count = {}
        self.ext_flag = False


        # フォルダ選択を促すラベル
        self.folder_label = tk.Label(self.main_frame, text="対象フォルダ以下のファイルを拡張子毎のフォルダに振り分けます。",bg="#233B6C",fg="#ffffff")
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
        self.target_len_label = tk.Label(self.button_frame, text="対象はありません",bg="#233B6C",fg="#ffffff")
        self.target_len_label.pack(pady=(20,20))

        # プレビューボタン
        self.preview_button = tk.Button(self.button_frame, text="振り分けプレビュー",command=self.preview)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # 実行ボタン
        self.execute_extension_button = tk.Button(self.button_frame, text="拡張子別振り分け実行",command=self.execute_extension)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = tk.Button(self.button_frame, text="フォルダ選択のクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))


    # フォルダを選択
    def select_folder(self):
        # フォルダを選択しなおしたとき等、画面上を一旦クリアする
        self.clear_data()

        self.folder = filedialog.askdirectory()
        # 確認用
        # print(self.folder)
        if not self.folder:
          messagebox.showerror("エラー","フォルダが選択されていません。")
          return

        # 画面にパスを表示 pathが長い時用に,anchor="w"の設定を追加
        self.dir_path.config(text=f"path:{self.folder}",anchor="w")

        # ファイルの一覧を取得
        self.files = os.listdir(self.folder)
        # listboxの既存情報を削除
        self.before_listbox.delete(0,tk.END)
        # listboxにファイル情報をインサート
        for f in self.files:
          self.before_listbox.insert(tk.END,f)

        #プレビュー押下を促す表示
        self.target_len_label.config(text="プレビューを実行してください")

    # プレビュー
    # フォルダが選択されている時、プレビューボタンを押下することで変更後を表示する
    def preview(self):
        # 実行フラグをfalseにしておく
        self.ext_flag = False

        if not self.folder:
            messagebox.showerror("エラー","フォルダが選択されていません。")
            return
        
        # カウント用変数の初期化
        self.ext_count = {}

        # リネーム後、プレビューを押下されたとき用にもう一度、フォルダからファイルの状態を読み込む
        self.files = os.listdir(self.folder)
        self.before_listbox.delete(0,tk.END)
        for f in self.files:
          self.before_listbox.insert(tk.END,f)

        # ディレクトリ情報
        # print("test",self.folder)
        
        # listboxとプレビュー結果格納変数の初期化
        self.after_listbox.delete(0,tk.END)
        self.preview_result = []
        preview_flag = False
        for f in self.files:
            # ファイル名とディレクトリ名(ファイルの場合は空)をresultに格納
            ext = self.extension_sort_preview(f)
            self.preview_result.append((f,ext))
            # ""じゃなければディレクトリ名と結合して表示
            if ext != "":
                self.after_listbox.insert(tk.END,f"{f}/{ext}")
                preview_flag = True
            else:
                self.after_listbox.insert(tk.END,f"{f}")
        
        # 変更対象が存在しない時、エラーメッセージを表示し、プレビューの結果を削除する
        if not preview_flag:
            messagebox.showerror("エラー","変更対象が存在しません")
            self.after_listbox.delete(0,tk.END)
            self.preview_result = []

        # 対象件数を表示
        # dict型にitems()を付け加えることでkeyとvalueのどちらも取得可能にする →self.ext_count.items()
        text = ""
        for ext, count in sorted(self.ext_count.items()):
            text += f"\n{ext}: {count}件"
        self.target_len_label.config(text=f"以下振り分け対象です{text}")


    # 拡張子ごとに振り分け
    def extension_sort_preview(self,filename):
        # フォルダは対象外
        if not os.path.isfile(f"{self.folder}/{filename}"):
            return ""

        # 拡張子抜きの名前と拡張子を取り出す
        # name, ext = os.path.splitext(filename)

        # 拡張子だけ取り出す
        ext = os.path.splitext(filename)[1]

        # 上記取得の拡張子の小文字を消し(lower)、.を消す(replace)という処理
        ext = ext.lower().replace(".", "")

        # 拡張子がない場合、not_extとしフォルダを作らせる
        if ext == "":
            ext = "not_ext"

        # カウント処理
        # dict型の変数の中にext(拡張子)が含まれているかを確認
        if ext in self.ext_count:
           self.ext_count[ext] += 1
        else:
            self.ext_count[ext] = 1
        # 確認用
        # print("カウント処理:",self.ext_count) 

        # 新しいパスとディレクトリ名を返却
        return ext
       
    # 拡張子ごとに振り分け、振り分け先フォルダがない場合作成
    def execute_extension(self):
        try:
            # プレビューを実行していない場合、処理しない
            if not self.preview_result:
                messagebox.showwarning("エラー","プレビューを実行してください。")
                return

            # extフラグがTureなら処理実行済みの警告を表示し、処理しない
            if self.ext_flag:
                messagebox.showwarning("警告","処理実行済みフォルダです。")
                return


            self.ext_flag = False
            for filename, ext in self.preview_result:

                #ext(拡張子名)が""なら処理しない
                if ext != "":
                    # ディレクトリがなければ作成
                    if not os.path.exists(f"{self.folder}/{ext}"):
                        os.mkdir(f"{self.folder}/{ext}")

                    # 新旧のフルパスを作成
                    old_path = os.path.join(self.folder, filename)
                    new_path = os.path.join(self.folder, f"{ext}/{filename}")
                    # ファイル名をnew_pathに変える
                    # os.renameは対象ディレクトリに同じ名前のファイルがある場合エラーになる(windows限定、MacOS及びLinaxでは上書きされる)
                    # そのため既存ファイルがある場合処理せず、error_resultでエラー表示する
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        # 強制的に上書きする処理
                        # os.replace(old_path, new_path)
                        self.ext_flag = True
                    else:
                        self.error_result.append((filename, ext))

            # 振り分け先に同じ名前のファイルがあった時のエラーメッセージを生成
            text = ""
            if self.error_result:
                for error_path, ext in self.error_result:
                    text += f"\n{error_path}"
                    
            # 処理実行flag及び上記でエラー/警告用のtextが作られていないかをチェック
            if self.ext_flag and text == "":
                messagebox.showinfo("Successful","対象フォルダ下にあるファイルを拡張子毎のフォルダに格納しました。")
            elif self.ext_flag and text != "":
                messagebox.showwarning("Partial Successful", f"フォルダ内に同一名称のファイルがあるため一部処理が実行できませんでした。{text}")
            elif not self.ext_flag and text != "":
                messagebox.showerror("エラー", f"フォルダ内に同一名称のファイルがあるため処理が実行できませんでした。{text}")
            else:
                messagebox.showerror("エラー","フォルダ下に対象が存在しません")
        
        except Exception as e:
            messagebox.showerror("エラー",e)

    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.folder = None
        self.files = None

        # プレビュー時に初期化されているが、一応こちらでも初期化
        self.preview_result = []
        self.error_result = []
        self.ext_count = {}
        self.ext_flag = False

        # 画面に表示したパスをクリア
        self.dir_path.config(text="path:")

        #件数ラベルを初期化
        self.target_len_label.config(text="対象はありません")

        # listboxの初期化
        self.before_listbox.delete(0,tk.END)
        self.after_listbox.delete(0,tk.END)
       
# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #ウィンドウを作る
    root = tk.Tk()
    #TrainingAppのインスタンスを生成⇒initを実行(1回)
    app = ExtensionSortApp(root)
    #イベント待ちループ開始
    root.mainloop()
