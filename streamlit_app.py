import streamlit as st
import random
import svgwrite

# -------------------------------
# 🎛 不正対応（好きなように設定可能）
# -------------------------------
GOAL_MAP = {
    "1": "⑱", "2": "⑰", "3": "⑯", "4": "⑮", "5": "⑭",
    "6": "⑬", "7": "⑫", "8": "⑪", "9": "⑩", "10": "⑨",
    "11": "⑧", "12": "⑦", "13": "⑥", "14": "⑤", "15": "④",
    "16": "③", "17": "②", "18": "①"
}

st.set_page_config(layout="wide", page_title="不正あみだくじ")

st.title("🎯 不正あみだくじ（18人用）")
st.caption("スタート地点にプレイヤーを割り当て、ゴールは事前設定されたものに従って不正に到達します。")

NUM_LINES = 18
LINE_LENGTH = 600
LINE_HEIGHT = 600
STEP = LINE_LENGTH // (NUM_LINES - 1)
HORIZ_SPACING = 40

# プレイヤー選択（1〜18人）
st.subheader("🎮 各スタート地点にプレイヤーを割り当ててください")

player_names = ["" for _ in range(NUM_LINES)]
cols = st.columns(NUM_LINES)
for i in range(NUM_LINES):
    with cols[i]:
        player_names[i] = st.selectbox(f"", options=[""] + [f"Player {j+1}" for j in range(NUM_LINES)], key=f"p{i}")
        st.markdown(f"<small>{i+1}</small>", unsafe_allow_html=True)

# ランダムな横線生成
def generate_lines():
    lines = []
    for y in range(50, LINE_HEIGHT, 30):
        candidates = list(range(NUM_LINES - 1))
        random.shuffle(candidates)
        for i in candidates[:random.randint(2, 5)]:
            lines.append(((i, y), (i + 1, y)))
    return lines

# SVGの描画
def draw_svg(lines):
    dwg = svgwrite.Drawing(size=(LINE_LENGTH + 2*HORIZ_SPACING, LINE_HEIGHT + 100))
    # 縦線
    for i in range(NUM_LINES):
        x = i * STEP + HORIZ_SPACING
        dwg.add(dwg.line(start=(x, 50), end=(x, LINE_HEIGHT), stroke='black', stroke_width=2))
    # 横線
    for (start, end) in lines:
    x1 = start[0] * STEP + HORIZ_SPACING
    x2 = end[0] * STEP + HORIZ_SPACING
    y = start[1]
    dwg.add(dwg.line(start=(x1, y), end=(x2, y), stroke='black', stroke_width=2))
    return dwg.tostring()

# あみだくじ処理
def follow_path(start_idx, lines):
    x = start_idx
    y = 50
    path = sorted(lines, key=lambda l: l[0][1])  # Y順に
    for (a, b) in path:
        if a[1] != y:
            continue
        if a[0] == x:
            x = b[0]
        elif b[0] == x:
            x = a[0]
    return x

# 横線生成と描画
lines = generate_lines()
svg = draw_svg(lines)
st.subheader("🖼 あみだくじ")
st.components.v1.html(svg, height=LINE_HEIGHT + 120, scrolling=False)

# 実行ボタン
if st.button("▶ 結果を見る"):
    st.subheader("🎉 結果発表")

    result_table = []
    for i in range(NUM_LINES):
        name = player_names[i] if player_names[i] else f"（未選択{i+1}）"
        final_x = follow_path(i, lines)
        final_pos = str(final_x + 1)
        goal = GOAL_MAP.get(final_pos, "❓")
        result_table.append({
            "スタート番号": i + 1,
            "プレイヤー": name,
            "到達ゴール": goal
        })

    st.table(result_table)
