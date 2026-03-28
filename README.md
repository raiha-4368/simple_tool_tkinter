# Simple Tool Tkinter
## Tkinterを使用したシンプルなツール
Tkinterを使用したシンプルなツール達をまとめたリポジトリ

## 使用技術/環境/起動及び使用手順
- それぞれのディレクトリ下にそれぞれ記載  

## Tools
- counter  
 数をカウントするシンプルなツール  
- stopwatch  
 start/stop/resetができるストップウォッチ  
 - contdown  
 時間を設定し、0になるまで時間を計測するツール    

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

simple_tool_tkinter/  
├contdown  
├counter  
├csv_viewer  
├memo  
└pomodoro_timer  
└rename_files  
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

icon作成時の画像  
ぼやける理由⇒.icoは複数サイズを持つ必要がある(16*16, 32*32, 48*48,128*128, '256*256'←最重要)
256*256で作成  
その他の無料ツール候補
icoFX(軽い)
favicon generator系(複数サイズ同時生成)


## 備考
このリポジトリに含むプログラムは個人開発したものです。  

## memo
作るツール案
・TODOリスト  
・DBファイルビューア  
候補4!!!・ポモドーロv2(ポモドーロ周期変更、一時停止、再開処理を追加)  
候補1!!!・csv整形(空白削除、列幅・改行整理)  
候補2!!!・csv差分表示  
・ファイル加工系  
候補3!!!・ファイル整理系  
・ファイル名＿連番付与ツール  
・拡張子ごとに自動振り分け  
・ログビューア  
・巨大テキスト高速表示  
・特定文字列抽出ツール  
・改行コード一発変換  
・全角半角変換  
・日付フォーマット変換  


■売れるか判断する基準  
作る前にこれチェック  
・手作業だと面倒か？  
・毎回やる作業か？  
・10秒以上短縮できるか？  
 2つ以上YESなら当たり候補  
