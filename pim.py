"""
Sistema Acadêmico - Aplicação Principal
Gerencia a interface principal do sistema acadêmico com navegação entre telas
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import webbrowser
import time
import os
import banco
from chatbot import app as chatbot_app # Importa a aplicação Flask do chatbot

# Importa os módulos de telas
import telas_alunos
import telas_salas
import telas_associacao
import telas_notas

# --- Configurações e Variáveis Globais ---
DB_NAME = "sistema_academico.db"
banco.DB_NAME = DB_NAME # Garante que o banco.py use o nome correto
banco.inicializador_do_banco() # Inicializa o banco de dados

# Variável global para o servidor Flask
flask_thread = None

# Variável global para o frame de conteúdo
content_frame = None
root = None

# --- Funções de Suporte ---

def start_flask_server():
    """Inicia o servidor Flask em uma thread separada."""
    global flask_thread
    # O Flask roda na porta 5000 por padrão.
    # O uso de `debug=False` e `use_reloader=False` é essencial para threads.
    try:
        chatbot_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Erro ao iniciar o servidor Flask: {e}")

def abrir_chatbot():
    """Inicia o servidor Flask (se não estiver rodando) e abre o chatbot no navegador."""
    global flask_thread
    if flask_thread is None or not (flask_thread.is_alive() if flask_thread else False):
        # Inicia o servidor Flask em uma thread separada
        flask_thread = threading.Thread(target=start_flask_server)
        flask_thread.daemon = True # Permite que a thread seja encerrada quando o processo principal terminar
        flask_thread.start()
        
        # Espera um pouco para o servidor iniciar
        time.sleep(1) 
        
        # Abre o navegador para a URL do chatbot
        webbrowser.open("http://127.0.0.1:5000")
    else:
        # Se já estiver rodando, apenas abre o navegador
        webbrowser.open("http://127.0.0.1:5000")

def on_closing(root):
    """Manipulador de fechamento para a janela principal."""
    if flask_thread and flask_thread.is_alive():
        # A thread é um daemon, então será encerrada com o processo principal.
        pass 
    root.destroy()

# --- Funções de Interface (Telas) ---

def iniciar_tela_principal():
    """Cria e exibe a tela principal do sistema acadêmico."""
    global root, content_frame
    root = tk.Tk()
    root.title("Sistema Acadêmico - Gerenciamento")
    root.geometry("800x600")
    root.config(bg="#282c34")

    # Manipulador de fechamento
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Título
    tk.Label(root, text="Sistema Acadêmico", font=("Arial", 24, "bold"), fg="#61dafb",
             bg="#282c34").pack(pady=20)
    
    # Frame para os botões de navegação
    frame_botoes = tk.Frame(root, bg="#282c34")
    frame_botoes.pack(pady=10)

    # Botões de Navegação
    tk.Button(frame_botoes, text="Gerenciar Alunos", command=lambda: telas_alunos.abrir_tela_alunos(content_frame), 
              bg="#98c379", fg="black",
              font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
    
    tk.Button(frame_botoes, text="Gerenciar Salas", command=lambda: telas_salas.abrir_tela_salas(content_frame), 
              bg="#e5c07b", fg="black",
              font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
    
    tk.Button(frame_botoes, text="Chatbot Acadêmico", command=abrir_chatbot, bg="#c678dd", fg="black",
              font=("Arial", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)

    # Frame para o conteúdo dinâmico
    content_frame = tk.Frame(root, bg="#20232a")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Exibe a tela de alunos por padrão
    telas_alunos.abrir_tela_alunos(content_frame)

    root.mainloop()

# --- Início da Aplicação ---

if __name__ == "__main__":
    iniciar_tela_principal()
