import tkinter as tk
from chess_engine import ChessGame

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.main_menu()
        self.root.mainloop()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Chess Game", font=("Arial", 32))
        title.pack(pady=20)

        author = tk.Label(self.root, text="by Kasper", font=("Arial", 12))
        author.pack(pady=5)

        solo_btn = tk.Button(self.root, text="Solo (vs ZyvaAI Chess)", font=("Arial", 18), width=20, command=self.start_solo)
        solo_btn.pack(pady=10)

        multi_btn = tk.Button(self.root, text="Multijoueur (2 joueurs)", font=("Arial", 18), width=20, command=self.start_multiplayer)
        multi_btn.pack(pady=10)

    def start_solo(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Échecs - Solo")
        ChessGame(game_window, ai_enabled=True)

    def start_multiplayer(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Échecs - Multijoueur")
        ChessGame(game_window, ai_enabled=False)

if __name__ == "__main__":
    ChessApp()