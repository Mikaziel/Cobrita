import tkinter as tk

import customtkinter as ctk


BOARD_CELLS = 20
CELL_SIZE = 20
MOVE_INTERVAL_MS = 150
DIRECTIONS = {
    "up": (0, -1),
    "w": (0, -1),
    "down": (0, 1),
    "s": (0, 1),
    "left": (-1, 0),
    "a": (-1, 0),
    "right": (1, 0),
    "d": (1, 0),
}


def draw_cell(board, column, row, color, tag):
    x = column * CELL_SIZE
    y = row * CELL_SIZE
    board.create_rectangle(
        x + 1,
        y + 1,
        x + CELL_SIZE - 1,
        y + CELL_SIZE - 1,
        fill=color,
        outline="",
        tags=tag,
    )


def main():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk(fg_color="#17201b")
    app.title("Cobrita")
    app.resizable(False, False)

    score = ctk.CTkLabel(app, text="0 pontos", anchor="w")
    score.pack(fill="x", padx=16, pady=(12, 8))

    board_size = BOARD_CELLS * CELL_SIZE
    board = tk.Canvas(
        app,
        width=board_size,
        height=board_size,
        background="#0c130f",
        highlightthickness=0,
    )
    board.pack(padx=16, pady=(0, 16))

    snake = [(9, 10), (8, 10), (7, 10)]
    direction = (1, 0)
    next_direction = None

    def draw_snake():
        board.delete("snake")
        for column, row in snake:
            draw_cell(board, column, row, "#73d79a", "snake")

    def steer(event):
        nonlocal next_direction
        requested = DIRECTIONS.get(event.keysym.lower())
        if requested is None:
            return

        opposite = (-direction[0], -direction[1])
        if requested != opposite:
            next_direction = requested

    def move_snake():
        nonlocal direction
        if next_direction is not None:
            column, row = snake[0]
            dx, dy = next_direction
            new_column, new_row = column + dx, row + dy
            if 0 <= new_column < BOARD_CELLS and 0 <= new_row < BOARD_CELLS:
                snake.insert(0, (new_column, new_row))
                snake.pop()
                direction = next_direction
                draw_snake()

        app.after(MOVE_INTERVAL_MS, move_snake)

    draw_cell(board, 13, 10, "#ff8178", "food")
    draw_snake()

    app.bind("<KeyPress>", steer)
    board.focus_set()
    app.after(MOVE_INTERVAL_MS, move_snake)

    app.mainloop()


if __name__ == "__main__":
    main()
