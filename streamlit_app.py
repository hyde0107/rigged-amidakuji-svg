import streamlit as st
import streamlit.components.v1 as components
import random

# --------------------------
# 設定
# --------------------------

NUM_COLS = 18
NUM_ROWS = 12
WIDTH = 900
HEIGHT = 600
COLUMN_SPACING = WIDTH / (NUM_COLS - 1)
ROW_SPACING = HEIGHT / NUM_ROWS

# 不正なゴールマッピング（自由に設定可能）
GOAL_MAP = {
    "1": "⑱",
    "2": "⑰",
    "3": "①",
    "4": "②",
    "5": "③",
    "6": "④",
    "7": "⑤",
    "8": "⑥",
    "9": "⑦",
    "10": "⑧",
    "11": "⑨",
    "12": "⑩",
    "13": "⑪",
    "14": "⑫",
    "15": "⑬",
    "16": "⑭",
    "17": "⑮",
    "18": "⑯"
}
PLAYER_NAMES = [f"プレイヤー{i+1}" for i in range(NUM_COLS)]
START_POINTS = [str(i + 1) for i in range(NUM_COLS)]

# --------------------------
# 状態初期化
# --------------------------

if "amidakuji_lines" not in st.session_state:
    # 横線ランダム生成
    st.session_state.amidakuji_lines = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 1):
            if random.random() < 0.2:
                st.session_state.amidakuji_lines.append((col, row))

if "player_assignment" not in st.session_state:
    st.session_state.player_assignment = {col: "" for col in START_POINTS}

if "show_result" not in st.session_state:
    st.session_state.show_result = False

# --------------------------
# SVG描画
# --------------------------

def generate_svg():
    svg = f'<svg width="{WIDTH}" height="{HEIGHT+80}" xmlns="http://www.w3.org/2000/svg">\n'

    # 縦線描画
    for i in range(NUM_COLS):
        x = i * COLUMN_SPACING
        svg += f'<line x1="{x}" y1="0" x2="{x}" y2="{HEIGHT}" stroke="black" stroke-width="2"/>\n'

    # 横線描画
    for col, row in st.session_state.amidakuji_lines:
        x1 = col * COLUMN_SPACING
        x2 = (col + 1) * COLUMN_SPACING
        y = row * ROW_SPACING
        svg += f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="black" stroke-width="2"/>\n'

    # スタート番号描画
    for i in range(NUM_COLS):
        x = i * COLUMN_SPACING
        svg += f'<text x="{x}" y="-10" text-anchor="middle" font-size="14">{i+1}</text>\n'

    # ゴール（〇数字）描画（非表示にしたい場合はコメントアウト）
    if st.session_state.show_result:
        for i in range(NUM_COLS):
            x = i * COLUMN_SPACING
            goal = GOAL_MAP[str(i+1)]
            svg += f'<text x="{x}" y="{HEIGHT + 30}" text-anchor="middle" font-size="16">{goal}</text>\n'
    else:
        for i in range(NUM_COLS):
            x = i * COLUMN_SPACING
            svg += f'<text x="{x}" y="{HEIGHT + 30}" text-anchor="middle" font-size="16">？？？</text>\n'

    svg += '</svg>'
    return svg

# --------------------------
# Streamlit UI
# --------------------------

st.title("🎯 不正あみだくじ（18人用・SVG）")
st.markdown("ランダムなあみだくじを表示しつつ、裏で不正にゴールを設定できます。")

# SVG表示
svg_code = generate_svg()
components.html(svg_code, height=HEIGHT+100)

# プレイヤー設定
st.subheader("スタート番号にプレイヤーを割り当ててください")
for col in START_POINTS:
    st.session_state.player_assignment[col] = st.selectbox(
        f"{col}番スタートのプレイヤー",
        [""] + PLAYER_NAMES,
        key=f"player_{col}"
    )

# 結果表示ボタン
if st.button("▶ 結果を見る"):
    st.session_state.show_result = True

# 結果表示
if st.session_state.show_result:
    st.subheader("🎉 結果発表")
    for start, player in st.session_state.player_assignment.items():
        if player:
            result = GOAL_MAP[start]
            st.markdown(f"**{player} → {result}**")
