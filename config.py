# Configuration et constantes pour le jeu d'échecs
# Fichier config.py

# Couleurs de l'interface
COLORS = {
    'bg_main': '#2b2b2b',
    'bg_secondary': '#1a1a1a',
    'text_primary': '#CCCCCC',
    'text_secondary': '#888888',
    'accent_gold': '#FFD700',
    'accent_green': '#4CAF50',
    'accent_blue': '#2196F3',
    'accent_orange': '#FF9800',
    'accent_red': '#f44336',
    'board_light': '#F0D9B5',
    'board_dark': '#B58863',
    'highlight_selected': '#FFD700',
    'highlight_move': '#4444FF',
    'highlight_capture': '#FF4444',
    'check_warning': '#FF4444'
}

# Configuration de l'IA
AI_CONFIG = {
    'default_depth': 3,
    'endgame_depth': 7,
    'late_endgame_depth': 6,
    'endgame_piece_threshold': 12,
    'late_endgame_piece_threshold': 8,
    'min_thinking_time': 0.5,  # secondes
    'max_thinking_time': 10.0  # secondes
}

# Configuration de l'interface
UI_CONFIG = {
    'board_size': 640,
    'square_size': 80,
    'piece_font_size': 36,
    'title_font_size': 36,
    'button_font_size': 16,
    'status_font_size': 14,
    'window_width': 800,
    'window_height': 700,
    'menu_width': 600,
    'menu_height': 500
}


MESSAGES = {
    'game_title': '♔ CHESS MASTER ♛',
    'game_subtitle': 'Jeu d\'échecs avec IA avancée',
    'playing_title': '♔ PARTIE D\'ÉCHECS ♛',
    'white_turn': 'Tour des Blancs',
    'black_turn': 'Tour des Noirs',
    'check_warning': 'ÉCHEC !',
    'ai_thinking': '🤖 ZyvaAI réfléchit...',
    'checkmate': 'Échec et mat ! T\'es nul,',
    'stalemate': 'Pat ! Match nul !',
    'new_game_confirm': 'Êtes vous sur de vouloir commencer une nouvelle partie ?',
    'game_instructions': 'Utilisez la souris pour déplacer les pièces'
}


MENU_BUTTONS = [
    {
        'text': '🤖 Solo (vs ZyvaAI Chess)',
        'color': COLORS['accent_green'],
        'command': 'start_solo'
    },
    {
        'text': '👥 Multijoueur (2 joueurs)',
        'color': COLORS['accent_blue'],
        'command': 'start_multiplayer'
    },
    {
        'text': 'ℹ️ Crédits',
        'color': COLORS['accent_orange'],
        'command': 'show_credits'
    },
    {
        'text': '❌ Quitter',
        'color': COLORS['accent_red'],
        'command': 'quit'
    }
]

CREDITS_INFO = {
    'title': '🏆 CRÉDITS 🏆',
    'developer': 'Zyvaouech (Kasper)',
    'date': '1er juillet 2025',
    'technologies': [
        '• Python 3.x',
        '• Tkinter (Interface graphique)',
        '• Algorithme Minimax avec élagage Alpha-Beta',
        '• Threading pour l\'IA asynchrone',
        '• Tables de position pour l\'évaluation'
    ],
    'features': [
        '• IA avancée avec évaluation de position',
        '• Interface graphique moderne et intuitive',
        '• Mode solo et multijoueur',
        '• Vérification complète des règles d\'échecs',
        '• Détection d\'échec et mat, pat',
        '• Historique des coups',
        '• Différents niveaux de difficulté selon la situation'
    ]
}

# Configuration des sons (pour extension future)
SOUNDS_CONFIG = {
    'enabled': False,
    'move_sound': 'sounds/move.wav',
    'capture_sound': 'sounds/capture.wav',
    'check_sound': 'sounds/check.wav',
    'checkmate_sound': 'sounds/checkmate.wav'
}


SAVE_CONFIG = {
    'enabled': False,
    'save_directory': 'saves/',
    'auto_save': True,
    'max_saves': 10
}