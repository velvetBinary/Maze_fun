# 🧱 Maze Escape Game (Enhanced GUI Version)

import tkinter as tk
import random

CELL_SIZE = 40
ROWS = 10
COLS = 10
TIME_LIMIT = 30  # seconds

class MazeEscape:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Escape")
        self.canvas = tk.Canvas(master, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.timer_label = tk.Label(master, text=f"Time Left: {TIME_LIMIT}", font=("Arial", 12))
        self.timer_label.grid(row=1, column=0, pady=10)

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=1, column=1)

        self.theme_button = tk.Button(master, text="Toggle Dark Mode", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=2)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.grid(row=1, column=3)

        self.dark_mode = False
        self.time_left = TIME_LIMIT
        self.timer_id = None

        self.restart_game()
        self.canvas.bind_all("<Key>", self.move_player)

    def restart_game(self):
        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = (0, 0)
        self.exit_pos = (ROWS - 1, COLS - 1)
        self.generate_maze()
        self.grid[self.exit_pos[0]][self.exit_pos[1]] = 0  # ensure exit is walkable
        self.time_left = TIME_LIMIT
        self.update_timer()
        self.draw_maze()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.draw_maze()

    def generate_maze(self):
        def carve(x, y):
            dirs = [(0,1),(1,0),(0,-1),(-1,0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < ROWS and 0 <= ny < COLS and self.grid[nx][ny] == 1:
                    self.grid[nx - dx][ny - dy] = 0
                    self.grid[nx][ny] = 0
                    carve(nx, ny)

        for r in range(ROWS):
            for c in range(COLS):
                self.grid[r][c] = 1
        self.grid[0][0] = 0
        carve(0, 0)
        self.grid[self.exit_pos[0]][self.exit_pos[1]] = 0

    def draw_maze(self):
        self.canvas.delete("all")
        wall_color = "#222" if self.dark_mode else "black"
        path_color = "#EEE" if self.dark_mode else "white"
        player_color = "cyan"
        exit_color = "lime"

        for r in range(ROWS):
            for c in range(COLS):
                color = wall_color if self.grid[r][c] == 1 else path_color
                self.canvas.create_rectangle(
                    c * CELL_SIZE, r * CELL_SIZE,
                    (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                    fill=color, outline="gray"
                )
        pr, pc = self.player_pos
        er, ec = self.exit_pos
        self.canvas.create_rectangle(pc*CELL_SIZE, pr*CELL_SIZE, (pc+1)*CELL_SIZE, (pr+1)*CELL_SIZE, fill=player_color)
        self.canvas.create_rectangle(ec*CELL_SIZE, er*CELL_SIZE, (ec+1)*CELL_SIZE, (er+1)*CELL_SIZE, fill=exit_color)

    def move_player(self, event):
        r, c = self.player_pos
        if event.keysym == "Up": r -= 1
        elif event.keysym == "Down": r += 1
        elif event.keysym == "Left": c -= 1
        elif event.keysym == "Right": c += 1
        if 0 <= r < ROWS and 0 <= c < COLS and self.grid[r][c] == 0:
            self.player_pos = (r, c)
            self.draw_maze()
            if self.player_pos == self.exit_pos:
                self.canvas.create_text(COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="You Escaped!", font=("Arial", 28), fill="red")
                self.master.after_cancel(self.timer_id)

    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.canvas.create_text(COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="Time's Up!", font=("Arial", 28), fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeEscape(root)
    root.mainloop()
