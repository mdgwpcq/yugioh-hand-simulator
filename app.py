import streamlit as st
import random

st.title("遊戯王 妨害カード内訳ジェネレーター")

# --- 入力: 誘発カードリスト ---
st.header("① 妨害カードの設定")
num_cards = st.number_input("妨害カードの種類数 (p)", min_value=1, max_value=20, value=5)
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

st.markdown(f"✅ 妨害カードの合計枚数 (h): **{total_h}** 枚")
st.markdown(f"📦 残りの山札: **{40 - total_h}** 枚")

# --- モード選択: 手動 or ランダム ---
st.header("② 手札内の妨害カード枚数を決定")
mode = st.selectbox("モードを選択", ["手動で選ぶ", "ランダムにする (0～5枚)"])

if mode == "手動で選ぶ":
    q = st.slider("手札に含まれていた妨害カード枚数 (q)", 0, 5, 0)
else:
    if st.button("🎲 ルーレットを回す"):
        q = random.randint(0, 5)
        st.success(f"ランダムに選ばれた妨害カード枚数: **{q}** 枚")
    else:
        st.stop()  # ボタン押されるまで処理停止

# --- 実行: q枚をランダムに抽出 ---
st.header("③ 結果: 手札に含まれていた妨害カード")

if total_h == 0:
    st.warning("妨害カードが1枚も登録されていません。上で設定してください。")
else:
    deck = []
    for name, count in induced_cards:
        deck.extend([name] * count)

    if q > total_h:
        st.error("山札内の妨害カードの枚数より多く引くことはできません！")
    else:
        hand = random.sample(deck, k=q)
        st.subheader("🃏 手札に含まれていた妨害カード")
        for card in hand:
            st.markdown(f"- {card}")
