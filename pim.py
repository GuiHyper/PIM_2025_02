import tkinter as tk
from tkinter import messagebox, ttk
import threading
import webbrowser
import time
import os
import banco

import telas_alunos
import telas_salas
import telas_associacao
import telas_notas

DB_NAME = "sistema_academico.db"
banco.DB_NAME = DB_NAME
banco.inicializador_do_banco()

flask_thread = None

content_frame = None
root = None

def on_closing(root):
    """Manipulador de fechamento para a janela principal."""
    if flask_thread and flask_thread.is_alive():
        pass 
    root.destroy()


def iniciar_tela_principal():
    """Cria e exibe a tela principal do sistema acadêmico."""
    global root, content_frame
    root = tk.Tk()
    root.title("Sistema Acadêmico - Gerenciamento")
    root.geometry("800x600")
    root.config(bg="#282c34")

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    tk.Label(root, text="Sistema Acadêmico", font=("Arial", 24, "bold"), fg="#61dafb",
             bg="#282c34").pack(pady=20)
    
    frame_botoes = tk.Frame(root, bg="#282c34")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Gerenciar Alunos", command=lambda: telas_alunos.abrir_tela_alunos(content_frame), 
              bg="#98c379", fg="black",
              font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
    
    tk.Button(frame_botoes, text="Gerenciar Salas", command=lambda: telas_salas.abrir_tela_salas(content_frame), 
              bg="#e5c07b", fg="black",
              font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)

    content_frame = tk.Frame(root, bg="#20232a")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    telas_alunos.abrir_tela_alunos(content_frame)

    root.mainloop()


if __name__ == "__main__":
    iniciar_tela_principal()
