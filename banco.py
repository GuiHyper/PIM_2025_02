import sqlite3

DB_NAME = "sistema_academico.db"

def conectar():
    """Conecta ao banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)

def inicializador_do_banco():
    """Cria as tabelas Aluno e Sala se não existirem."""
    with conectar() as conexao:
        cursor = conexao.cursor()

        # Tabela aluno
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS aluno ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "nome TEXT NOT NULL,"
            "matricula TEXT NOT NULL UNIQUE,"
            "email TEXT NOT NULL UNIQUE,"
            "curso TEXT NOT NULL)"
        )

        # Tabela sala
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sala ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "nome TEXT NOT NULL UNIQUE,"
            "capacidade INTEGER NOT NULL,"
            "curso TEXT NOT NULL DEFAULT '' )"
        )

        # Tabela aluno_sala (Associação N:M entre Aluno e Sala)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS aluno_sala ("
            "aluno_id INTEGER NOT NULL,"
            "sala_id INTEGER NOT NULL,"
            "PRIMARY KEY (aluno_id, sala_id),"
            "FOREIGN KEY (aluno_id) REFERENCES aluno(id) ON DELETE CASCADE,"
            "FOREIGN KEY (sala_id) REFERENCES sala(id) ON DELETE CASCADE)"
        )

        # Tabela nota
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS nota ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "aluno_id INTEGER NOT NULL,"
            "sala_id INTEGER NOT NULL,"
            "np1 REAL DEFAULT 0.0,"
            "np2 REAL DEFAULT 0.0,"
            "trabalho REAL DEFAULT 0.0,"
            "media REAL DEFAULT 0.0,"
            "data_atribuicao DATETIME DEFAULT CURRENT_TIMESTAMP,"
            "UNIQUE (aluno_id, sala_id),"
            "FOREIGN KEY (aluno_id) REFERENCES aluno(id) ON DELETE CASCADE,"
            "FOREIGN KEY (sala_id) REFERENCES sala(id) ON DELETE CASCADE)"
        )
        
    # Commit das criações iniciais
        conexao.commit()

        # Garantir compatibilidade com bancos existentes: adicionar coluna 'curso' se faltar
        cursor.execute("PRAGMA table_info(sala)")
        cols = [row[1] for row in cursor.fetchall()]
        if 'curso' not in cols:
            cursor.execute("ALTER TABLE sala ADD COLUMN curso TEXT NOT NULL DEFAULT ''")
            conexao.commit()

    # --- Funções CRUD para Aluno ---

def adicionar_aluno(nome, matricula, email, curso):
    """Adiciona um novo aluno ao banco de dados."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO aluno (nome, matricula, email, curso)
                VALUES (?, ?, ?, ?)
            ''', (nome, matricula, email, curso))
            conexao.commit()
            return True
    except sqlite3.IntegrityError:
        # Matrícula ou email já existem
        return False

def buscar_alunos():
    """Retorna todos os alunos cadastrados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, matricula, email, curso FROM aluno ORDER BY nome")
        return cursor.fetchall()

def buscar_aluno_por_id(aluno_id):
    """Retorna um aluno pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, matricula, email, curso FROM aluno WHERE id = ?", (aluno_id,))
        return cursor.fetchone()

def atualizar_aluno(aluno_id, nome, matricula, email, curso):
    """Atualiza os dados de um aluno."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE aluno SET nome = ?, matricula = ?, email = ?, curso = ?
                WHERE id = ?
            ''', (nome, matricula, email, curso, aluno_id))
            conexao.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        # Matrícula ou email já existem
        return False

def deletar_aluno(aluno_id):
    """Deleta um aluno pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM aluno WHERE id = ?", (aluno_id,))
        conexao.commit()
        return cursor.rowcount > 0

# --- Funções CRUD para Sala ---

def adicionar_sala(nome, capacidade, curso=''):
    """Adiciona uma nova sala ao banco de dados."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO sala (nome, capacidade, curso)
                VALUES (?, ?, ?)
            ''', (nome, capacidade, curso))
            conexao.commit()
            return True
    except sqlite3.IntegrityError:
        # Nome da sala já existe
        return False

def buscar_salas():
    """Retorna todas as salas cadastradas."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, capacidade, curso FROM sala ORDER BY nome")
        return cursor.fetchall()

def buscar_sala_por_id(sala_id):
    """Retorna uma sala pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, capacidade, curso FROM sala WHERE id = ?", (sala_id,))
        return cursor.fetchone()

def atualizar_sala(sala_id, nome, capacidade, curso=''):
    """Atualiza os dados de uma sala."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE sala SET nome = ?, capacidade = ?, curso = ?
                WHERE id = ?
            ''', (nome, capacidade, curso, sala_id))
            conexao.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        # Nome da sala já existe
        return False

def deletar_sala(sala_id):
    """Deleta uma sala pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM sala WHERE id = ?", (sala_id,))
        conexao.commit()
        return cursor.rowcount > 0

# --- Funções para Associação Aluno-Sala ---

def associar_aluno_sala(aluno_id, sala_id):
    """Associa um aluno a uma sala."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO aluno_sala (aluno_id, sala_id)
                VALUES (?, ?)
            ''', (aluno_id, sala_id))
            conexao.commit()
            return True
    except sqlite3.IntegrityError:
        # Aluno já associado a esta sala
        return False

def desassociar_aluno_sala(aluno_id, sala_id):
    """Desassocia um aluno de uma sala."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            DELETE FROM aluno_sala WHERE aluno_id = ? AND sala_id = ?
        ''', (aluno_id, sala_id))
        conexao.commit()
        return cursor.rowcount > 0

def buscar_alunos_por_sala(sala_id):
    """Retorna os alunos associados a uma sala."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT a.id, a.nome, a.matricula, a.email, a.curso
            FROM aluno a
            JOIN aluno_sala als ON a.id = als.aluno_id
            WHERE als.sala_id = ?
            ORDER BY a.nome
        ''', (sala_id,))
        return cursor.fetchall()

def buscar_salas_por_aluno(aluno_id):
    """Retorna as salas associadas a um aluno."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT s.id, s.nome, s.capacidade, s.curso
            FROM sala s
            JOIN aluno_sala als ON s.id = als.sala_id
            WHERE als.aluno_id = ?
            ORDER BY s.nome
        ''', (aluno_id,))
        return cursor.fetchall()

def buscar_cursos():
    """Retorna a lista de cursos distintos cadastrados (provenientes da tabela aluno)."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT curso FROM aluno WHERE curso IS NOT NULL AND curso != '' ORDER BY curso")
        return [row[0] for row in cursor.fetchall()]

# --- Funções CRUD para Notas ---

def calcular_media(np1, np2, trabalho):
    """Calcula a média ponderada: NP1(peso 4) + NP2(peso 4) + Trabalho(peso 2)."""
    # A soma dos pesos é 4 + 4 + 2 = 10
    if np1 is None or np2 is None or trabalho is None:
        return 0.0
    
    media = (np1 * 4 + np2 * 4 + trabalho * 2) / 10
    return round(media, 2)

def atribuir_notas(aluno_id, sala_id, np1, np2, trabalho):
    """Atribui ou atualiza as notas de um aluno em uma sala e calcula a média."""
    media = calcular_media(np1, np2, trabalho)
    
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # Tenta atualizar
            cursor.execute('''
                UPDATE nota SET np1 = ?, np2 = ?, trabalho = ?, media = ?, data_atribuicao = CURRENT_TIMESTAMP
                WHERE aluno_id = ? AND sala_id = ?
            ''', (np1, np2, trabalho, media, aluno_id, sala_id))
            
            if cursor.rowcount == 0:
                # Se não atualizou, insere
                cursor.execute('''
                    INSERT INTO nota (aluno_id, sala_id, np1, np2, trabalho, media)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (aluno_id, sala_id, np1, np2, trabalho, media))
            
            conexao.commit()
            return True
    except Exception as e:
        print(f"Erro ao atribuir notas: {e}")
        return False

def buscar_notas_aluno_sala(aluno_id, sala_id):
    """Busca as notas (NP1, NP2, Trabalho, Média) de um aluno em uma sala."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT np1, np2, trabalho, media FROM nota WHERE aluno_id = ? AND sala_id = ?
        ''', (aluno_id, sala_id))
        resultado = cursor.fetchone()
        # Retorna (np1, np2, trabalho, media) ou (0.0, 0.0, 0.0, 0.0) se não houver registro
        return resultado if resultado else (0.0, 0.0, 0.0, 0.0)

def buscar_notas_por_sala(sala_id):
    """Retorna as notas (NP1, NP2, Trabalho, Média) de todos os alunos em uma sala."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT a.nome, n.np1, n.np2, n.trabalho, n.media, n.data_atribuicao
            FROM nota n
            JOIN aluno a ON n.aluno_id = a.id
            WHERE n.sala_id = ?
            ORDER BY a.nome
        ''', (sala_id,))
        return cursor.fetchall()

if __name__ == "__main__":
    inicializador_do_banco()
    print(f"Banco de dados '{DB_NAME}' inicializado com as tabelas 'aluno', 'sala', 'aluno_sala' e 'nota'.")
