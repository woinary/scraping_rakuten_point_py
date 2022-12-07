from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from configparser import ConfigParser
import time
import csv
import os

# 楽天ポイントクラブ・ポイント実績URL
RAKUTEN_POINT_URL = 'https://point.rakuten.co.jp/history/?l-id=point_top_history_pc'

# 設定ファイル
CONFIG_FILE = '.config'

# 出力ファイルのエンコーディング
ENCODING = 'utf-8-sig'

# pythonファイルと同じディレクトリにchromeriver.exeがある場合引数は空でOK
driver = webdriver.Chrome()

# 楽天へのログイン
def login_rakuten():

    # 設定ファイルからパスワードを取得
    config = ConfigParser()
    config.read(CONFIG_FILE)
    section = 'RAKUTEN'

    print("ログインページ呼び出し")
    driver.get(RAKUTEN_POINT_URL)
    print("ログインページ表示")

    # chromedriver起動待ちを3秒似設定
    time.sleep(3)

    try:

        print("ログイン処理開始")
        # 楽天ポイントのログイン画面からIDフィールドを検索、IDを入力
        id = driver.find_element(By.ID, "loginInner_u")
        print("ID欄検索")
        # ↓自分のIDを入力
        id.send_keys(config.get(section, 'userid'))
        print("IDセット")

        # 同じくパスワードフィールドを検索、IDを入力
        password = driver.find_element(By.ID, "loginInner_p")
        print("パスワード欄検索")
        # ↓自分のパスワードを入力
        password.send_keys(config.get(section, 'password'))
        print("パスワードセット")

        time.sleep(1)

        # ログインボタンを検索、ログインボタンをクリック
        login_button = driver.find_element(By.NAME, "submit")
        login_button.click()
        print("ログイン実行")

    except Exception as e:
        print('Login Error')
        print('type:' + str(type(e)))
        print('args:' + str(e.args))
        print('message:' + e.message)
        print('e自身:' + str(e))
        return False

    print("ログイン処理完了")
    return True

### ポイント1件分の処理 ###
def get_point_info(pd, df, columns, post):
    try:
        # 日付
        date = post.find_element(By.CSS_SELECTOR, 'td.detail .date').text
        date = date.replace("[", "")
        date = date.replace("]", "")

        # サービス
        service = post.find_element(By.CSS_SELECTOR, '.service a').text

        # 内容
        detail = post.find_element(By.CSS_SELECTOR, 'td.detail').text

        # ランクアップ
        try:
            rankup = post.find_element(By.CSS_SELECTOR, '.label-rankup').text
            detail = detail.replace('ランクアップ対象', '').strip()

        except:
            rankup = "-"

        # アクション、期間限定
        action = post.find_element(By.CSS_SELECTOR, '.action').text
        limited = "-"
        if action == "獲得\n期間限定":
            action = "獲得"
            limited = "期間限定"

        # ポイント
        point = post.find_element(By.CSS_SELECTOR, '.point').text
        point = point.replace(',','')
        # point = int(point.replace(',','')) * -1

        # 備考
        note = post.find_element(By.CSS_SELECTOR, '.note').text
        if len(note) < 1:
            note = "-"

        # 連番列を設定
        no = len(df.index) + 1

        # スクレイピングした情報をリストに追加
        se = pd.Series([no, date, service, detail, rankup, action, limited, point, note], columns)
        df = pd.concat([df, pd.DataFrame([se])], ignore_index=True)

        print("1件完了(" + str(no) + "):" + date + ": " + point)

    except Exception as e:
        print('Proc Error')
        print('type:' + str(type(e)))
        print('args:' + str(e.args))
        print('message:' + e.message)
        print('e自身:' + str(e))

    return df

### 次ページを取得 ###
def get_next_page(page):
    try:
        # 次のページに進むためのURLを取得
        confirm_page = driver.find_element(By.CSS_SELECTOR, "ul.pagination li:last-child a").text
        url = driver.find_element(By.CSS_SELECTOR, "ul.pagination li:last-child a").get_attribute("href")

        time.sleep(3)
        print(str(page) + "ページを取得中．．．")
        driver.get(url)
        time.sleep(1)
    except:
        print("最終ページ")

    return confirm_page

### ポイント情報の取得 ###
def get_r_info():

    # 表示ページの定義
    page = 1
    confirm_page = 'NEXT'

    # リストを作成
    columns = ['No', '日付', 'サービス', '内容', 'ランクアップ対象', '利用／獲得', '期間限定', 'ポイント', '備考']

    # 配列名を指定する
    df = pd.DataFrame(columns=columns)

    # 実行
    while(str(confirm_page) == 'NEXT'):

        # ポイントの獲得情報を取得
        print("ポイント獲得情報取得")
        posts = driver.find_elements(By.CSS_SELECTOR, '.get')

        for post in posts:
            df = get_point_info(pd, df, columns, post)
        print("獲得情報群取得完了")

        # ポイントの利用情報を取得
        print("ポイント利用情報取得")
        posts = driver.find_elements(By.CSS_SELECTOR, '.use')

        for post in posts:
            df = get_point_info(pd, df, columns, post)
        print("利用情報取得完了")

        print("ページ遷移処理開始")
        # ページ数を1増やす
        page += 1

        # デバッグモードでは2ページで強制終了
        global debug_mode
        if debug_mode:
            if page > 2:
                print("デバッグモードのため強制終了")
                break

        # 次ページを取得
        confirm_page =  get_next_page(page)

    return df

### データの書き出し ###
def write_point_data(df):
    # 最後に得たデータをCSVにして保存
    filename = "rakuten_point.csv"
    df.to_csv("csv/" + filename, encoding=ENCODING, index=False)
    print("終了しました！！")

### メイン ###

# デフォルト値
default_configs = {'DEBUG': { 'debug' : 'no'}}

# DEBUGモード
debug_mode = False
config = ConfigParser()
config.read_dict(default_configs)
config.read(CONFIG_FILE)

# メイン処理
if config.get('DEBUG', 'debug') == 'yes':
    print("DEBUGモード")
    debug_mode = True

if login_rakuten():
    df = get_r_info()
    if not df.empty:
        write_point_data(df)