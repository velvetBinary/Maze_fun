# 🧱 Maze Escape Game (Basic Logic First)

import tkinter as tk
import random

CELL_SIZE = 40
ROWS = 10
COLS = 10

class MazeEscape:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
        self.canvas.pack()

        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = (0, 0)
        self.exit_pos = (ROWS - 1, COLS - 1)

        self.generate_maze()
        self.draw_maze()

        self.canvas.bind_all("<Key>", self.move_player)

    def generate_maze(self):
        # Simple recursive backtracking maze generation
        def carve(x, y):
            dirs = [(0,1),(1,0),(0,-1),(-1,0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < ROWS and 0 <= ny < COLS and self.grid[nx][ny] == 1:
                    self.grid[nx - dx][ny - dy] = 0
                    self.grid[nx][ny] = 0
                    carve(nx, ny)

        # Initialize entire grid as walls (1), then carve
        for r in range(ROWS):
            for c in range(COLS):
                self.grid[r][c] = 1
        self.grid[0][0] = 0
        carve(0, 0)
        self.grid[self.exit_pos[0]][self.exit_pos[1]] = 0

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                color = "black" if self.grid[r][c] == 1 else "white"
                self.canvas.create_rectangle(
                    c * CELL_SIZE, r * CELL_SIZE,
                    (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE,
                    fill=color
                )
        pr, pc = self.player_pos
        er, ec = self.exit_pos
        self.canvas.create_rectangle(pc*CELL_SIZE, pr*CELL_SIZE, (pc+1)*CELL_SIZE, (pr+1)*CELL_SIZE, fill="blue")
        self.canvas.create_rectangle(ec*CELL_SIZE, er*CELL_SIZE, (ec+1)*CELL_SIZE, (er+1)*CELL_SIZE, fill="green")

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
                self.canvas.create_text(
                    COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2,
                    text="You Escaped!", font=("Arial", 24), fill="red"
                )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Escape")
    game = MazeEscape(root)
    root.mainloop()
