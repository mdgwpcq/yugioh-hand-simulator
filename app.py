import streamlit as st
import random
import time

st.title("遊戯王 妨害カード内訳ジェネレーター")

# 妨害カードの数を決定
num_cards = st.number_input("妨害カードの種類数 (p)", min_value=1, max_value=20, value=4)

card_names = []
card_counts = []

# 任意入力欄（カード名と採用枚数）
st.subheader("妨害カードの設定")
for i in range(num_cards):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"カード{i+1}の名前", key=f"name_{i}", value=f"カード{i+1}")
    with col2:
        count = st.number_input(f"採用枚数", min_value=0, max_value=3, key=f"count_{i}", value=1)
    card_names.append(name)
    card_counts.append(count)

# 合計
total_h = sum(card_counts)
st.markdown(f"**妨害カード合計枚数: {total_h} 枚**")

# 手札から引く妨害カード数
q = st.slider("手札に含まれていた妨害カード枚数 (q)", 0, 5, 1)

# 実行ボタン
if st.button("内訳をランダムに決定！"):
    st.markdown("### 内訳：")

    # 抽選処理（合計h枚中q枚を選ぶ）
    deck = []
    for name, count in zip(card_names, card_counts):
        deck.extend([name] * count)
    
    # シャッフルと抽選
    random.shuffle(deck)
    chosen = random.sample(deck, k=min(q, len(deck)))

    # 演出的ルーレット
    placeholder = st.empty()
    for _ in range(10):
        sample = random.sample(deck, k=min(q, len(deck)))
        placeholder.markdown("🎰 " + " / ".join(sample))
        time.sleep(0.1)

    # 最終結果
    placeholder.markdown("🎯 **" + " / ".join(chosen) + "**")

