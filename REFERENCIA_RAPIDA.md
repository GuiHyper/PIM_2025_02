# ⚡ Referência Rápida - Sistema Acadêmico v2.0

## 🚀 Começar Rápido

```bash
# Executar o projeto
python pim.py
```

---

## 📁 Estrutura do Projeto

```
PIM/
├── 🎨 TELAS (Interface Tkinter)
│   ├── pim.py ⭐ (Principal - Navbar)
│   ├── telas_alunos.py (Gerenciar alunos)
│   ├── telas_salas.py (Gerenciar salas)
│   ├── telas_associacao.py (Associar alunos-salas)
│   └── telas_notas.py (Atribuir notas)
│
├── 💾 DADOS
│   ├── banco.py (Acesso ao BD)
│   └── sistema_academico.db (SQLite)
│
├── 🤖 EXTRAS
│   ├── chatbot.py (Flask IA)
│   └── .env (Variáveis de ambiente)
│
└── 📚 DOCUMENTAÇÃO
    ├── README.md ← COMECE AQUI
    ├── ARQUITETURA.txt
    ├── GUIA_REFATORACAO.md
    ├── RESUMO_REFATORACAO.txt
    ├── INDICE_PROJETO.txt
    ├── MAPA_VISUAL.txt
    └── REFERENCIA_RAPIDA.md (Este arquivo!)
```

---

## 🎯 Onde Encontrar Cada Funcionalidade

| O que eu quero fazer | Arquivo a editar | Função principal |
|---|---|---|
| Adicionar campo ao formulário de alunos | `telas_alunos.py` | `abrir_tela_alunos()` |
| Editar aluno | `telas_alunos.py` | `carregar_aluno_para_edicao()` |
| Adicionar campo ao formulário de salas | `telas_salas.py` | `abrir_tela_salas()` |
| Ver alunos de uma sala com status | `telas_salas.py` | `on_sala_selecionada()` |
| Associar aluno a sala | `telas_associacao.py` | `abrir_tela_associacao_aluno_sala()` |
| Mudar fórmula de média | `banco.py` | `calcular_media()` |
| Atribuir notas a alunos | `telas_notas.py` | `atribuir_notas_selecionadas()` |
| Adicionar botão na navbar | `pim.py` | `iniciar_tela_principal()` |
| Mudar cores do tema | `pim.py` + telas | Buscar por `#282c34` etc |

---

## 🔧 Tarefas Comuns

### Adicionar Nova Tela

1. **Criar arquivo:**
   ```python
   # telas_exemplo.py
   import tkinter as tk
   import banco
   
   def abrir_tela_exemplo(content_frame):
       for widget in content_frame.winfo_children():
           widget.destroy()
       
       tk.Label(content_frame, text="Minha Nova Tela", 
                font=("Arial", 18), fg="white", bg="#20232a").pack()
   ```

2. **Editar `pim.py`:**
   ```python
   # Adicionar no topo:
   import telas_exemplo
   
   # Adicionar botão na navbar:
   tk.Button(frame_botoes, text="Exemplo",
             command=lambda: telas_exemplo.abrir_tela_exemplo(content_frame))
   ```

### Adicionar Campo ao Formulário

**Exemplo: Adicionar campo "Telefone" em alunos**

```python
# Em telas_alunos.py, função abrir_tela_alunos():

# Adicionar antes do Combobox de Curso:
tk.Label(form_frame, text="Telefone:", bg="#20232a", fg="white")\
    .grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_telefone_aluno = tk.Entry(form_frame, width=30)
entry_telefone_aluno.grid(row=2, column=1, padx=5, pady=5)

# Em adicionar_ou_atualizar_aluno():
telefone = entry_telefone_aluno.get()
```

### Mudar Cores

Busque pelos hexadecimais e substitua:
- `#282c34` - Fundo primário
- `#20232a` - Fundo secundário
- `#61dafb` - Destaque (ciano)
- `#98c379` - Botão sucesso (verde)
- `#e5c07b` - Botão aviso (amarelo)
- `#e06c75` - Botão perigo (vermelho)

---

## 📊 Variáveis Globais por Arquivo

### `telas_alunos.py`
- `aluno_id_selecionado` - StringVar com ID do aluno
- `entry_nome_aluno` - Entry para nome
- `entry_email_aluno` - Entry para email
- `curso_var` - StringVar para curso
- `selected_curso` - Combobox de cursos
- `label_matricula_aluno` - Label mostrando matrícula
- `tree_alunos` - Treeview com lista de alunos

### `telas_salas.py`
- `sala_id_selecionada` - StringVar com ID da sala
- `entry_nome_sala` - Entry para nome
- `entry_capacidade_sala` - Entry para capacidade
- `entry_descricao_sala` - Entry para descrição
- `tree_salas` - Treeview com lista de salas
- `tree_alunos_sala` - Treeview com alunos da sala

### `telas_associacao.py`
- `aluno_selecionado_var` - StringVar para aluno
- `sala_selecionada_var` - StringVar para sala

### `telas_notas.py`
- `sala_nota_selecionada_var` - StringVar para sala
- `entry_np1` - Entry para NP1
- `entry_np2` - Entry para NP2
- `entry_trabalho` - Entry para Trabalho
- `tree_notas` - Treeview com lista de notas

---

## 🔗 Funções de Banco de Dados Mais Usadas

```python
# ALUNOS
banco.adicionar_aluno(nome, matricula, email, curso)
banco.buscar_alunos()
banco.atualizar_aluno(id, nome, matricula, email, curso)
banco.deletar_aluno(id)

# SALAS
banco.adicionar_sala(nome, capacidade, descricao)
banco.buscar_salas()
banco.atualizar_sala(id, nome, capacidade, descricao)
banco.deletar_sala(id)

# ASSOCIAÇÕES
banco.associar_aluno_sala(aluno_id, sala_id)
banco.desassociar_aluno_sala(aluno_id, sala_id)
banco.buscar_alunos_por_sala(sala_id)

# NOTAS
banco.atribuir_notas(aluno_id, sala_id, np1, np2, trabalho)
banco.buscar_notas_aluno_sala(aluno_id, sala_id)
banco.calcular_media(np1, np2, trabalho)
```

---

## 🎨 Código Padrão para Novas Telas

```python
"""
Módulo de [Nome da Tela]
Descrição do que faz
"""

import tkinter as tk
from tkinter import messagebox, ttk
import banco

# Variáveis globais
widget1 = None
widget2 = None
tree_lista = None


def abrir_tela_exemplo(content_frame):
    """Abre a tela de exemplo."""
    global widget1, widget2, tree_lista
    
    # Limpar content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(content_frame, text="Título da Tela", 
             font=("Arial", 18, "bold"), fg="white",
             bg="#20232a").pack(pady=10)
    
    # Frame do formulário
    form_frame = tk.Frame(content_frame, bg="#20232a")
    form_frame.pack(pady=10)
    
    # Widgets do formulário
    tk.Label(form_frame, text="Campo 1:", bg="#20232a", 
             fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    widget1 = tk.Entry(form_frame, width=30)
    widget1.grid(row=0, column=1, padx=5, pady=5)
    
    # Botões
    action_frame = tk.Frame(content_frame, bg="#20232a")
    action_frame.pack(pady=10)
    
    tk.Button(action_frame, text="Salvar", command=salvar_dados,
              bg="#98c379", fg="black", font=("Arial", 10, "bold"))\
        .pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Limpar", command=limpar_campos,
              bg="#e5c07b", fg="black", font=("Arial", 10, "bold"))\
        .pack(side=tk.LEFT, padx=5)
    
    # Treeview
    tree_lista = ttk.Treeview(content_frame, columns=("Col1", "Col2"),
                              show="headings")
    tree_lista.heading("Col1", text="Coluna 1")
    tree_lista.heading("Col2", text="Coluna 2")
    tree_lista.pack(fill=tk.BOTH, expand=True)
    
    carregar_dados()


def carregar_dados():
    """Carrega dados da Treeview."""
    # Limpar
    for item in tree_lista.get_children():
        tree_lista.delete(item)
    
    # Inserir dados
    dados = banco.buscar_algo()  # Use sua função
    for dado in dados:
        tree_lista.insert("", tk.END, values=dado)


def salvar_dados():
    """Salva os dados."""
    valor = widget1.get()
    if not valor:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return
    
    if banco.adicionar_algo(valor):  # Use sua função
        messagebox.showinfo("Sucesso", "Dados salvos!")
        limpar_campos()
        carregar_dados()
    else:
        messagebox.showerror("Erro", "Não foi possível salvar.")


def limpar_campos():
    """Limpa os campos do formulário."""
    widget1.delete(0, tk.END)
```

---

## 🐛 Troubleshooting

| Problema | Solução |
|---|---|
| `ModuleNotFoundError: No module named 'telas_alunos'` | Certifique-se que os arquivos estão no mesmo diretório |
| `NameError: name 'content_frame' is not defined` | Verifique se `content_frame` está sendo passado como parâmetro |
| Banco de dados não criado | Execute `python pim.py` uma vez, o banco será criado automaticamente |
| Chatbot não abre | Instale Flask: `pip install flask` e adicione chave OpenAI em `.env` |
| Treeview vazio | Verifique se há dados no banco com `banco.buscar_alunos()` |

---

## 📈 Estatísticas do Projeto

| Métrica | Valor |
|---|---|
| Arquivos Python | 7 |
| Linhas de código | ~710 |
| Tabelas de BD | 4 |
| Telas implementadas | 5 |
| Status | ✅ Funcional |

---

## 🎓 Recursos Educacionais

- **Tkinter:** Widgets, layout, event binding
- **SQLite3:** CRUD, transações, índices
- **Flask:** Rotas, templates, threading
- **Padrão MVC:** Model (banco) → View (telas) → Controller (pim)

---

## 💡 Boas Práticas Implementadas

✅ Código modular e reutilizável  
✅ Separação de responsabilidades  
✅ Tratamento de erros  
✅ Validação de entrada  
✅ Interface consistente  
✅ Documentação clara  
✅ Nomes descritivos de variáveis/funções  
✅ Comentários explicativos  

---

## 🚀 Próximas Melhorias Sugeridas

1. Criar `telas_relatorios.py`
2. Criar `telas_configuracoes.py`
3. Adicionar `util_validacao.py`
4. Adicionar `util_estilos.py`
5. Implementar autenticação
6. Migrar para web (Flask + HTML)

---

## 📞 Precisa de Ajuda?

1. Leia o **README.md** para entender o projeto
2. Consulte **ARQUITETURA.txt** para entender a estrutura
3. Veja **INDICE_PROJETO.txt** para descrição detalhada de cada arquivo
4. Veja este documento para referência rápida

---

**Versão:** 2.0 | **Status:** ✅ Modular e Funcional | **Data:** Novembro 2025
