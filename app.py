import streamlit as st
import random
from collections import Counter

st.title("遊戯王 妨害カード内訳ジェネレーター")

st.markdown("40枚デッキから初期手札5枚を引いたとき、妨害カードがq枚入っていた場合の内訳をランダム表示します。")

st.header("妨害カードの設定")

# 入力フォーム
bo_cards = {}
default_names = ["うらら", "G", "わらし", "うさぎ"]
for name in default_names:
    count = st.slider(f"{name} の採用枚数", 0, 3, 3 if name in ["うらら", "G"] else 1)
    if count > 0:
        bo_cards[name] = count

# 合計枚数の表示とチェック
h = sum(bo_cards.values())
st.write(f"妨害カード合計: {h} 枚")
if h > 40:
    st.error("妨害カードの合計が40枚を超えています。修正してください。")
    st.stop()

q = st.slider("手札に含まれていた妨害カード枚数（q）", 0, 5, 2)
