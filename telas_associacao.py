"""
Módulo de Associação Aluno-Sala
Responsável pela interface de associação e desassociação de alunos a salas
"""

import tkinter as tk
from tkinter import messagebox, ttk
import banco
from notifications import toast_success, toast_error, toast_warning

aluno_selecionado_var = None
sala_selecionada_var = None


def abrir_tela_associacao_aluno_sala(content_frame):
    """Abre a tela para associar alunos a salas."""
    global aluno_selecionado_var, sala_selecionada_var
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Associar Aluno a Sala", font=("Arial", 18, "bold"), fg="white",
             bg="#20232a").pack(pady=10)

    select_frame = tk.Frame(content_frame, bg="#20232a")
    select_frame.pack(pady=10)

    tk.Label(select_frame, text="Aluno:", bg="#20232a", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    alunos = banco.buscar_alunos()
    alunos_dict = {aluno[0]: f"{aluno[1]} ({aluno[2]})" for aluno in alunos}
    alunos_nomes = list(alunos_dict.values())
    alunos_ids = list(alunos_dict.keys())
    
    aluno_selecionado_var = tk.StringVar(select_frame)
    if alunos_nomes:
        aluno_selecionado_var.set(alunos_nomes[0])
    
    aluno_menu = ttk.Combobox(select_frame, textvariable=aluno_selecionado_var, values=alunos_nomes, state="readonly", width=40)
    aluno_menu.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(select_frame, text="Sala:", bg="#20232a", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    salas = banco.buscar_salas()
    salas_dict = {sala[0]: f"{sala[1]} (Cap: {sala[2]})" for sala in salas}
    
    sala_selecionada_var = tk.StringVar(select_frame)
    sala_menu = ttk.Combobox(select_frame, textvariable=sala_selecionada_var, state="readonly", width=40)
    sala_menu.grid(row=1, column=1, padx=5, pady=5)

    action_frame = tk.Frame(content_frame, bg="#20232a")
    action_frame.pack(pady=10)

    salas_associadas_frame = tk.Frame(content_frame, bg="#20232a")
    salas_associadas_frame.pack(pady=10, fill=tk.BOTH, expand=False)
    
    tk.Label(salas_associadas_frame, text="Salas Associadas:", font=("Arial", 12, "bold"), fg="#61dafb",
             bg="#20232a").pack(pady=5, padx=5, anchor="w")
    
    salas_lista_frame = tk.Frame(salas_associadas_frame, bg="#20232a")
    salas_lista_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

    def carregar_salas_associadas(aluno_id):
        """Carrega e exibe as salas associadas ao aluno."""
        for widget in salas_lista_frame.winfo_children():
            widget.destroy()
        
        if aluno_id is None:
            tk.Label(salas_lista_frame, text="Nenhuma sala associada", bg="#20232a", fg="#888888", 
                    font=("Arial", 10)).pack(pady=10)
            return
        
        salas_associadas = banco.buscar_salas_por_aluno(aluno_id)
        
        if not salas_associadas:
            tk.Label(salas_lista_frame, text="Nenhuma sala associada", bg="#20232a", fg="#888888", 
                    font=("Arial", 10)).pack(pady=10)
            return
        
        for sala in salas_associadas:
            sala_id = sala[0]
            sala_nome = sala[1]
            
            sala_frame = tk.Frame(salas_lista_frame, bg="#2d2d2d")
            sala_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(sala_frame, text=sala_nome, bg="#2d2d2d", fg="white", 
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            
            tk.Button(sala_frame, text="✕", command=lambda sid=sala_id, aid=aluno_id: remover_associacao(aid, sid), 
                     bg="#e06c75", fg="black", font=("Arial", 10, "bold"), width=3).pack(side=tk.RIGHT, padx=5, pady=5)
    
    def remover_associacao(aluno_id, sala_id):
        """Remove a associação entre aluno e sala."""
        if banco.desassociar_aluno_sala(aluno_id, sala_id):
            toast_success(None, "Aluno desassociado da sala com sucesso!")
            carregar_salas_associadas(aluno_id)
        else:
            toast_error(None, "Erro ao desassociar aluno da sala.")

    def atualizar_salas_por_aluno(event=None):
        """Atualiza a lista de salas de acordo com o curso do aluno selecionado."""
        aluno_nome_selecionado = aluno_selecionado_var.get()
        
        aluno_id = None
        for id, nome in alunos_dict.items():
            if nome == aluno_nome_selecionado:
                aluno_id = id
                break
        
        if aluno_id is None:
            sala_menu['values'] = []
            sala_selecionada_var.set("")
            carregar_salas_associadas(None)
            return
        
        aluno = banco.buscar_aluno_por_id(aluno_id)
        if not aluno:
            sala_menu['values'] = []
            sala_selecionada_var.set("")
            carregar_salas_associadas(None)
            return
        
        curso_aluno = aluno[4] if len(aluno) > 4 else ''
        
        salas_filtradas = {}
        for sala_id, sala_nome in salas_dict.items():
            sala = banco.buscar_sala_por_id(sala_id)
            if sala:
                curso_sala = sala[3] if len(sala) > 3 else ''
                if curso_aluno and curso_sala and curso_aluno == curso_sala:
                    salas_filtradas[sala_id] = sala_nome
        
        salas_nomes_filtradas = list(salas_filtradas.values())
        sala_menu['values'] = salas_nomes_filtradas
        
        if salas_nomes_filtradas:
            sala_menu.current(0)
        else:
            sala_selecionada_var.set("")
        
        carregar_salas_associadas(aluno_id)
    
    aluno_menu.bind("<<ComboboxSelected>>", atualizar_salas_por_aluno)
    
    atualizar_salas_por_aluno()

    def get_ids():
        aluno_nome_selecionado = aluno_selecionado_var.get()
        sala_nome_selecionada = sala_selecionada_var.get()
        
        aluno_id = None
        for id, nome in alunos_dict.items():
            if nome == aluno_nome_selecionado:
                aluno_id = id
                break
        
        sala_id = None
        for id, nome in salas_dict.items():
            if nome == sala_nome_selecionada:
                sala_id = id
                break
        
        return aluno_id, sala_id

    def associar():
        aluno_id, sala_id = get_ids()
        if aluno_id is None or sala_id is None:
            toast_warning(None, "Selecione um aluno e uma sala.")
            return

        aluno = banco.buscar_aluno_por_id(aluno_id)
        sala = banco.buscar_sala_por_id(sala_id)
        curso_aluno = aluno[4] if aluno and len(aluno) > 4 else ''
        curso_sala = sala[3] if sala and len(sala) > 3 else ''
        if curso_aluno and curso_sala and curso_aluno != curso_sala:
            toast_error(None, f"Aluno do curso '{curso_aluno}' não pode ser associado à sala do curso '{curso_sala}'.")
            return

        if banco.associar_aluno_sala(aluno_id, sala_id):
            toast_success(None, "Aluno associado à sala com sucesso!")
            carregar_salas_associadas(aluno_id)
        else:
            toast_error(None, "Aluno já está associado a esta sala.")

    tk.Button(action_frame, text="Associar", command=associar, bg="#98c379", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
