import sqlite3

def criar_banco():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            idade INTEGER,
            trabalha TEXT,
            horas_dia_num REAL,
            impacto_relacoes TEXT,
            plataforma_mais_usada TEXT,
            horario_pico TEXT,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def cadastrar_resposta(id_usuario, idade, trabalha, horas_dia_num, impacto_relacoes, plataforma_mais_usada, horario_pico):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO respostas (id_usuario, idade, trabalha, horas_dia_num, impacto_relacoes, plataforma_mais_usada, horario_pico)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_usuario, idade, trabalha, horas_dia_num, impacto_relacoes, plataforma_mais_usada, horario_pico))
    conn.commit()
    conn.close()

def obter_resposta_usuario(id_usuario):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM respostas WHERE id_usuario = ?', (id_usuario,))
    resposta = cursor.fetchone()
    conn.close()
    return resposta

def atualizar_resposta(id_usuario, idade, trabalha, horas_dia_num, impacto_relacoes, plataforma_mais_usada, horario_pico):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE respostas 
        SET idade = ?, trabalha = ?, horas_dia_num = ?, impacto_relacoes = ?, plataforma_mais_usada = ?, horario_pico = ?
        WHERE id_usuario = ?
    ''', (idade, trabalha, horas_dia_num, impacto_relacoes, plataforma_mais_usada, horario_pico, id_usuario))
    conn.commit()
    conn.close()

def excluir_resposta(id_usuario):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM respostas WHERE id_usuario = ?', (id_usuario,))
    conn.commit()
    conn.close()

def verificar_usuario(email, senha):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user

def cadastrar_usuario(nome, email, senha):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_email_existe(email):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe
