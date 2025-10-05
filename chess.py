import tkinter as tk
from tkinter import messagebox
from chess_engine import ChessGame


class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Échiquier")
        self.root.geometry("600x500")
        self.root.configure(bg='#2b2b2b')
        self.main_menu()
        self.root.mainloop()

    def main_menu(self):

        for widget in self.root.winfo_children():
            widget.destroy()


        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(expand=True, fill='both')

        title = tk.Label(
            main_frame, 
            text="♔ AI Chess Games ♛", 
            font=("Arial", 36, "bold"), 
            fg='#FFD700',
            bg='#2b2b2b'
        )
        title.pack(pady=30)

        subtitle = tk.Label(
            main_frame, 
            text="Codé pour Sacha et Cédric", 
            font=("Arial", 14, "italic"), 
            fg='#CCCCCC',
            bg='#2b2b2b'
        )
        subtitle.pack(pady=5)


        author = tk.Label(
            main_frame, 
            text="par Kasper", 
            font=("Arial", 12), 
            fg='#888888',
            bg='#2b2b2b'
        )
        author.pack(pady=5)

        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=40)


        button_style = {
            'font': ("Arial", 16, "bold"),
            'width': 22,
            'height': 2,
            'relief': 'raised',
            'bd': 3,
            'cursor': 'hand2'
        }

        solo_btn = tk.Button(
            button_frame, 
            text="🤖 Solo (vs ZyvaAI Chess)", 
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            command=self.start_solo,
            **button_style
        )
        solo_btn.pack(pady=8)

        multi_btn = tk.Button(
            button_frame, 
            text="👥 Multijoueur (2 joueurs)", 
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            command=self.start_multiplayer,
            **button_style
        )
        multi_btn.pack(pady=8)
        
        credit_btn = tk.Button(
            button_frame, 
            text="ℹ️ Crédits", 
            bg='#FF9800',
            fg='white',
            activebackground='#F57C00',
            command=self.show_credits,
            **button_style
        )
        credit_btn.pack(pady=8)

        # Bouton Quitter
        quit_btn = tk.Button(
            button_frame, 
            text="❌ Quitter", 
            bg='#f44336',
            fg='white',
            activebackground='#d32f2f',
            command=self.root.quit,
            **button_style
        )
        quit_btn.pack(pady=8)

        footer = tk.Label(
            main_frame, 
            text="Utilisez la souris pour sélectionner et déplacer les pièces", 
            font=("Arial", 10), 
            fg='#666666',
            bg='#2b2b2b'
        )
        footer.pack(side='bottom', pady=20)

    def start_solo(self):
        try:
            game_window = tk.Toplevel(self.root)
            game_window.title("♔ Échecs - Solo vs ZyvaAI ♛")
            game_window.geometry("800x770")
            game_window.configure(bg='#2b2b2b')
            

            game_window.transient(self.root)
            game_window.grab_set()
            
            ChessGame(game_window, ai_enabled=True, parent_app=self)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer la partie solo: {str(e)}")

    def start_multiplayer(self):

        try:
            game_window = tk.Toplevel(self.root)
            game_window.title("♔ Échecs - Multijoueur ♛")
            game_window.geometry("800x770")
            game_window.configure(bg='#2b2b2b')
            
            game_window.transient(self.root)
            game_window.grab_set()
            
            ChessGame(game_window, ai_enabled=False, parent_app=self)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer la partie multijoueur: {str(e)}")
        
    def show_credits(self):

        credits_window = tk.Toplevel(self.root)
        credits_window.title("Crédits")
        credits_window.geometry("500x600")
        credits_window.configure(bg='#2b2b2b')
        credits_window.transient(self.root)
        credits_window.grab_set()

     
        credits_frame = tk.Frame(credits_window, bg='#2b2b2b')
        credits_frame.pack(expand=True, fill='both', padx=20, pady=20)


        title_label = tk.Label(
            credits_frame, 
            text="🏆 CRÉDITS 🏆", 
            font=("Arial", 24, "bold"), 
            fg='#FFD700',
            bg='#2b2b2b'
        )
        title_label.pack(pady=20)


        dev_info = tk.Label(
            credits_frame,
            text="Développeur Principal:",
            font=("Arial", 14, "bold"),
            fg='#CCCCCC',
            bg='#2b2b2b'
        )
        dev_info.pack(pady=5)

        dev_name = tk.Label(
            credits_frame,
            text="Zyvaouech (Kasper)",
            font=("Arial", 16),
            fg='#4CAF50',
            bg='#2b2b2b'
        )
        dev_name.pack(pady=5)

        # Date de création
        date_label = tk.Label(
            credits_frame,
            text="Date de créatipn: 3 juillet 2025",
            font=("Arial", 12),
            fg='#888888',
            bg='#2b2b2b'
        )
        date_label.pack(pady=10)

        # Technologies utilisées
        tech_title = tk.Label(
            credits_frame,
            text="Algorithme utilisée:",
            font=("Arial", 14, "bold"),
            fg='#CCCCCC',
            bg='#2b2b2b'
        )
        tech_title.pack(pady=(20, 5))

        technologies = [
            "• Python 3.6.0",
            "• Tkinter (Screen avec image)",
            "• Algorithme Minimax",
            "• Trucs secrets.."
        ]

        for tech in technologies:
            tech_label = tk.Label(
                credits_frame,
                text=tech,
                font=("Arial", 11),
                fg='#AAAAAA',
                bg='#2b2b2b',
                anchor='w'
            )
            tech_label.pack(pady=2)

        features_title = tk.Label(
            credits_frame,
            text="Caractéristiques:",
            font=("Arial", 14, "bold"),
            fg='#CCCCCC',
            bg='#2b2b2b'
        )
        features_title.pack(pady=(20, 5))

        features = [
            "• IA avancée avec évaluation de position",
            "• Interface graphique intuitive",
            "• Mode solo et multijoueur",
            "• Vérification des coups légaux"
        ]

        for feature in features:
            feature_label = tk.Label(
                credits_frame,
                text=feature,
                font=("Arial", 11),
                fg='#AAAAAA',
                bg='#2b2b2b',
                anchor='w'
            )
            feature_label.pack(pady=2)


        close_btn = tk.Button(
            credits_frame,
            text="Fermer",
            font=("Arial", 12, "bold"),
            bg='#f44336',
            fg='white',
            activebackground='#d32f2f',
            command=credits_window.destroy,
            width=15,
            height=2,
            cursor='hand2'
        )
        close_btn.pack(pady=30)


if __name__ == "__main__":
    ChessApp()