import streamlit as st
import random
import numpy as np

st.set_page_config(page_title="遊戯王 妨害カード内訳ジェネレーター", layout="centered")
st.title("🃏 妨害カード内訳ジェネレーター")

st.header("① 妨害カードの設定")
num_cards = st.number_input("妨害カードの種類数 (p)", min_value=1, max_value=20, value=4)

induced_cards = []
total_h = 0

for i in range(num_cards):
    cols = st.columns([2, 1])
    with cols[0]:
        name = st.text_input(f"カード{i+1}の名前", key=f"name_{i}")
    with cols[1]:
        count = st.number_input("採用枚数", min_value=0, max_value=3, value=1, step=1, key=f"count_{i}")
    if name:
        induced_cards.append((name, count))
        total_h += count

st.divider()

st.header("② デッキの設定")
col_deck_label, col_deck_input = st.columns([2, 1])
with col_deck_label:
    st.markdown("#### 相手のデッキ枚数")
with col_deck_input:
    deck_size = st.number_input("", min_value=30, max_value=60, value=40, step=1)

non_induced_count = deck_size - total_h

st.divider()

st.header("③ 手札の妨害カード枚数の選択")
mode = st.radio("モード選択", ["手動で選択", "ランダムで選択（分布に基づく）"])

if mode == "手動で選択":
    q = st.number_input("手札に含まれる妨害カード枚数 (q)", min_value=0, max_value=5, value=1, step=1)
else:
    mu = total_h / deck_size * 5
    sigma = 0.8  # 分布の広がり調整（必要に応じて変更）
    q = int(np.clip(np.random.normal(loc=mu, scale=sigma), 0, 5))
    st.markdown(f"🎲 ランダム選択結果: **{q}枚** の妨害カードが手札に含まれます")

st.divider()

if st.button("🎯 妨害カードを確認！"):
    card_pool = []
    for name, count in induced_cards:
        card_pool.extend([name] * count)

    if q > len(card_pool):
        st.error("指定された枚数の妨害カードをデッキから引くことができません。")
    else:
        drawn = random.sample(card_pool, q)
        st.success(f"手札の妨害カード内訳（{q}枚中）:")
        st.write("・" + "\n・".join(drawn))
