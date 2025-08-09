import tkinter as tk
from tkinter import messagebox
import random
import os

# --- Game Logic ---
def check_winner(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2 - i] == player for i in range(3)): return True
    return False

def empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]

def save_result(result):
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(result + "\n")

def ai_move():
    # 1. Try to win
    for r, c in empty_cells():
        board[r][c] = "O"
        if check_winner("O"):
            update_cell(r, c, "O")
            return
        board[r][c] = ""
    
    # 2. Block player
    for r, c in empty_cells():
        board[r][c] = "X"
        if check_winner("X"):
            board[r][c] = "O"
            update_cell(r, c, "O")
            return
        board[r][c] = ""
    
    # 3. Random move
    r, c = random.choice(empty_cells())
    update_cell(r, c, "O")

def update_cell(r, c, player):
    board[r][c] = player
    buttons[r][c].config(text=player, state="disabled")
    if check_winner(player):
        result = "🎉 You win!" if player == "X" else "💻 Computer wins!"
        save_result(result)
        messagebox.showinfo("Game Over", result)
        disable_board()
        return
    elif not empty_cells():
        save_result("🤝 It's a draw!")
        messagebox.showinfo("Game Over", "🤝 It's a draw!")
        disable_board()

def player_move(r, c):
    if board[r][c] == "":
        update_cell(r, c, "X")
        if empty_cells():
            ai_move()

def disable_board():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state="disabled")
    play_again_btn.config(state="normal")

def reset_board():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", state="normal")
    play_again_btn.config(state="disabled")

# --- GUI Setup ---
root = tk.Tk()
root.title("Tic-Tac-Toe vs Computer 🤖")

board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

# Game board buttons
for r in range(3):
    for c in range(3):
        btn = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda r=r, c=c: player_move(r, c))
        btn.grid(row=r, column=c)
        buttons[r][c] = btn

# Play Again button
play_again_btn = tk.Button(root, text="🔄 Play Again", font=("Arial", 14),
                           state="disabled", command=reset_board)
play_again_btn.grid(row=3, column=0, columnspan=3, pady=10)

# Create results file if not exists
if not os.path.exists("results.txt"):
    with open("results.txt", "w") as f:
        f.write("Tic-Tac-Toe Game Results\n------------------------\n")

root.mainloop()
