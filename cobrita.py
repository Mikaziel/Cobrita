import tkinter as tk
from random import choice

import customtkinter as ctk


BOARD_CELLS = 20
CELL_SIZE = 20
BOARD_SIZE = BOARD_CELLS * CELL_SIZE
MOVE_INTERVAL_MS = 150
WINDOW_COLOR = "#17201b"
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


def choose_food_position(snake):
    occupied = set(snake)
    free_cells = [
        (column, row)
        for row in range(BOARD_CELLS)
        for column in range(BOARD_CELLS)
        if (column, row) not in occupied
    ]
    return choice(free_cells) if free_cells else None


def show_game(app):
    score = ctk.CTkLabel(app, text="0 pontos", anchor="w")
    score.pack(fill="x", padx=16, pady=(12, 8))

    board = tk.Canvas(
        app,
        width=BOARD_SIZE,
        height=BOARD_SIZE,
        background="#0c130f",
        highlightthickness=0,
    )
    board.pack(padx=16, pady=(0, 16))

    footer = ctk.CTkFrame(app, fg_color="transparent")
    footer.pack(fill="x", padx=16, pady=(0, 16))
    status = ctk.CTkLabel(footer, text="", anchor="w")
    status.pack(side="left")

    snake = []
    food = None
    points = 0
    direction = (1, 0)
    next_direction = None
    move_timer = None

    def draw_snake():
        board.delete("snake")
        for column, row in snake:
            draw_cell(board, column, row, "#73d79a", "snake")

    def draw_food():
        board.delete("food")
        if food is not None:
            column, row = food
            draw_cell(board, column, row, "#ff8178", "food")

    def handle_key(event):
        nonlocal next_direction
        key = event.keysym.lower()
        if key == "r":
            restart_game()
            return

        requested = DIRECTIONS.get(key)
        if move_timer is None or requested is None:
            return

        opposite = (-direction[0], -direction[1])
        if requested != opposite:
            next_direction = requested

    def move_snake():
        nonlocal direction, food, move_timer, points
        move_timer = None
        if next_direction is not None:
            column, row = snake[0]
            dx, dy = next_direction
            new_column, new_row = column + dx, row + dy
            new_head = (new_column, new_row)
            if (
                not 0 <= new_column < BOARD_CELLS
                or not 0 <= new_row < BOARD_CELLS
                or new_head in snake[:-1]
            ):
                status.configure(text="Fim de jogo")
                return

            snake.insert(0, new_head)
            direction = next_direction
            if new_head == food:
                points += 1
                score.configure(text="1 ponto" if points == 1 else f"{points} pontos")
                food = choose_food_position(snake)
                draw_food()
            else:
                snake.pop()
            draw_snake()

        if food is None:
            status.configure(text="Tabuleiro completo")
            return

        move_timer = app.after(MOVE_INTERVAL_MS, move_snake)

    def restart_game():
        nonlocal direction, food, move_timer, next_direction, points
        if move_timer is not None:
            app.after_cancel(move_timer)

        snake[:] = [(9, 10), (8, 10), (7, 10)]
        food = (13, 10)
        points = 0
        direction = (1, 0)
        next_direction = None
        score.configure(text="0 pontos")
        status.configure(text="")
        draw_food()
        draw_snake()
        board.focus_set()
        move_timer = app.after(MOVE_INTERVAL_MS, move_snake)

    ctk.CTkButton(footer, text="Reiniciar (R)", command=restart_game).pack(side="right")
    app.bind("<KeyPress>", handle_key)
    restart_game()


def main():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk(fg_color=WINDOW_COLOR)
    app.title("Cobrita")
    app.resizable(False, False)

    menu_screen = ctk.CTkFrame(
        app,
        width=BOARD_SIZE + 32,
        height=508,
        fg_color=WINDOW_COLOR,
        corner_radius=0,
    )
    menu_screen.pack(fill="both", expand=True)
    menu_screen.grid_propagate(False)
    menu_screen.grid_columnconfigure(0, weight=1)
    menu_screen.grid_rowconfigure(0, weight=1)
    menu_screen.grid_rowconfigure(3, weight=1)

    def start_game():
        menu_screen.pack_forget()
        show_game(app)

    ctk.CTkLabel(
        menu_screen,
        text="Cobrita",
        font=ctk.CTkFont(size=56, weight="bold"),
        text_color="#73d79a",
    ).grid(row=1, column=0, pady=(0, 20))
    ctk.CTkButton(
        menu_screen, text="Play", command=start_game, width=144, height=40,
    ).grid(row=2, column=0)

    app.mainloop()


if __name__ == "__main__":
    main()
