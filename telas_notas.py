"""
Módulo de Atribuição de Notas
Responsável pela interface de atribuição de notas aos alunos em cada sala
"""

import tkinter as tk
from tkinter import messagebox, ttk
from notifications import toast_success, toast_error, toast_warning
import banco

sala_nota_selecionada_var = None
entry_np1 = None
entry_np2 = None
entry_trabalho = None
tree_notas = None


def abrir_tela_atribuir_notas(content_frame):
    """Abre a tela para atribuir notas aos alunos de uma sala."""
    global sala_nota_selecionada_var, entry_np1, entry_np2, entry_trabalho, tree_notas
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Atribuição de Notas", font=("Arial", 18, "bold"), fg="white",
             bg="#20232a").pack(pady=10)

    select_frame = tk.Frame(content_frame, bg="#20232a")
    select_frame.pack(pady=10)

    tk.Label(select_frame, text="Selecionar Sala:", bg="#20232a", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    salas = banco.buscar_salas()
    salas_dict = {sala[0]: f"{sala[1]} (Cap: {sala[2]})" for sala in salas}
    salas_nomes = list(salas_dict.values())
    
    sala_nota_selecionada_var = tk.StringVar(select_frame)
    
    sala_menu = ttk.Combobox(select_frame, textvariable=sala_nota_selecionada_var, values=salas_nomes, state="readonly", width=40)
    sala_menu.grid(row=0, column=1, padx=5, pady=5)
    
    def carregar_alunos_e_notas(event=None):
        sala_nome_selecionada = sala_nota_selecionada_var.get()
        sala_id = None
        for id, nome in salas_dict.items():
            if nome == sala_nome_selecionada:
                sala_id = id
                break
        
        if sala_id is None:
            return

        for item in tree_notas.get_children():
            tree_notas.delete(item)

        alunos_na_sala = banco.buscar_alunos_por_sala(sala_id)
        
        for aluno in alunos_na_sala:
            aluno_id = aluno[0]
            nome_aluno = aluno[1]
            np1, np2, trabalho, media = banco.buscar_notas_aluno_sala(aluno_id, sala_id)
            
            if media >= 7:
                status = "APROVADO"
                tag = "aprovado"
            else:
                status = "REPROVADO"
                tag = "reprovado"
            
            tree_notas.insert("", tk.END, values=(aluno_id, nome_aluno, np1, np2, trabalho, media, status), tags=(tag,))

    sala_menu.bind("<<ComboboxSelected>>", carregar_alunos_e_notas)

    tree_notas = ttk.Treeview(content_frame, columns=("ID", "Nome", "NP1", "NP2", "Trabalho", "Média", "Status"), show="headings")
    tree_notas.heading("ID", text="ID")
    tree_notas.heading("Nome", text="Nome do Aluno")
    tree_notas.heading("NP1", text="NP1 (Peso 4)")
    tree_notas.heading("NP2", text="NP2 (Peso 4)")
    tree_notas.heading("Trabalho", text="Trabalho (Peso 2)")
    tree_notas.heading("Média", text="Média")
    tree_notas.heading("Status", text="Status")
    
    tree_notas.column("ID", width=50, anchor="center")
    tree_notas.column("Nome", width=150)
    tree_notas.column("NP1", width=80, anchor="center")
    tree_notas.column("NP2", width=80, anchor="center")
    tree_notas.column("Trabalho", width=100, anchor="center")
    tree_notas.column("Média", width=80, anchor="center")
    tree_notas.column("Status", width=100, anchor="center")
    
    tree_notas.tag_configure("aprovado", foreground="#00aa00", background="#20232a")
    tree_notas.tag_configure("reprovado", foreground="#ff6b6b", background="#20232a")
    
    tree_notas.pack(fill=tk.BOTH, expand=True, pady=10)

    atribuir_frame = tk.Frame(content_frame, bg="#20232a")
    atribuir_frame.pack(pady=10)

    tk.Label(atribuir_frame, text="NP1:", bg="#20232a", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_np1 = tk.Entry(atribuir_frame, width=5)
    entry_np1.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(atribuir_frame, text="NP2:", bg="#20232a", fg="white").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_np2 = tk.Entry(atribuir_frame, width=5)
    entry_np2.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(atribuir_frame, text="Trabalho:", bg="#20232a", fg="white").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    entry_trabalho = tk.Entry(atribuir_frame, width=5)
    entry_trabalho.grid(row=0, column=5, padx=5, pady=5)

    def atribuir_notas_selecionadas():
        selected_item = tree_notas.focus()
        if not selected_item:
            toast_warning(None, "Selecione um aluno na lista.")
            return

        aluno_id = tree_notas.item(selected_item, 'values')[0]
        
        np1_str = entry_np1.get()
        np2_str = entry_np2.get()
        trabalho_str = entry_trabalho.get()
        
        if not np1_str or not np2_str or not trabalho_str:
            toast_warning(None, "Preencha todas as notas (NP1, NP2, Trabalho).")
            return

        try:
            np1 = float(np1_str)
            np2 = float(np2_str)
            trabalho = float(trabalho_str)
            
            if not (0.0 <= np1 <= 10.0 and 0.0 <= np2 <= 10.0 and 0.0 <= trabalho <= 10.0):
                raise ValueError
        except ValueError:
            toast_error(None, "Notas inválidas. Digite números entre 0.0 e 10.0.")
            return

        sala_nome_selecionada = sala_nota_selecionada_var.get()
        sala_id = None
        for id, nome in salas_dict.items():
            if nome == sala_nome_selecionada:
                sala_id = id
                break
        
        if sala_id is None:
            toast_error(None, "Sala não selecionada.")
            return

        if banco.atribuir_notas(aluno_id, sala_id, np1, np2, trabalho):
            media = banco.calcular_media(np1, np2, trabalho)
            if media >= 7:
                toast_success(None, f"Notas atribuídas. Média calculada: {media}\n✓ ALUNO APROVADO!")
            else:
                toast_success(None, f"Notas atribuídas. Média calculada: {media}\n✗ Aluno reprovado.")
            entry_np1.delete(0, tk.END)
            entry_np2.delete(0, tk.END)
            entry_trabalho.delete(0, tk.END)
            carregar_alunos_e_notas() 
        else:
            toast_error(None, "Não foi possível atribuir as notas.")

    tk.Button(atribuir_frame, text="Atribuir Notas", command=atribuir_notas_selecionadas, bg="#98c379", fg="black",
              font=("Arial", 10, "bold")).grid(row=0, column=6, padx=10, pady=5)
