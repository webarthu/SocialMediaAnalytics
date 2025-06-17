import sqlite3

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

