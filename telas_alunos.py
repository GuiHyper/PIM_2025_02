"""
Módulo de Gerenciamento de Alunos
Responsável pela interface de cadastro, edição e exclusão de alunos
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import banco

# Variáveis globais para os widgets de alunos
aluno_id_selecionado = None
entry_nome_aluno = None
entry_email_aluno = None
selected_curso = None
curso_var = None
label_matricula_aluno = None
tree_alunos = None


def gerar_matricula():
    """Gera uma matrícula com formato: 1 letra maiúscula + 6 dígitos numéricos."""
    letra = random.choice(string.ascii_uppercase)
    numeros = ''.join(random.choices(string.digits, k=6))
    return letra + numeros


def abrir_tela_alunos(content_frame):
    """Exibe a interface de gerenciamento de alunos."""
    global aluno_id_selecionado, entry_nome_aluno, entry_email_aluno, selected_curso, curso_var, label_matricula_aluno, tree_alunos
    
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    tk.Label(content_frame, text="Gerenciamento de Alunos", font=("Arial", 18, "bold"), fg="white",
             bg="#20232a").pack(pady=10)

    # Frame para o formulário de cadastro/edição
    form_frame = tk.Frame(content_frame, bg="#20232a")
    form_frame.pack(pady=10)

    # Variáveis de controle
    aluno_id_selecionado = tk.StringVar()
    
    tk.Label(form_frame, text="Nome:", bg="#20232a", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome_aluno = tk.Entry(form_frame, width=30)
    entry_nome_aluno.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Email:", bg="#20232a", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_email_aluno = tk.Entry(form_frame, width=30)
    entry_email_aluno.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Curso:", bg="#20232a", fg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    curso_var = tk.StringVar()
    selected_curso = ttk.Combobox(form_frame, width=27, textvariable=curso_var, state="readonly")
    selected_curso["values"] = (
                                "",
                                "Direito",
                                "Administração",
                                "Medicina",
                                "Enfermagem",
                                "Psicologia",   
                                "Engenharia Civil",
                                "Pedagogia",
                                "Analise e Desenvolvimento de Sistemas",
                                "Arquitetura e Urbanismo",
                                "Nutrição")
    selected_curso.grid(row=3, column=1, padx=5, pady=5)
    selected_curso.current(0)

    # Exibe matrícula (apenas leitura) abaixo do campo Curso
    tk.Label(form_frame, text="Matrícula:", bg="#20232a", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    label_matricula_aluno = tk.Label(form_frame, text="(Gerada automaticamente)", bg="#20232a", fg="#61dafb")
    label_matricula_aluno.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Botões de Ação
    action_frame = tk.Frame(content_frame, bg="#20232a")
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="Adicionar Aluno", command=adicionar_ou_atualizar_aluno, bg="#98c379", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Limpar Campos", command=limpar_campos_aluno, bg="#e5c07b", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Excluir Selecionado", command=deletar_aluno_selecionado, bg="#e06c75", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Associar a Sala", command=lambda: __import__('telas_associacao').abrir_tela_associacao_aluno_sala(content_frame), 
              bg="#61dafb", fg="black",
              font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

    # Treeview para exibir a lista de alunos
    tree_alunos = ttk.Treeview(content_frame, columns=("ID", "Nome", "Matrícula", "Email", "Curso"), show="headings")
    tree_alunos.heading("ID", text="ID")
    tree_alunos.heading("Nome", text="Nome")
    tree_alunos.heading("Matrícula", text="Matrícula")
    tree_alunos.heading("Email", text="Email")
    tree_alunos.heading("Curso", text="Curso")
    
    tree_alunos.column("ID", width=50, anchor="center")
    tree_alunos.column("Nome", width=150)
    tree_alunos.column("Matrícula", width=100, anchor="center")
    tree_alunos.column("Email", width=150)
    tree_alunos.column("Curso", width=150)
    
    tree_alunos.pack(fill=tk.BOTH, expand=True)
    tree_alunos.bind("<<TreeviewSelect>>", carregar_aluno_para_edicao)

    carregar_alunos_na_treeview()


def carregar_alunos_na_treeview():
    """Carrega os dados dos alunos na Treeview."""
    for item in tree_alunos.get_children():
        tree_alunos.delete(item)
    
    alunos = banco.buscar_alunos()
    for aluno in alunos:
        tree_alunos.insert("", tk.END, values=aluno)


def limpar_campos_aluno():
    """Limpa os campos do formulário de aluno."""
    aluno_id_selecionado.set("")
    entry_nome_aluno.delete(0, tk.END)
    label_matricula_aluno.config(text="(Gerada automaticamente)")
    entry_email_aluno.delete(0, tk.END)
    curso_var.set("")


def carregar_aluno_para_edicao(event):
    """Carrega os dados do aluno selecionado para edição."""
    selected_item = tree_alunos.focus()
    if selected_item:
        values = tree_alunos.item(selected_item, 'values')
        aluno_id_selecionado.set(values[0])
        
        limpar_campos_aluno()
        entry_nome_aluno.insert(0, values[1])
        label_matricula_aluno.config(text=values[2])
        entry_email_aluno.insert(0, values[3])
        curso_var.set(values[4])


def adicionar_ou_atualizar_aluno():
    """Adiciona um novo aluno ou atualiza um existente."""
    nome = entry_nome_aluno.get()
    email = entry_email_aluno.get()
    curso = curso_var.get()

    if not nome or not email or not curso:
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios.")
        return

    aluno_id = aluno_id_selecionado.get()
    if aluno_id:
        # Atualizar - para atualizar usamos a matrícula existente
        matricula = label_matricula_aluno.cget("text")
        if banco.atualizar_aluno(aluno_id, nome, matricula, email, curso):
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")
    else:
        # Adicionar - gerar nova matrícula
        matricula = gerar_matricula()
        if banco.adicionar_aluno(nome, matricula, email, curso):
            messagebox.showinfo("Sucesso", f"Aluno adicionado com sucesso!\nMatrícula: {matricula}")
            label_matricula_aluno.config(text=matricula)
        else:
            messagebox.showerror("Erro", "Email já cadastrado ou matrícula duplicada.")

    limpar_campos_aluno()
    carregar_alunos_na_treeview()


def deletar_aluno_selecionado():
    """Deleta o aluno selecionado."""
    selected_item = tree_alunos.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione um aluno para excluir.")
        return

    aluno_id = tree_alunos.item(selected_item, 'values')[0]
    
    if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o aluno ID {aluno_id}?"):
        if banco.deletar_aluno(aluno_id):
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
            limpar_campos_aluno()
            carregar_alunos_na_treeview()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir o aluno.")
