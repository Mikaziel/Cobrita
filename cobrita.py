import tkinter as tk

import customtkinter as ctk


BOARD_CELLS = 20
CELL_SIZE = 20


def draw_cell(board, column, row, color):
    x = column * CELL_SIZE
    y = row * CELL_SIZE
    board.create_rectangle(
        x + 1,
        y + 1,
        x + CELL_SIZE - 1,
        y + CELL_SIZE - 1,
        fill=color,
        outline="",
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
    for column, row in snake:
        draw_cell(board, column, row, "#73d79a")

    draw_cell(board, 13, 10, "#ff8178")

    app.mainloop()


if __name__ == "__main__":
    main()
