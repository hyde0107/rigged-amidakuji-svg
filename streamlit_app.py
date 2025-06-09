import streamlit as st
import random

N = 6
participants = [f"参加者{i+1}" for i in range(N)]
default_goals = [f"ゴール{i+1}" for i in range(N)]

def generate_ladders(n, max_lines=10):
    ladders = []
    for _ in range(max_lines):
        pos = random.randint(0, n-2)
        height = random.random()
        ladders.append((pos, height))
    ladders.sort(key=lambda x: x[1])
    return ladders

def traverse(start_idx, ladders, n):
    pos = start_idx
    for (line_pos, _) in ladders:
        if pos == line_pos:
            pos += 1
        elif pos == line_pos + 1:
            pos -= 1
    return pos

st.title("シンプルあみだくじ")

# 参加者選択
start_selection = []
for i in range(N):
    sel = st.selectbox(f"スタート位置{i+1}の参加者を選択", participants, key=f"start_{i}")
    start_selection.append(sel)

ladders = generate_ladders(N)
st.write("横線一覧 (縦線間の位置と高さ):")
for (pos, height) in ladders:
    st.write(f"{pos} と {pos+1} の間、高さ {height:.2f}")

# あみだくじ経路計算
goal_positions = [traverse(i, ladders, N) for i in range(N)]

# 【ここだけあなたが書き換えてください】
# スタートインデックス -> ゴール結果の対応を自由に設定できるように
# 例：0番スタートは"ゴールA", 1番スタートは"ゴールB" ... みたいに
goal_mapping = {
    0: "ゴールX",
    1: "ゴールY",
    2: "ゴールZ",
    3: "ゴールW",
    4: "ゴールV",
    5: "ゴールU",
}

if st.button("結果を見る"):
    st.write("=== あみだくじの結果 ===")
    for i, part in enumerate(start_selection):
        final_pos = goal_positions[i]
        # goal_mappingが設定されていればそちらを使う。なければdefault_goalsから
        goal_result = goal_mapping.get(final_pos, default_goals[final_pos])
        st.write(f"{part} → {goal_result}")
