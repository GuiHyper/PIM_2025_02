"""
Módulo de Gerenciamento de Salas
Responsável pela interface de cadastro, edição e exclusão de salas,
bem como visualização de alunos matriculados em cada sala com seus status de aprovação
"""

import tkinter as tk
from tkinter import messagebox, ttk
import banco

sala_id_selecionada = None
entry_nome_sala = None
entry_capacidade_sala = None
tree_salas = None
tree_alunos_sala = None
combobox_curso = None
sala_curso_var = None


def on_sala_selecionada(event):
    """Carrega os alunos da sala selecionada na treeview de alunos."""
    selected_item = tree_salas.focus()
    if selected_item:
        values = tree_salas.item(selected_item, 'values')
        sala_id = values[0]
        
        for item in tree_alunos_sala.get_children():
            tree_alunos_sala.delete(item)
        
        alunos = banco.buscar_alunos_por_sala(sala_id)
        
        for aluno in alunos:
            aluno_id = aluno[0]
            nome_aluno = aluno[1]
            matricula_aluno = aluno[2]
            
            np1, np2, trabalho, media = banco.buscar_notas_aluno_sala(aluno_id, sala_id)
            
            if media >= 7:
                status = "APROVADO"
                tag = "aprovado"
            else:
                status = "REPROVADO"
                tag = "reprovado"
            
            tree_alunos_sala.insert("", tk.END, values=(aluno_id, nome_aluno, matricula_aluno, media, status), tags=(tag,))
        
        limpar_campos_sala()
        entry_nome_sala.insert(0, values[1])
        entry_capacidade_sala.insert(0, values[2])
        # Se houver coluna de curso, o índice 3 existe
        if len(values) > 3:
            sala_curso_var.set(values[3])
        else:
            sala_curso_var.set("")
        sala_id_selecionada.set(values[0])


def abrir_tela_salas(content_frame):
    """Exibe a interface de gerenciamento de salas."""
    global sala_id_selecionada, entry_nome_sala, entry_capacidade_sala, tree_salas, tree_alunos_sala, sala_curso_var, combobox_curso
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    tk.Label(content_frame, text="Gerenciamento de Salas", font=("Arial", 18, "bold"), fg="white",
             bg="#20232a").pack(pady=10)

    form_frame = tk.Frame(content_frame, bg="#20232a")
    form_frame.pack(pady=10)

    sala_id_selecionada = tk.StringVar()
    
    tk.Label(form_frame, text="Nome da Sala:", bg="#20232a", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome_sala = tk.Entry(form_frame, width=30)
    entry_nome_sala.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Capacidade:", bg="#20232a", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_capacidade_sala = tk.Entry(form_frame, width=30)
    entry_capacidade_sala.grid(row=1, column=1, padx=5, pady=5)

    # Combobox de Cursos (para vincular sala a um curso)
    tk.Label(form_frame, text="Curso:", bg="#20232a", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    sala_curso_var = tk.StringVar()
    combobox_curso = ttk.Combobox(form_frame, textvariable=sala_curso_var, width=27, state='readonly')
    # Popular com cursos existentes na tabela aluno
    cursos = banco.buscar_cursos()
    combobox_curso['values'] = cursos
    combobox_curso.grid(row=2, column=1, padx=5, pady=5)

    action_frame = tk.Frame(content_frame, bg="#20232a")
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="Adicionar Sala", command=adicionar_ou_atualizar_sala, bg="#98c379", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Limpar Campos", command=limpar_campos_sala, bg="#e5c07b", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Excluir Selecionada", command=deletar_sala_selecionada, bg="#e06c75", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Atribuir Notas", command=lambda: __import__('telas_notas').abrir_tela_atribuir_notas(content_frame), 
              bg="#61dafb", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

    main_content_frame = tk.Frame(content_frame, bg="#20232a")
    main_content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    salas_frame = tk.Frame(main_content_frame, bg="#20232a")
    salas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    tk.Label(salas_frame, text="Salas Cadastradas", font=("Arial", 12, "bold"), fg="#61dafb", bg="#20232a").pack(pady=5)

    tree_salas = ttk.Treeview(salas_frame, columns=("ID", "Nome", "Capacidade", "Curso"), show="headings", height=15)
    tree_salas.heading("ID", text="ID")
    tree_salas.heading("Nome", text="Nome da Sala")
    tree_salas.heading("Capacidade", text="Capacidade")
    tree_salas.heading("Curso", text="Curso")
    
    tree_salas.column("ID", width=40, anchor="center")
    tree_salas.column("Nome", width=100)
    tree_salas.column("Capacidade", width=70, anchor="center")
    tree_salas.column("Curso", width=120)
    
    tree_salas.pack(fill=tk.BOTH, expand=True)
    tree_salas.bind("<<TreeviewSelect>>", on_sala_selecionada)

    alunos_sala_frame = tk.Frame(main_content_frame, bg="#20232a")
    alunos_sala_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    tk.Label(alunos_sala_frame, text="Alunos da Sala Selecionada", font=("Arial", 12, "bold"), fg="#98c379", bg="#20232a").pack(pady=5)

    tree_alunos_sala = ttk.Treeview(alunos_sala_frame, columns=("ID", "Nome", "Matrícula", "Média", "Status"), show="headings", height=15)
    tree_alunos_sala.heading("ID", text="ID")
    tree_alunos_sala.heading("Nome", text="Nome")
    tree_alunos_sala.heading("Matrícula", text="Matrícula")
    tree_alunos_sala.heading("Média", text="Média")
    tree_alunos_sala.heading("Status", text="Status")
    
    tree_alunos_sala.column("ID", width=30, anchor="center")
    tree_alunos_sala.column("Nome", width=100)
    tree_alunos_sala.column("Matrícula", width=70, anchor="center")
    tree_alunos_sala.column("Média", width=60, anchor="center")
    tree_alunos_sala.column("Status", width=80, anchor="center")
    
    tree_alunos_sala.tag_configure("aprovado", foreground="#00aa00", background="#20232a")
    tree_alunos_sala.tag_configure("reprovado", foreground="#ff6b6b", background="#20232a")
    
    tree_alunos_sala.pack(fill=tk.BOTH, expand=True)

    carregar_salas_na_treeview()


def carregar_salas_na_treeview():
    """Carrega os dados das salas na Treeview."""
    for item in tree_salas.get_children():
        tree_salas.delete(item)
    
    salas = banco.buscar_salas()
    for sala in salas:
        tree_salas.insert("", tk.END, values=sala)


def limpar_campos_sala():
    """Limpa os campos do formulário de sala."""
    sala_id_selecionada.set("")
    entry_nome_sala.delete(0, tk.END)
    entry_capacidade_sala.delete(0, tk.END)
    try:
        sala_curso_var.set("")
    except Exception:
        pass


def adicionar_ou_atualizar_sala():
    """Adiciona uma nova sala ou atualiza uma existente."""
    nome = entry_nome_sala.get()
    capacidade_str = entry_capacidade_sala.get()
    curso = sala_curso_var.get() if sala_curso_var else ""

    if not nome or not capacidade_str:
        messagebox.showwarning("Aviso", "Nome e Capacidade são obrigatórios.")
        return
    
    try:
        capacidade = int(capacidade_str)
    except ValueError:
        messagebox.showerror("Erro", "Capacidade deve ser um número inteiro.")
        return

    sala_id = sala_id_selecionada.get()
    if sala_id:
        if banco.atualizar_sala(sala_id, nome, capacidade, curso):
            messagebox.showinfo("Sucesso", "Sala atualizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Nome da Sala já cadastrado.")
    else:
        if banco.adicionar_sala(nome, capacidade, curso):
            messagebox.showinfo("Sucesso", "Sala adicionada com sucesso!")
        else:
            messagebox.showerror("Erro", "Nome da Sala já cadastrado.")

    limpar_campos_sala()
    carregar_salas_na_treeview()


def deletar_sala_selecionada():
    """Deleta a sala selecionada."""
    selected_item = tree_salas.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione uma sala para excluir.")
        return

    sala_id = tree_salas.item(selected_item, 'values')[0]
    
    if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a sala ID {sala_id}?"):
        if banco.deletar_sala(sala_id):
            messagebox.showinfo("Sucesso", "Sala excluída com sucesso.")
            try:
                for item in tree_alunos_sala.get_children():
                    tree_alunos_sala.delete(item)
            except Exception:
                pass

            limpar_campos_sala()
            carregar_salas_na_treeview()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir a sala.")
