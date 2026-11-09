import sqlite3

from models import RegistroBase


# ==========================================
# 1. CAMADA DE BANCO DE DADOS (SQLite)
# ==========================================

# Cria o banco de dados se ele não existe e conecta ao banco de dados
def conectar_banco():
    # Cria o arquivo banco_a3.db na mesma pasta do projeto
    conn = sqlite3.connect("banco_a3.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn


# Cria a tabela automaticamente ao iniciar a API
def criar_tabelas():
    conn = conectar_banco()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            ativo BOOLEAN DEFAULT TRUE
        )
    ''')
    conn.commit()
    conn.close()


## Rota post
# Insere um novo registro no banco de dados
def inserir_novo_registro(registro: RegistroBase):
    conn = conectar_banco()
    cursor = conn.cursor()
    print(registro)
    cursor.execute(
        "INSERT INTO registros (titulo, descricao, ativo) VALUES (?, ?, ?)",
        (registro.titulo, registro.descricao, registro.ativo)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id


## Rotas get
# Retorna todos os registros do banco de dados
def consultar_registros():
    conn = conectar_banco()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()
    return registros

# Retorna um registro do banco de dados a partir do seu id
def consultar_registro_por_id(registro_id: int):
    conn = conectar_banco()
    registro = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
    conn.close()
    return registro


## Rota put
# Atualiza um registro existente no banco de dados
def atualizar_registro_existente(registro_id: int, registro: RegistroBase):
    conn = conectar_banco()
    conn.execute(
        "UPDATE registros SET titulo = ?, descricao = ?, ativo = ? WHERE id = ?",
        (registro.titulo, registro.descricao, registro.ativo, registro_id)
    )
    conn.commit()
    conn.close()


## Rota delete
# Remove um registro do banco de dados
def remover_registro(registro_id: int):
    conn = conectar_banco()
    conn.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
