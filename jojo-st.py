import streamlit as st
import os
import openai
import unicodedata
from PIL import Image, ImageDraw, ImageFont

# Streamlitページ設定
st.set_page_config(page_title="HAGAKUREの奇妙な擬音", layout="centered")
st.title("HAGAKUREの奇妙な擬音")

# APIキー入力
api_key = st.text_input("OpenAI APIキーを入力してEnterキーを押してください:",type='password')

system_prompt = '''
##タスク:
 - あなたはユーザが与える{擬音にする動作}について漫画"ジョジョの奇妙な冒険"で表現される{芸術的でユニークな擬音}を生成します。
 - ユニークで芸術的な表現である必要があります。
 - 擬音を見てその場面がイメージできるありきたりな擬音は絶対にダメです。
##
参考にする例：
 - ズキュウウウン: ディオのエリナへの強引なキス。
 - メギャア: ディオによるジョナサンの顔への肘打ち。
 - イジケー: ジョースター家の使用人がいじける。
 - ルルバババ: スピードワゴンの帽子からカッターを投げる。
 - メメタア: ツェペリ男爵の波紋でカエルを殴る。
 - パパウパウパウ: ツェペリ男爵の波紋カッター。
 - キュイイイン: シュトロハイムの自白剤注射。
 - アッバーッ: サンタナに侵入されたドイツ兵。
 - ワムウッ！: ワムウがカーズとエシディシを目覚めさせる。
 - パウロオオオオオオ: 柱の男たちの相談時の風。
 - クッパァ: シーザーが柱の男たちに挑む。
 - オパウ！: ワムウの神砂嵐。
 - ルチャアア: ジョセフのエシディシへの波紋。
 - シャワアアア: カーズの館にシーザーが入る。
 - グッパオン: 承太郎が階段を転げる。
 - ドキューン: 承太郎の看護師へのキス。
 - ズズオウウン: サメがアンに忍び寄る。
 - ののおおーっ: 「イエローテンパランス」の正体現わし。
 - メギャン: ホル・ホースのスタンド登場。
 - ドッガウイーン: 「ホウィール・オブ・フォーチュン」の突進。
 - ドロドアオーッ: ホル・ホースのジープ逃走。
 - ドギタウ: 承太郎に化けたオインゴの反応。
 - ドリュウウーン: 仗助の「クレイジーダイヤモンド」使用。
 - ボムギ！: 康一のマウンテンバイク事故。
 - ズキーン: 山岸由花子と康一のキス。
 - バンギョン: 「ブラック・サバス」の移動。
 - カリシィーッ: ジョルノのポルポ暗殺。
 - ピッタアァーッ: ブチャラティの鍵操作。
 - スボサ！: 「ベイビィ・フェイス」のバイク融合。
 - ボニンンン: 「クラッシュ」の吹き飛び。
## 注意事項:
 - 擬音を見てその場面がイメージできるようなありきたりな擬音は絶対にダメです。
 - ユーザが与える{擬音にする動作}を基に{芸術的でユニークな擬音}のみ生成します。
 - それ以外の内容や文章は絶対に出力しません。
'''
# 半角文字に変換
def to_halfwidth_char(char):
    return unicodedata.normalize('NFKC', char)

# ひらがなをカタカナに変換
def hiragana_to_katakana(text):
    return "".join(
        chr(ord(char) + 96) if 'ぁ' <= char <= 'ゖ' else to_halfwidth_char(char)
        for char in text
    )

from PIL import Image, ImageDraw, ImageFont

def create_image(text):
    image_size = (800, 400)
    background_color = (255, 255, 255)
    font_path = 'JOJO-R.otf'
    first_char_font_size = 260
    rest_font_size = 100

    main_font = ImageFont.truetype(font_path, rest_font_size)
    first_char_font = ImageFont.truetype(font_path, first_char_font_size)

    dummy_image = Image.new('RGB', image_size, background_color)
    dummy_draw = ImageDraw.Draw(dummy_image)

    first_char_bbox = dummy_draw.textbbox((0, 0), text[0], font=first_char_font)
    rest_text_bbox = dummy_draw.textbbox((0, 0), text[1:], font=main_font)

    first_char_width = first_char_bbox[2] - first_char_bbox[0]
    first_char_height = first_char_bbox[3] - first_char_bbox[1]
    rest_text_width = rest_text_bbox[2] - rest_text_bbox[0]
    rest_text_height = rest_text_bbox[3] - rest_text_bbox[1]

    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)

    # テキストの垂直中央位置の計算
    total_height = max(first_char_height, rest_text_height)
    text_y = (image_size[1] - total_height) / 2

    # 一文字目と残りのテキストの垂直位置を中央揃えにする
    first_char_y = text_y + (total_height - first_char_height) / 2
    rest_text_y = text_y + (total_height - rest_text_height) / 2

    # テキストの水平位置の計算
    first_char_x = (image_size[0] - (first_char_width + rest_text_width)) / 2

    # テキストの描画
    draw.text((first_char_x, first_char_y), text[0], fill='black', font=first_char_font)
    rest_text_x = first_char_x + first_char_width
    draw.text((rest_text_x, rest_text_y), text[1:], fill='black', font=main_font)

    return image


if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    client = openai.OpenAI(api_key=api_key)
    
    # User message
    user_message = '擬音にする動作:'
    # ユーザー入力
    user_message += str(st.text_input("擬音にする動作やシチュエーションを入力してください: 例:プログラミングでエラーが解消されず頭を抱える"))

    # 開始ボタン
    if st.button("擬音を生成"):

        if user_message:
            full_message = user_message

            # チャットコンプリーションの生成
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_message}
            ]

            try:
                chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                # 応答を処理
                response_content = chat_completion.choices[0].message.content
                if ':' in response_content:
                    response_content = response_content.split(':')[0]

                # ひらがなをカタカナに変換
                response_content_katakana = hiragana_to_katakana(response_content)

                # 画像を生成
                image = create_image(response_content_katakana)
                st.image(image)
                st.write('生成された擬音: ' + response_content_katakana)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")