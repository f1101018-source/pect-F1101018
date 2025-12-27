import tkinter as tk
from tkinter import messagebox
import random

# ===============================
# 第三版：宮崎駿風格踩地雷
# ===============================

def open_version_three():
    diff_win = tk.Toplevel(root)
    diff_win.title("選擇冒險難度")
    diff_win.geometry("250x200")

    def start_game(rows, cols, mines):
        diff_win.destroy()
        start_ghibli_game(rows, cols, mines)

    tk.Label(diff_win, text="選擇森林冒險難度", font=("Arial", 12)).pack(pady=10)
    tk.Button(diff_win, text="🌼 簡單", command=lambda: start_game(6, 6, 6)).pack(pady=5)
    tk.Button(diff_win, text="🍃 普通", command=lambda: start_game(8, 8, 10)).pack(pady=5)
    tk.Button(diff_win, text="🌲 困難", command=lambda: start_game(10, 10, 18)).pack(pady=5)


def start_ghibli_game(ROWS, COLS, MINES):
    win = tk.Toplevel(root)
    win.title("宮崎駿風格踩地雷")
    win.config(bg="#dff0d8")

    first_click = True
    mines = [[0]*COLS for _ in range(ROWS)]
    revealed = [[False]*COLS for _ in range(ROWS)]
    flagged = [[False]*COLS for _ in range(ROWS)]

    frame = tk.Frame(win, bg="#dff0d8")
    frame.pack(padx=10, pady=10)

    buttons = []

    def place_mines(er, ec):
        placed = 0
        while placed < MINES:
            r = random.randint(0, ROWS-1)
            c = random.randint(0, COLS-1)
            if (r, c) != (er, ec) and mines[r][c] == 0:
                mines[r][c] = -1
                placed += 1

    def left_click(r, c):
        nonlocal first_click

        if revealed[r][c] or flagged[r][c]:
            return

        if first_click:
            place_mines(r, c)
            first_click = False

        if mines[r][c] == -1:
            buttons[r][c].config(text="🌱", bg="#7fbf7f")
            messagebox.showerror("冒險失敗", "你踩到森林陷阱了")
            win.destroy()
            return

        revealed[r][c] = True
        buttons[r][c].config(text="🌼", bg="#f7fcb9", state=tk.DISABLED)

    def right_click(r, c):
        if revealed[r][c]:
            return
        flagged[r][c] = not flagged[r][c]
        buttons[r][c].config(text="🍃" if flagged[r][c] else "")

    for r in range(ROWS):
        row = []
        for c in range(COLS):
            b = tk.Button(frame, width=3, height=1, bg="#eaf7e4")
            b.grid(row=r, column=c)
            b.bind("<Button-1>", lambda e, r=r, c=c: left_click(r, c))
            b.bind("<Button-3>", lambda e, r=r, c=c: right_click(r, c))
            row.append(b)
        buttons.append(row)


# ===============================
# 主選單
# ===============================

root = tk.Tk()
root.title("踩地雷專題主選單")
root.geometry("320x300")

tk.Label(root, text="踩地雷多版本專題", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="第三版：宮崎駿風格", width=25, command=open_version_three).pack(pady=10)
tk.Button(root, text="離開", width=25, command=root.quit).pack(pady=10)

root.mainloop()
