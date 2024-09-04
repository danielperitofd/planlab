import os
import mysql.connector
from mysql.connector import errorcode

DATABASE_NAME = 'plano_aula_db'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='danielguspe',
            password='root',
            database=DATABASE_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        exit(1)

def create_database_if_not_exists(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    except mysql.connector.Error as err:
        print(f"Erro ao criar banco de dados: {err}")
        exit(1)
    cursor.close()

# Criação das tabelas
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aula (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_aula DATE NOT NULL,
            turma VARCHAR(255) NOT NULL,
            semestre VARCHAR(255) NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            conteudo_programatico TEXT,
            metodologia TEXT,
            recursos_necessarios TEXT,
            avaliacao_observacoes TEXT,
            observacoes TEXT,
            eventos_extraordinarios ENUM('Sim', 'Não'),
            usuario_id INT,
            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
        )
    ''')
    conn.commit()
    inserir_dados_iniciais(conn)
    cursor.close()

def inserir_dados_iniciais(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios = cursor.fetchall()
    if not usuarios:
        cursor.execute('''
            INSERT INTO usuario (nome, email, senha)
            VALUES ("usuario", "usuario@usuario.com.br", "1234")
        ''')
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    conn = get_db_connection()
    create_tables(conn)
    conn.close()
    print("Banco de dados e tabelas configurados com sucesso.")
