# Simple Tool Tkinter
## Tkinterを使用したシンプルなツール
Tkinterを使用したシンプルなツール達をまとめたリポジトリ

## 使用技術/環境/起動及び使用手順
- それぞれのディレクトリ下にそれぞれ記載  

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

simple_tool_tkinter/  
├counter  
└stopwatch  
└ .gitignore  
└ README.md  

</details>

# exe化方法(各フォルダ直下で実行)
■pyinstallerのインストール  
以下コマンドを実行  
pip install pyinstaller   

exe化の方法  
1.以下コマンドを実行  
pyinstaller main.py --onefile  --noconsole --icon=icon_01.ico

使用しそうなオプション  
--onefileは1つのファイルにまとめる  
--noconsoleはコンソールを表示しない  
--icon=test.icoはアイコンを変更(*.iconファイルを同一ディレクトリに配置する)  

2.作業ディレクトリ内にbuildディレクトリ/distディレクトリが作成される  
distディレクトリ内にあるmain.exeをダブルクリックで実行出来るようになっている(筈)  

3.エラーになった場合は  
コンソールからmain.exeを実行し、エラーを確認する(--noconsoleを設定していると出ない可能性あるので注意)  

# icon作成参考
https://qiita.com/Kosen-amai/items/4700100342c76f9fda78  
https://ao-system.net/alphaicon/  

## 備考
このリポジトリに含むプログラムは個人開発したものです。  