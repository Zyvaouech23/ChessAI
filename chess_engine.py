import tkinter as tk
import time
import threading

PIECES = {
    "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟",
    "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙"
}

PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000
}

CENTER_SQUARES = [
    (3, 3), (3, 4), (4, 3), (4, 4),
    (2, 3), (2, 4), (5, 3), (5, 4),
    (3, 2), (4, 2), (3, 5), (4, 5)
]

class ChessGame:
    def __init__(self, root, ai_enabled=False):
        self.root = root
        self.canvas = tk.Canvas(root, width=640, height=640)
        self.canvas.pack()
        self.ai_enabled = ai_enabled

        self.board = self.create_board()
        self.selected = None
        self.possible_moves = []
        self.current_player = 'w'

        self.turn_number = 0
        self.en_passant_target = None
        self.castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

        if self.ai_enabled and self.current_player == 'b':
            self.root.after(100, self.ai_move)

    def create_board(self):
        board = [["" for _ in range(8)] for _ in range(8)]
        board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
        board[1] = ['bP'] * 8
        board[6] = ['wP'] * 8
        board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        return board

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#EEEED2", "#769656"]
        for row in range(8):
            for col in range(8):
                x1, y1 = col * 80, row * 80
                x2, y2 = x1 + 80, y1 + 80
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=PIECES[piece], font=("Arial", 36))

        for (row, col) in self.possible_moves:
            x1, y1 = col * 80, row * 80
            x2, y2 = x1 + 80, y1 + 80
            self.canvas.create_rectangle(x1+5, y1+5, x2-5, y2-5, outline="red", width=3)

    def handle_click(self, event):
        if self.ai_enabled and self.current_player == 'b':
            return

        col = event.x // 80
        row = event.y // 80

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        piece = self.board[row][col]

        if self.selected:
            if (row, col) in self.possible_moves:
                self.move_piece(*self.selected, row, col)
                self.selected = None
                self.possible_moves = []
                self.current_player = 'b' if self.current_player == 'w' else 'w'
                self.draw_board()

                if self.ai_enabled and self.current_player == 'b':
                    self.root.after(100, self.ai_move)
            else:
                self.selected = None
                self.possible_moves = []
                self.draw_board()
        elif piece and piece[0] == self.current_player:
            legal_moves = self.get_legal_moves(row, col)
            if self.is_in_check(self.current_player):
                # On filtre uniquement les coups qui permettent de sortir de l'échec
                all_moves = self.get_all_legal_moves(self.current_player)
                allowed_targets = {(sr, sc, dr, dc) for (sr, sc, dr, dc) in all_moves if sr == row and sc == col}
                legal_moves = [(dr, dc) for (sr, sc, dr, dc) in allowed_targets]

            self.selected = (row, col)
            self.possible_moves = legal_moves
            self.draw_board()

    def move_piece(self, sr, sc, dr, dc):
        piece = self.board[sr][sc]
        self.turn_number += 1

        self.board[dr][dc] = piece
        self.board[sr][sc] = ""

        if piece[1] == 'P' and (dr == 0 or dr == 7):
            self.board[dr][dc] = piece[0] + 'Q'

    def get_all_legal_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == color:
                    for dr, dc in self.get_legal_moves(r, c):
                        moves.append((r, c, dr, dc))
        return moves

    def get_legal_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        color = piece[0]
        raw_moves = self.get_raw_moves(row, col)
        legal_moves = []

        for dr, dc in raw_moves:
            captured = self.board[dr][dc]
            self.board[dr][dc] = piece
            self.board[row][col] = ""
            if not self.is_in_check(color):
                legal_moves.append((dr, dc))
            self.board[row][col] = piece
            self.board[dr][dc] = captured

        return legal_moves

    def is_in_check(self, color):
        king_pos = [(r, c) for r in range(8) for c in range(8) if self.board[r][c] == color + 'K']
        if not king_pos:
            return True
        kr, kc = king_pos[0]
        opponent = 'b' if color == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == opponent:
                    if (kr, kc) in self.get_raw_moves(r, c):
                        return True
        return False
