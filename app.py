import streamlit as st
import random
import numpy as np

st.title("遊戯王 妨害カード内訳ジェネレーター")

# --- 妨害カード設定 ---
st.header("① 妨害カードの設定")
num_cards = st.number_input("妨害カードの種類数 (p)", min_value=1, max_value=20, value=4)
induced_cards = []
total_h = 0

for i in range(num_cards):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"カード{i+1}の名前", key=f"name_{i}")
    with col2:
        count = st.slider(f"採用枚数 (最大3枚)", 0, 3, 1, key=f"count_{i}")
    if name:
        induced_cards.append((name, count))
        total_h += count

# --- デッキ枚数（自由に設定可能） ---
st.header("② デッキの設定")
deck_size = st.slider("相手のデッキ枚数", min_value=30, max_value=60, value=40)
non_induced = deck_size - total_h
st.markdown(f"✅ 妨害カードの合計枚数 (h): **{total_h}** 枚")
st.markdown(f"📦 妨害以外のカード枚数: **{non_induced}** 枚")

# --- モード選択（手動 or ランダム with 正規分布）---
st.header("③ 手札に含まれる妨害カードの枚数を選ぶ")
mode = st.radio("手札の妨害カード枚数をどう決める？", ["手動で選ぶ", "ランダムに決める（正規分布）"])
manual_q = 0
if mode == "手動で選ぶ":
    manual_q = st.slider("手札に含まれる妨害カード枚数 (q)", 0, 5, 0)
else:
    if st.button("🎲 ランダムに選ぶ（正規分布）"):
        # 正規分布によるサンプリング
        hand_size = 5
        ratio = total_h / deck_size if deck_size > 0 else 0
        mean = hand_size * ratio
        std_dev = 1.0  # 標準偏差（調整可）
        q_dist = int(round(np.random.normal(loc=mean, scale=std_dev)))
        manual_q = max(0, min(5, q_dist))  # 0〜5にクリップ
        st.success(f"ランダムに選ばれた妨害カード枚数: **{manual_q}** 枚")
    else:
        st.stop()

# --- 結果表示 ---
st.header("④ 結果: 手札に含まれていた妨害カード")

if total_h == 0:
    st.warning("妨害カードが1枚も登録されていません。上で設定してください。")
else:
    deck = []
    for name, count in induced_cards:
        deck.extend([name] * count)

    if manual_q > total_h:
        st.error("山札内の妨害カードの枚数より多く引くことはできません！")
    else:
        hand = random.sample(deck, k=manual_q) if manual_q > 0 else []
        st.subheader("🃏 手札に含まれていた妨害カード")
        if hand:
            for card in hand:
                st.markdown(f"- {card}")
        else:
            st.markdown("*妨害カードは手札に含まれていません。*")
