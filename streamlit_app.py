import streamlit as st
import matplotlib.pyplot as plt
import random

N = 6  # 縦線の本数
max_horizontal = 10  # 横線の本数

def generate_ladders(n, max_lines):
    ladders = []
    for _ in range(max_lines):
        x = random.randint(0, n-2)  # 横線の位置（縦線間）
        y = random.uniform(0, 1)    # 高さ（0〜1）
        ladders.append((x, y))
    ladders.sort(key=lambda x: x[1])
    return ladders

def draw_amidakuji(n, ladders):
    fig, ax = plt.subplots(figsize=(6, 8))

    # 縦線を描く
    for i in range(n):
        ax.plot([i, i], [0, 1], color="black", linewidth=2)

    # 横線を描く
    for (x, y) in ladders:
        ax.plot([x, x+1], [y, y], color="black", linewidth=2)

    # 軸の調整
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, 1)
    ax.axis('off')  # 軸非表示

    return fig

st.title("あみだくじ線の描画")

ladders = generate_ladders(N, max_horizontal)

fig = draw_amidakuji(N, ladders)
st.pyplot(fig)
