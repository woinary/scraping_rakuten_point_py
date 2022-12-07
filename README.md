# 楽天ポイントクラブのポイント実績をCSV出力する

## 概要

楽天ポイントクラブのポイント実績ページの内容を取得して、CSVファイルに出力します。

## 使い方

適当なフォルダにpythonファイルを置いて実行してください。本体は「scraping_rakuten_point.py」です。引数は不要です。

楽天のID、パスワードを記載した設定ファイル（.config）が必要ですので、先に作っておいてください。

```:
[RAKUTEN]
userid = 自分の楽天ID
password = 自分の楽天パスワード
```

添付のmakeconfig.pyを実行することで雛形を作成できますが、テキストエディタで書いたほうが早いでしょう。

そのフォルダにcsvフォルダを作っておかないと出力時にエラーになります。
chromedriverも同じところにおいてください。適宜、ライブラリのインストールも必要です。

## 前提条件

使用するには以下のものが必要です。

* Python3
* 以下のライブラリ
  * Selenium
  * Pandas
  * ConfigParser
* Chrome Driver

## 注意事項

* 過度なアクセスで楽天のサーバに負荷をかけないようにしてください

## 免責事項

動作確認はしていますが、不具合がある可能性もあります。本スクリプトの使用によって不利益が生じた場合も作成者は一切の補償はできません。
そのため同意できない場合や内容を理解できない場合は実行しないでください。
また、ソースの改変についても一切自由ですが、同様に改変内容かオリジナルのままかによらず保証も保証もできませんので、自身の責任と判断で行なってください。

## 動作確認

Apple Silicon搭載MacBook(macOS Ventura 13.0.1)で確認しています。

## 参考

以下サイトのプログラムを参考にさせていただきました。
ただし、使っているライブラリのバージョンの都合でエラーや警告が出てきたため、アップデート内容に合わせてプログラムを修正しています。
さらに、そのついでで構成からかなりいじっているので、半分くらいは書き直しています。

[Pythonで自動化してみよう！　～楽天ポイントの明細をスクレイピングでダウンロードしてみる～](https://massu-keiei.com/python_automation_rakuten_point/)

### オリジナルからの変更点

* 出力内容の変更
  * 利用ポイントを負数にしていたのを廃止（データ取得処理統合のため）
  * 期間限定ポイントの列を独立（自分の集計の都合上）
  * ランクアップ対象外の場合の出力を「-」に変更（自分の集計の都合上）
  * 内容欄の「ランクアップ対象」表記を削除
  * 内容欄のトリム処理を追加
  * 備考欄が空欄だった場合に「-」を出力（自分の集計の都合上）
  * 出力ファイルの見出しを日本語文字列に修正
  * 出力ファイルの各行左端のインデックスを1オリジンに変更
* ライブラリのエラー、警告対応
  * Seleniumのfind_element_by_...系メソッド廃止による修正
  * Pandaのappendメソッドが非推奨になったことによる修正
* 内部処理の変更
  * モジュール分けを細かくしてモジュール構成を変更
  * 楽天のID、パスワードは設定ファイルに記載するように変更
  * try〜exceptで囲む範囲を狭く変更
  * 進捗状況確認用に出力メッセージを大幅追加
  * page変数とcount変数が同じ内容のようなのでpageへ統合
  * 使われていないmarket,product変数を削除
  * ハードコーディングされていた楽天ポイントのURLを定数に別出し
  * 出力ファイルの文字エンコーディングを定数に別出し
  * 次ページ取得タイミングを変更（ページ処理の先頭から末尾へ移動）

## 履歴

* 2022/12/07 初版