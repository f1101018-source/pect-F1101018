import tkinter as tk
from tkinter import messagebox
import random
import time

# ======================
# 主遊戲類別
# ======================
class Minesweeper:
    def __init__(self, root, rows=9, cols=9, mines=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.total_mines = mines

        # 是否已經點擊第一次（用來確保第一次不踩雷）
        self.first_click = True

        # 記錄開始時間
        self.start_time = None
        self.timer_running = False

        # 建立資料結構
        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.revealed = set()

        self.create_ui()
        self.create_board()

    # ======================
    # 建立上方資訊 UI
    # ======================
    def create_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack()

        self.mine_label = tk.Label(top_frame, text=f"💣 地雷：{self.total_mines}")
        self.mine_label.pack(side=tk.LEFT, padx=10)

        self.flag_label = tk.Label(top_frame, text="🚩 插旗正確：0")
        self.flag_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(top_frame, text="⏱ 時間：0 秒")
        self.time_label.pack(side=tk.LEFT, padx=10)

        restart_btn = tk.Button(top_frame, text="重新開始", command=self.restart)
        restart_btn.pack(side=tk.RIGHT, padx=10)

    # ======================
    # 建立棋盤
    # ======================
    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # ======================
    # 放置地雷（第一次點擊後）
    # ======================
    def place_mines(self, safe_cell):
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        all_cells.remove(safe_cell)

        self.mines = set(random.sample(all_cells, self.total_mines))

    # ======================
    # 左鍵點擊
    # ======================
    def left_click(self, r, c):
        if (r, c) in self.flags or (r, c) in self.revealed:
            return

        if self.first_click:
            self.place_mines((r, c))
            self.start_timer()
            self.first_click = False

        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)

        if self.check_win():
            self.game_over(True)

    # ======================
    # 右鍵插旗
    # ======================
    def right_click(self, r, c):
        if (r, c) in self.revealed:
            return

        btn = self.buttons[(r, c)]

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            self.flags.add((r, c))
            btn.config(text="🚩")

        self.update_flag_score()

    # ======================
    # 翻開格子
    # ======================
    def reveal(self, r, c):
        if (r, c) in self.revealed:
            return

        self.revealed.add((r, c))
        btn = self.buttons[(r, c)]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)

        count = self.count_adjacent_mines(r, c)

        if count > 0:
            btn.config(text=str(count))
        else:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    # ======================
    # 計算周圍地雷數
    # ======================
    def count_adjacent_mines(self, r, c):
        count = 0
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if (nr, nc) in self.mines:
                    count += 1
        return count

    # ======================
    # 判斷勝利
    # ======================
    def check_win(self):
        return len(self.revealed) == self.rows * self.cols - self.total_mines

    # ======================
    # 遊戲結束
    # ======================
    def game_over(self, win):
        self.timer_running = False

        for (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣")

        if win:
            messagebox.showinfo("勝利", f"恭喜過關！耗時 {int(time.time() - self.start_time)} 秒")
        else:
            messagebox.showerror("失敗", "你踩到地雷了！")

    # ======================
    # 更新插旗正確數
    # ======================
    def update_flag_score(self):
        correct = len(self.flags & self.mines)
        self.flag_label.config(text=f"🚩 插旗正確：{correct}")

    # ======================
    # 計時器
    # ======================
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"⏱ 時間：{elapsed} 秒")
            self.root.after(1000, self.update_timer)

    # ======================
    # 重新開始
    # ======================
    def restart(self):
        self.board_frame.destroy()
        self.first_click = True
        self.mines.clear()
        self.flags.clear()
        self.revealed.clear()
        self.flag_label.config(text="🚩 插旗正確：0")
        self.time_label.config(text="⏱ 時間：0 秒")
        self.create_board()


# ======================
# 主程式入口
# ======================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("踩地雷 Minesweeper")
    game = Minesweeper(root, rows=9, cols=9, mines=10)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import time

# ==================================================
# 第一版踩地雷（基礎版）
# ==================================================
class MinesweeperV1:
    def __init__(self, window):
        self.window = window
        self.window.title("踩地雷 第一版（基礎版）")

        self.rows = 8
        self.cols = 8
        self.mines_count = 10

        self.first_click = True
        self.mines = set()
        self.buttons = {}

        self.create_board()

    def create_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.window,
                    width=3,
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def place_mines(self, safe_cell):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        cells.remove(safe_cell)
        self.mines = set(random.sample(cells, self.mines_count))

    def click(self, r, c):
        if self.first_click:
            self.place_mines((r, c))
            self.first_click = False

        if (r, c) in self.mines:
            messagebox.showerror("遊戲結束", "你踩到地雷了 💣")
            return

        self.buttons[(r, c)].config(text="O", state=tk.DISABLED)


# ==================================================
# 第二版踩地雷（進階版）
# ==================================================
class MinesweeperV2:
    def __init__(self, window):
        self.window = window
        self.window.title("踩地雷 第二版（進階版）")

        self.rows = 9
        self.cols = 9
        self.mines_count = 10

        self.first_click = True
        self.mines = set()
        self.flags = set()
        self.revealed = set()

        self.start_time = None
        self.timer_running = False

        self.create_top_ui()
        self.create_board()

    # ---------- 上方 UI ----------
    def create_top_ui(self):
        top = tk.Frame(self.window)
        top.pack(pady=5)

        self.time_label = tk.Label(top, text="⏱ 時間：0 秒")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.flag_label = tk.Label(top, text="🚩 插旗正確：0")
        self.flag_label.pack(side=tk.LEFT, padx=10)

        tk.Button(top, text="重新開始", command=self.restart).pack(side=tk.RIGHT, padx=10)

    # ---------- 建立棋盤 ----------
    def create_board(self):
        self.board = tk.Frame(self.window)
        self.board.pack()

        self.buttons = {}

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board,
                    width=3,
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # ---------- 放置地雷 ----------
    def place_mines(self, safe_cell):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        cells.remove(safe_cell)
        self.mines = set(random.sample(cells, self.mines_count))

    # ---------- 左鍵 ----------
    def left_click(self, r, c):
        if (r, c) in self.flags or (r, c) in self.revealed:
            return

        if self.first_click:
            self.place_mines((r, c))
            self.start_timer()
            self.first_click = False

        if (r, c) in self.mines:
            self.game_over(False)
            return

        self.reveal(r, c)

    # ---------- 右鍵 ----------
    def right_click(self, r, c):
        if (r, c) in self.revealed:
            return

        btn = self.buttons[(r, c)]

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="")
        else:
            self.flags.add((r, c))
            btn.config(text="🚩")

        self.update_flag_score()

    # ---------- 翻格 ----------
    def reveal(self, r, c):
        if (r, c) in self.revealed:
            return

        self.revealed.add((r, c))
        self.buttons[(r, c)].config(relief=tk.SUNKEN, state=tk.DISABLED)

    # ---------- 遊戲結束 ----------
    def game_over(self, win):
        self.timer_running = False
        for cell in self.mines:
            self.buttons[cell].config(text="💣")

        if win:
            messagebox.showinfo("勝利", "你贏了！")
        else:
            messagebox.showerror("失敗", "踩到地雷 💣")

    # ---------- 插旗分數 ----------
    def update_flag_score(self):
        correct = len(self.flags & self.mines)
        self.flag_label.config(text=f"🚩 插旗正確：{correct}")

    # ---------- 計時 ----------
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"⏱ 時間：{elapsed} 秒")
            self.window.after(1000, self.update_timer)

    # ---------- 重新開始 ----------
    def restart(self):
        self.board.destroy()
        self.first_click = True
        self.mines.clear()
        self.flags.clear()
        self.revealed.clear()
        self.time_label.config(text="⏱ 時間：0 秒")
        self.flag_label.config(text="🚩 插旗正確：0")
        self.create_board()


# ==================================================
# 主選單
# ==================================================
def open_v1():
    win = tk.Toplevel(root)
    MinesweeperV1(win)

def open_v2():
    win = tk.Toplevel(root)
    MinesweeperV2(win)

root = tk.Tk()
root.title("踩地雷版本選單")

tk.Label(root, text="請選擇要開啟的版本", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="第一版（基礎）", width=20, command=open_v1).pack(pady=5)
tk.Button(root, text="第二版（進階）", width=20, command=open_v2).pack(pady=5)

root.mainloop()
