import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

# Symboles Unicode pour les pièces d'échecs
PIECES = {
    "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟",
    "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙"
}

# Valeurs des pièces pour l'évaluation
PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000
}

# Tables de position pour une évaluation plus fine
PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

CENTER_SQUARES = [
    (3, 3), (3, 4), (4, 3), (4, 4),
    (2, 3), (2, 4), (5, 3), (5, 4),
    (3, 2), (4, 2), (3, 5), (4, 5)
]

class ChessGame:
    def __init__(self, root, ai_enabled=False, parent_app=None):
        self.root = root
        self.parent_app = parent_app
        self.ai_enabled = ai_enabled
        
        # Configuration de la fenêtre
        self.setup_window()
        
        # Initialisation du jeu
        self.board = self.create_board()
        self.selected = None
        self.possible_moves = []
        self.current_player = 'w'
        self.is_thinking = False
        self.game_over = False
        self.move_history = []
        
        # Interface utilisateur
        self.create_widgets()
        self.draw_board()
        
        # Démarrer l'IA si nécessaire
        if self.ai_enabled and self.current_player == 'b':
            self.root.after(1000, self.ai_move)

    def setup_window(self):
        """Configure la fenêtre de jeu"""
        self.root.configure(bg='#2b2b2b')
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Frame supérieur pour les informations
        info_frame = tk.Frame(main_frame, bg='#2b2b2b')
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Titre du jeu
        game_title = tk.Label(
            info_frame,
            text="♔ PARTIE D'ÉCHECS ♛",
            font=("Arial", 20, "bold"),
            fg='#FFD700',
            bg='#2b2b2b'
        )
        game_title.pack()
        
        # Frame pour le status et les contrôles
        status_frame = tk.Frame(info_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', pady=5)
        
        # Label du joueur actuel
        self.status_label = tk.Label(
            status_frame,
            text="Tour des Blancs",
            font=("Arial", 14, "bold"),
            fg='#CCCCCC',
            bg='#2b2b2b'
        )
        self.status_label.pack(side='left')
        
        # Label pour l'IA qui réfléchit
        self.thinking_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 12, "italic"),
            fg='#FFA500',
            bg='#2b2b2b'
        )
        self.thinking_label.pack(side='left', padx=(20, 0))
        
        # Boutons de contrôle
        control_frame = tk.Frame(status_frame, bg='#2b2b2b')
        control_frame.pack(side='right')
        
        # Bouton nouvelle partie
        new_game_btn = tk.Button(
            control_frame,
            text="🔄 Nouvelle Partie",
            font=("Arial", 10, "bold"),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            command=self.new_game,
            cursor='hand2'
        )
        new_game_btn.pack(side='left', padx=2)
        
        # Bouton retour menu
        menu_btn = tk.Button(
            control_frame,
            text="🏠 Menu",
            font=("Arial", 10, "bold"),
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            command=self.return_to_menu,
            cursor='hand2'
        )
        menu_btn.pack(side='left', padx=2)
        
        # Frame pour l'échiquier
        board_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='raised', bd=3)
        board_frame.pack()
        
        # Canvas pour l'échiquier
        self.canvas = tk.Canvas(
            board_frame, 
            width=640, 
            height=640,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)
        
        # Bind des événements
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_hover)

    def create_board(self):
        """Initialise l'échiquier avec les pièces"""
        board = [["" for _ in range(8)] for _ in range(8)]
        board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
        board[1] = ['bP'] * 8
        board[6] = ['wP'] * 8
        board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        return board

    def draw_board(self):
        """Dessine l'échiquier et les pièces"""
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]  # Couleurs d'échiquier classiques
        
        for row in range(8):
            for col in range(8):
                x1, y1 = col * 80, row * 80
                x2, y2 = x1 + 80, y1 + 80
                color = colors[(row + col) % 2]
                
                # Dessiner la case
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Ajouter les coordonnées
                if col == 0:  # Numéros des rangs
                    self.canvas.create_text(
                        x1 + 10, y1 + 10, 
                        text=str(8-row), 
                        font=("Arial", 10, "bold"), 
                        fill="#444444"
                    )
                if row == 7:  # Lettres des colonnes
                    self.canvas.create_text(
                        x2 - 10, y2 - 10, 
                        text=chr(ord('a') + col), 
                        font=("Arial", 10, "bold"), 
                        fill="#444444"
                    )
                
                # Dessiner la pièce
                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text(
                        (x1 + x2) // 2, 
                        (y1 + y2) // 2, 
                        text=PIECES[piece], 
                        font=("Arial", 36),
                        fill="#000000"
                    )

        # Mettre en évidence la case sélectionnée
        if self.selected:
            row, col = self.selected
            x1, y1 = col * 80, row * 80
            x2, y2 = x1 + 80, y1 + 80
            self.canvas.create_rectangle(
                x1 + 2, y1 + 2, x2 - 2, y2 - 2, 
                outline="#FFD700", width=4
            )

        # Mettre en évidence les coups possibles
        for (row, col) in self.possible_moves:
            x1, y1 = col * 80, row * 80
            x2, y2 = x1 + 80, y1 + 80
            
            if self.board[row][col]:  # Case avec pièce ennemie (capture)
                self.canvas.create_oval(
                    x1 + 10, y1 + 10, x2 - 10, y2 - 10, 
                    outline="#FF4444", width=4, fill=""
                )
            else:  # Case vide
                self.canvas.create_oval(
                    x1 + 30, y1 + 30, x2 - 30, y2 - 30, 
                    fill="#4444FF", outline="#4444FF"
                )

    def handle_hover(self, event):
        """Gère le survol de la souris"""
        if self.game_over or (self.ai_enabled and self.current_player == 'b'):
            return
            
        # Changer le curseur selon la position
        col = event.x // 80
        row = event.y // 80
        
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board[row][col]
            if piece and piece[0] == self.current_player:
                self.canvas.config(cursor="hand2")
            elif self.selected and (row, col) in self.possible_moves:
                self.canvas.config(cursor="target")
            else:
                self.canvas.config(cursor="")

    def handle_click(self, event):
        """Gère les clics sur l'échiquier"""
        if self.game_over or (self.ai_enabled and self.current_player == 'b'):
            return

        col = event.x // 80
        row = event.y // 80
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        piece = self.board[row][col]

        if self.selected:
            if (row, col) in self.possible_moves:
                # Effectuer le mouvement
                self.make_move(*self.selected, row, col)
                self.selected = None
                self.possible_moves = []
                self.current_player = 'b' if self.current_player == 'w' else 'w'
                self.update_status()
                self.draw_board()
                
                # Vérifier les conditions de fin
                if self.check_game_end():
                    return
                
                # Tour de l'IA
                if self.ai_enabled and self.current_player == 'b':
                    self.root.after(500, self.ai_move)
            else:
                # Désélectionner ou sélectionner une nouvelle pièce
                if piece and piece[0] == self.current_player:
                    self.selected = (row, col)
                    self.possible_moves = self.get_legal_moves(row, col)
                else:
                    self.selected = None
                    self.possible_moves = []
                self.draw_board()
        elif piece and piece[0] == self.current_player:
            # Sélectionner une pièce
            self.selected = (row, col)
            self.possible_moves = self.get_legal_moves(row, col)
            self.draw_board()

    def make_move(self, sr, sc, dr, dc):
        """Effectue un mouvement et l'ajoute à l'historique"""
        piece = self.board[sr][sc]
        captured = self.board[dr][dc]
        
        # Sauvegarder le mouvement dans l'historique
        move = {
            'from': (sr, sc),
            'to': (dr, dc),
            'piece': piece,
            'captured': captured
        }
        self.move_history.append(move)
        
        # Effectuer le mouvement
        self.move_piece(sr, sc, dr, dc)

    def move_piece(self, sr, sc, dr, dc):
        """Déplace une pièce sur l'échiquier"""
        piece = self.board[sr][sc]
        self.board[dr][dc] = piece
        self.board[sr][sc] = ""
        
        # Promotion des pions
        if piece[1] == 'P' and (dr == 0 or dr == 7):
            self.board[dr][dc] = piece[0] + 'Q'

    def get_all_legal_moves(self, color):
        """Retourne tous les coups légaux pour une couleur"""
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] and self.board[r][c][0] == color:
                    for dr, dc in self.get_legal_moves(r, c):
                        moves.append((r, c, dr, dc))
        return moves

    def get_legal_moves(self, row, col):
        """Retourne les coups légaux pour une pièce donnée"""
        piece = self.board[row][col]
        if not piece:
            return []
        color = piece[0]
        raw_moves = self.get_raw_moves(row, col)
        legal_moves = []

        for dr, dc in raw_moves:
            # Simuler le mouvement
            captured = self.board[dr][dc]
            self.board[dr][dc] = piece
            self.board[row][col] = ""
            
            # Vérifier si le roi est en échec
            if not self.is_in_check(color):
                legal_moves.append((dr, dc))
            
            # Annuler le mouvement
            self.board[row][col] = piece
            self.board[dr][dc] = captured
            
        return legal_moves

    def get_raw_moves(self, row, col):
        """Retourne les mouvements bruts possibles pour une pièce"""
        piece = self.board[row][col]
        if not piece:
            return []
        moves = []
        color, kind = piece[0], piece[1]
        direction = -1 if color == 'w' else 1
        enemy = 'b' if color == 'w' else 'w'

        def inside(r, c):
            return 0 <= r < 8 and 0 <= c < 8

        if kind == 'P':
            if inside(row + direction, col) and self.board[row + direction][col] == "":
                moves.append((row + direction, col))
                if (row == 6 and color == 'w') or (row == 1 and color == 'b'):
                    if self.board[row + 2 * direction][col] == "":
                        moves.append((row + 2 * direction, col))
            
            for dc in [-1, 1]:
                r, c = row + direction, col + dc
                if inside(r, c) and self.board[r][c] and self.board[r][c][0] == enemy:
                    moves.append((r, c))

        elif kind == 'N':
            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                           (1, -2), (1, 2), (2, -1), (2, 1)]:
                r, c = row + dr, col + dc
                if inside(r, c) and (not self.board[r][c] or self.board[r][c][0] == enemy):
                    moves.append((r, c))

        elif kind in ['B', 'R', 'Q']:
            directions = []
            if kind in ['B', 'Q']:  
                directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            if kind in ['R', 'Q']:  
                directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while inside(r, c):
                    if not self.board[r][c]:
                        moves.append((r, c))
                    elif self.board[r][c][0] == enemy:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif kind == 'K':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if inside(r, c) and (not self.board[r][c] or self.board[r][c][0] == enemy):
                        moves.append((r, c))

        return moves

    def is_in_check(self, color):
        """Vérifie si le roi d'une couleur est en échec"""
        king_pos = [(r, c) for r in range(8) for c in range(8) if self.board[r][c] == color + 'K']
        if not king_pos:
            return True
        kr, kc = king_pos[0]
        
        enemy = 'b' if color == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] and self.board[r][c][0] == enemy:
                    if (kr, kc) in self.get_raw_moves(r, c):
                        return True
        return False

    def is_checkmate(self, color):
        """Vérifie si c'est échec et mat"""
        if not self.is_in_check(color):
            return False
        return len(self.get_all_legal_moves(color)) == 0

    def is_stalemate(self, color):
        """Vérifie si c'est pat"""
        if self.is_in_check(color):
            return False
        return len(self.get_all_legal_moves(color)) == 0

    def check_game_end(self):
        if self.is_checkmate(self.current_player):
            winner = "Noirs" if self.current_player == 'w' else "Blancs"
            self.game_over = True
            self.status_label.config(text=f"Échec et mat ! {winner} gagnent !", fg='#FF4444')
            messagebox.showinfo("Fin de partie", f"Échec et mat !\n{winner} remportent la partie !")
            return True
        elif self.is_stalemate(self.current_player):
            self.game_over = True
            self.status_label.config(text="Pat ! Match nul !", fg='#FFA500')
            messagebox.showinfo("Fin de partie", "Pat ! La partie se termine par un match nul.")
            return True
        return False

    def update_status(self):
        if not self.game_over:
            player_name = "Blancs" if self.current_player == 'w' else "Noirs"
            if self.is_in_check(self.current_player):
                self.status_label.config(text=f"Tour des {player_name} - ÉCHEC !", fg='#FF4444')
            else:
                self.status_label.config(text=f"Tour des {player_name}", fg='#CCCCCC')

    def evaluate_board(self):
        score = 0
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece:
                    val = PIECE_VALUES.get(piece[1], 0)
                    pos_val = self.get_position_value(piece, r, c)
                    
                    if piece[0] == 'b':
                        score += val + pos_val
                    else:
                        score -= val + pos_val
        
        for r, c in CENTER_SQUARES:
            piece = self.board[r][c]
            if piece:
                if piece[0] == 'b':
                    score += 10
                else:
                    score -= 10
        
        if self.is_in_check('b'):
            score -= 50
        if self.is_in_check('w'):
            score += 50
        
        return score

    def get_position_value(self, piece, row, col):
        kind = piece[1]
        color = piece[0]
        
        if color == 'w':
            row = 7 - row
        
        if kind == 'P':
            return PAWN_TABLE[row][col] if 0 <= row < 8 and 0 <= col < 8 else 0
        elif kind == 'N':
            return KNIGHT_TABLE[row][col] if 0 <= row < 8 and 0 <= col < 8 else 0
        elif kind == 'B':
            return BISHOP_TABLE[row][col] if 0 <= row < 8 and 0 <= col < 8 else 0
        
        return 0

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate_board(), None

        color = 'b' if maximizing else 'w'
        legal_moves = self.get_all_legal_moves(color)

        if not legal_moves:
            if self.is_in_check(color):
                return (-999999 if maximizing else 999999), None
            else:
                return 0, None

        best_move = None

        if maximizing:
            max_eval = float('-inf')
            random.shuffle(legal_moves)
            
            for move in legal_moves:
                sr, sc, dr, dc = move
                piece = self.board[sr][sc]
                captured = self.board[dr][dc]

                self.board[dr][dc] = piece
                self.board[sr][sc] = ""

                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)

    
                self.board[sr][sc] = piece
                self.board[dr][dc] = captured

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Élagage Alpha-Beta

            return max_eval, best_move

        else:
            min_eval = float('inf')
            random.shuffle(legal_moves)
            
            for move in legal_moves:
                sr, sc, dr, dc = move
                piece = self.board[sr][sc]
                captured = self.board[dr][dc]

                self.board[dr][dc] = piece
                self.board[sr][sc] = ""

                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)

                self.board[sr][sc] = piece
                self.board[dr][dc] = captured

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break 

            return min_eval, best_move

    def coord_to_alg(self, row, col):
        files = 'abcdefgh'
        ranks = '87654321'
        return files[col] + ranks[row]

    def ai_move(self):
        if self.is_thinking or self.game_over:
            return
            
        self.is_thinking = True
        self.thinking_label.config(text="🤖 ZyvaAI réfléchit...")
        self.root.update()

        def worker():
            try:
                start_time = time.time()
                depth = 5  
                
            
                piece_count = sum(1 for r in range(8) for c in range(8) if self.board[r][c])
                if piece_count <= 12:
                    depth = 5
                elif piece_count <= 8:
                    depth = 6
                
                score, move = self.minimax(depth, float('-inf'), float('inf'), True)
                
                elapsed = time.time() - start_time
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
                
                if move:
                    sr, sc, dr, dc = move
                    piece_name = self.get_piece_name(self.board[sr][sc])
                    move_notation = f"{piece_name} {self.coord_to_alg(sr, sc)} → {self.coord_to_alg(dr, dc)}"
                    
                    self.make_move(sr, sc, dr, dc)
                    print(f"ZyvaAI a joué : {move_notation} (Score: {score})")
                    
                    # Mettre à jour l'interface dans le thread principal
                    self.root.after(0, self.after_ai_move)
                else:
                    print("ZyvaAI n'a trouvé aucun coup valide")
                    self.root.after(0, self.after_ai_move)
                    
            except Exception as e:
                print(f"Erreur de l'IA: {e}")
                self.root.after(0, self.after_ai_move)

        threading.Thread(target=worker, daemon=True).start()

    def after_ai_move(self):
        """Actions à effectuer après le coup de l'IA"""
        self.is_thinking = False
        self.thinking_label.config(text="")
        self.current_player = 'w'
        self.update_status()
        self.draw_board()
        self.check_game_end()

    def get_piece_name(self, piece):
        """Retourne le nom français de la pièce"""
        names = {
            'P': 'Pion', 'R': 'Tour', 'N': 'Cavalier',
            'B': 'Fou', 'Q': 'Dame', 'K': 'Roi'
        }
        return names.get(piece[1], piece[1])

    def new_game(self):
        """Commence une nouvelle partie"""
        response = messagebox.askyesno(
            "Nouvelle partie", 
            "Êtes-vous sûr de vouloir commencer une nouvelle partie ?"
        )
        if response:
            self.board = self.create_board()
            self.selected = None
            self.possible_moves = []
            self.current_player = 'w'
            self.is_thinking = False
            self.game_over = False
            self.move_history = []
            self.update_status()
            self.draw_board()
            
            if self.ai_enabled and self.current_player == 'b':
                self.root.after(1000, self.ai_move)

    def return_to_menu(self):
        if self.parent_app:
            self.root.destroy()
            self.parent_app.main_menu()
        else:
            self.root.destroy()