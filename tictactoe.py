import customtkinter as ctk
import tkinter.messagebox as messagebox

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya - Minimax IA")
        self.root.geometry("400x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.start_frame = None
        self.board_frame = None
        self.result_label = None

        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.board = [""] * 9
        self.buttons = []

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_widgets()

        self.start_frame = ctk.CTkFrame(self.root)
        self.start_frame.pack(expand=True)

        label = ctk.CTkLabel(self.start_frame, text="Elige tu símbolo:", font=("Arial", 20))
        label.pack(pady=20)

        x_button = ctk.CTkButton(self.start_frame, text="Jugar como X", command=lambda: self.start_game("X"))
        x_button.pack(pady=10)

        o_button = ctk.CTkButton(self.start_frame, text="Jugar como O", command=lambda: self.start_game("O"))
        o_button.pack(pady=10)

    def start_game(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        self.board = [""] * 9
        self.buttons = []

        self.clear_widgets()
        self.create_game_board()

        if self.player_symbol == "O":
            self.ai_move()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_game_board(self):
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20)

        for i in range(9):
            button = ctk.CTkButton(
                self.board_frame, text="", width=80, height=80,
                font=("Arial", 30),
                fg_color="gray", text_color="white",
                command=lambda i=i: self.player_move(i)
            )
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        self.result_label = ctk.CTkLabel(self.root, text="", font=("Arial", 18))
        self.result_label.pack(pady=10)

    def player_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.player_symbol
            self.update_button(index)
            if self.check_winner(self.player_symbol):
                self.end_game("¡Ganaste!")
            elif "" not in self.board:
                self.end_game("¡Empate!")
            else:
                self.root.after(100, self.ai_move)
        else:
            messagebox.showinfo("Movimiento inválido", "Esa casilla ya está ocupada.")

    def ai_move(self):
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai_symbol
                score = self.minimax(self.board, 0, False, -float("inf"), float("inf"))
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = self.ai_symbol
            self.update_button(best_move)
            if self.check_winner(self.ai_symbol):
                self.end_game("Perdiste...")
            elif "" not in self.board:
                self.end_game("¡Empate!")

    def minimax(self, board, depth, is_maximizing, alpha=-float("inf"), beta=float("inf")):
        if self.check_winner(self.ai_symbol):
            return 1
        elif self.check_winner(self.player_symbol):
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = self.ai_symbol
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = self.player_symbol
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def update_button(self, index):
        symbol = self.board[index]
        color = "lightblue" if symbol == "X" else "tomato"
        self.buttons[index].configure(text=symbol, fg_color=color, state="disabled")

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def end_game(self, message):
        answer = messagebox.askyesno("Fin del juego", message + "\n¿Deseas jugar otra vez?")
        if answer:
            self.create_start_screen()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToeApp(root)
    root.mainloop()
