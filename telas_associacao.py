"""
Módulo de Associação Aluno-Sala
Responsável pela interface de associação e desassociação de alunos a salas
"""

import tkinter as tk
from tkinter import messagebox, ttk
import banco

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
    salas_nomes = list(salas_dict.values())
    salas_ids = list(salas_dict.keys())

    sala_selecionada_var = tk.StringVar(select_frame)
    if salas_nomes:
        sala_selecionada_var.set(salas_nomes[0])

    sala_menu = ttk.Combobox(select_frame, textvariable=sala_selecionada_var, values=salas_nomes, state="readonly", width=40)
    sala_menu.grid(row=1, column=1, padx=5, pady=5)

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
            messagebox.showwarning("Aviso", "Selecione um aluno e uma sala.")
            return

        aluno = banco.buscar_aluno_por_id(aluno_id)
        sala = banco.buscar_sala_por_id(sala_id)
        curso_aluno = aluno[4] if aluno and len(aluno) > 4 else ''
        curso_sala = sala[3] if sala and len(sala) > 3 else ''
        if curso_aluno and curso_sala and curso_aluno != curso_sala:
            messagebox.showerror("Erro", f"Aluno do curso '{curso_aluno}' não pode ser associado à sala do curso '{curso_sala}'.")
            return

        if banco.associar_aluno_sala(aluno_id, sala_id):
            messagebox.showinfo("Sucesso", "Aluno associado à sala com sucesso!")
        else:
            messagebox.showerror("Erro", "Aluno já está associado a esta sala.")

    def desassociar():
        aluno_id, sala_id = get_ids()
        if aluno_id is None or sala_id is None:
            messagebox.showwarning("Aviso", "Selecione um aluno e uma sala.")
            return

        if banco.desassociar_aluno_sala(aluno_id, sala_id):
            messagebox.showinfo("Sucesso", "Aluno desassociado da sala com sucesso!")
        else:
            messagebox.showerror("Erro", "Aluno não está associado a esta sala.")

    action_frame = tk.Frame(content_frame, bg="#20232a")
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="Associar", command=associar, bg="#98c379", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Desassociar", command=desassociar, bg="#e06c75", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
