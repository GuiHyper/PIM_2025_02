## 📋 Estrutura do Projeto - Sistema Acadêmico

O projeto foi refatorado para separar as páginas/telas em arquivos diferentes, melhorando a organização e manutenibilidade do código.

### 📁 Estrutura de Arquivos

```
PIM/
├── pim.py                  # Arquivo principal - Interface e navegação
├── telas_alunos.py         # Tela de gerenciamento de alunos
├── telas_salas.py          # Tela de gerenciamento de salas
├── telas_associacao.py     # Tela de associação aluno-sala
├── telas_notas.py          # Tela de atribuição de notas
├── banco.py                # Módulo de banco de dados
├── chatbot.py              # Módulo de chatbot (Flask)
└── sistema_academico.db    # Banco de dados SQLite
```

---

### 📄 Descrição dos Arquivos

#### **pim.py** (Arquivo Principal)
- Inicializa a aplicação Tkinter
- Gerencia a janela principal e o frame de conteúdo
- Coordena a navegação entre telas via botões
- Gerencia o servidor Flask do chatbot
- **Funções principais:**
  - `iniciar_tela_principal()` - Cria a interface principal
  - `start_flask_server()` - Inicia o servidor Flask em thread
  - `abrir_chatbot()` - Abre o chatbot no navegador

#### **telas_alunos.py**
- Interface de gerenciamento de alunos (Cadastro, edição, exclusão)
- Auto-geração de matrícula (1 letra + 6 dígitos)
- Visualização de lista de alunos em Treeview
- **Funções principais:**
  - `abrir_tela_alunos()` - Abre a tela de alunos
  - `gerar_matricula()` - Gera ID de matrícula automático
  - `adicionar_ou_atualizar_aluno()` - Salva/atualiza aluno
  - `carregar_aluno_para_edicao()` - Carrega dados para edição
  - `deletar_aluno_selecionado()` - Remove aluno

#### **telas_salas.py**
- Interface de gerenciamento de salas (Cadastro, edição, exclusão)
- Visualização de alunos matriculados com status de aprovação
- **Status de aprovação:** 
  - 🟢 Verde (APROVADO) = Média ≥ 7
  - 🔴 Vermelho (REPROVADO) = Média < 7
- **Funções principais:**
  - `abrir_tela_salas()` - Abre a tela de salas
  - `on_sala_selecionada()` - Carrega alunos da sala selecionada
  - `adicionar_ou_atualizar_sala()` - Salva/atualiza sala
  - `deletar_sala_selecionada()` - Remove sala

#### **telas_associacao.py**
- Interface para associar/desassociar alunos a salas
- Comboboxes para seleção de aluno e sala
- **Funções principais:**
  - `abrir_tela_associacao_aluno_sala()` - Abre a tela de associação
  - Funções auxiliares de seleção e associação

#### **telas_notas.py**
- Interface para atribuição de notas (NP1, NP2, Trabalho)
- Cálculo automático de média ponderada
- Visualização de status de aprovação
- **Fórmula da média:** (NP1×4 + NP2×4 + Trabalho×2) / 10
- **Funções principais:**
  - `abrir_tela_atribuir_notas()` - Abre a tela de notas
  - `carregar_alunos_e_notas()` - Carrega alunos da sala selecionada
  - `atribuir_notas_selecionadas()` - Salva as notas

#### **banco.py**
- Módulo de acesso ao banco de dados SQLite
- Operações CRUD para alunos, salas, notas e associações
- Não foi modificado nesta refatoração

#### **chatbot.py**
- Aplicação Flask do chatbot acadêmico
- Não foi modificado nesta refatoração

---

### 🎨 Tema de Cores
- **Fundo primário:** #282c34 (Cinza escuro)
- **Fundo secundário:** #20232a (Cinza mais escuro)
- **Texto principal:** Branco
- **Destaque:** #61dafb (Ciano)
- **Botão de ação:** #98c379 (Verde)
- **Botão de alerta:** #e5c07b (Amarelo)
- **Botão de exclusão:** #e06c75 (Vermelho)
- **Status APROVADO:** #00aa00 (Verde)
- **Status REPROVADO:** #ff6b6b (Vermelho)

---

### 🚀 Como Usar

1. **Executar o sistema:**
   ```bash
   python pim.py
   ```

2. **Gerenciar Alunos:**
   - Clique em "Gerenciar Alunos"
   - Preencha nome, email e selecione curso
   - Clique "Adicionar Aluno" (matrícula gerada automaticamente)

3. **Gerenciar Salas:**
   - Clique em "Gerenciar Salas"
   - Crie salas com nome, capacidade e descrição
   - Veja alunos matriculados e seus status

4. **Associar Alunos a Salas:**
   - Na tela de Alunos, clique "Associar a Sala"
   - Selecione aluno e sala
   - Clique "Associar"

5. **Atribuir Notas:**
   - Na tela de Salas, clique "Atribuir Notas"
   - Selecione uma sala
   - Selecione um aluno
   - Preencha NP1, NP2 e Trabalho (0-10)
   - Clique "Atribuir Notas"

6. **Usar Chatbot:**
   - Clique em "Chatbot Acadêmico"
   - O navegador abrirá em http://127.0.0.1:5000

---

### ✨ Benefícios da Refatoração

1. **Melhor Organização** - Cada tela em seu próprio arquivo
2. **Facilita Manutenção** - Mais fácil encontrar e corrigir código
3. **Escalabilidade** - Adicionar novas telas sem modificar pim.py
4. **Reusabilidade** - Funções podem ser reutilizadas em outros projetos
5. **Clareza** - Código mais limpo e documentado

---

### 📝 Notas

- Todas as variáveis globais são mantidas em seus respectivos módulos
- O `content_frame` é passado como parâmetro para as funções `abrir_tela_*`
- As telas são carregadas dinamicamente quando o usuário clica no botão
- O banco de dados é criado automaticamente ao iniciar a aplicação

---

### 🔧 Requisitos

- Python 3.8+
- tkinter (incluído com Python)
- sqlite3 (incluído com Python)
- Flask (para o chatbot)
- OpenAI API key (para o chatbot)

