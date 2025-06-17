import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from db import (
    criar_banco,
    verificar_usuario,
    cadastrar_resposta,
    obter_resposta_usuario,
    atualizar_resposta,
    excluir_resposta,
    cadastrar_usuario,
    verificar_email_existe
)
from graphics import grafico_dispersao, grafico_barras_lateral, grafico_pizza, grafico_barras_horario, mostrar_grafico


class App:
    def __init__(self):
        criar_banco()
        self.root = tk.Tk()
        self.root.title("Meu Projeto")
        self.root.geometry("1900x900")
        self.root.configure(bg="#1e1e2f")  # exemplo de cor azul claro
        self.usuario_logado = None
        self.tela_inicial()

    def set_hover_effect(self, widget, hover_color, normal_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))
    
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_inicial(self):
        self.limpar_tela()

        print("Usuario logado:", self.usuario_logado)

        # Cria um frame centralizado na janela
        frame_central = tk.Frame(self.root, bg="#1e1e2f")
        frame_central.place(relx=0.5, rely=0.5, anchor='center')

        # Label centralizado dentro do frame
        tk.Label(frame_central, text="Bem-vindo!", bg="#1e1e2f", fg="#ffffff").pack(pady=10)

        # Botão Login centralizado dentro do frame
        btn_login = tk.Button(frame_central, text="Login", width=20, bg="#1e1e2f", fg="#ffffff", command=self.tela_login)
        btn_login.pack(pady=5)
        self.set_hover_effect(btn_login, "#2c2c3e", "#1e1e2f")

        # Botão Cadastro centralizado dentro do frame
        btn_cadastro = tk.Button(frame_central, text="Cadastro", width=20, bg="#1e1e2f", fg="#ffffff", command=self.tela_cadastro)
        btn_cadastro.pack(pady=5)
        self.set_hover_effect(btn_cadastro, "#2c2c3e", "#1e1e2f")



    def tela_login(self):
        self.limpar_tela()

        frame = tk.Frame(self.root, bg="#1e1e2f", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Login", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=(0, 20))

        # Email
        tk.Label(frame, text="Email", anchor='w', bg="#1e1e2f", fg="#ffffff").pack(fill='x')
        self.entry_email_login = tk.Entry(frame, bg="#151524", fg="#ffffff", insertbackground="#ffffff")
        self.entry_email_login.pack(fill='x', pady=(0, 10))

        # Senha
        tk.Label(frame, text="Senha", anchor='w', bg="#1e1e2f", fg="#ffffff").pack(fill='x')
        self.entry_senha_login = tk.Entry(frame, bg="#151524", fg="#ffffff", show="*", insertbackground="#ffffff")
        self.entry_senha_login.pack(fill='x', pady=(0, 20))


        def tentar_login():
            email = self.entry_email_login.get().strip()
            senha = self.entry_senha_login.get().strip()

            if not email or not senha:
                messagebox.showerror("Erro", "Email e senha não podem estar vazios.")
                return

            user = verificar_usuario(email, senha)
            if user:
                self.usuario_logado = user
                messagebox.showinfo("Sucesso", f"Bem-vindo, {user[1]}!")
                self.tela_principal()
            else:
                messagebox.showerror("Erro", "Email ou senha incorretos.")

        # Botões
        tk.Button(frame, text="Entrar", width=20, bg="#2c2c3e", fg="#ffffff", command=tentar_login).pack(pady=(0, 10))
        tk.Button(frame, text="Voltar", width=20, bg="#2c2c3e", fg="#ffffff", command=self.tela_inicial).pack()


    def tela_cadastro(self):
        self.limpar_tela()

        frame = tk.Frame(self.root, bg="#1e1e2f", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Cadastro", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=(0, 20))

        # Nome
        tk.Label(frame, text="Nome", anchor='w', bg="#1e1e2f", fg="#ffffff").pack(fill='x')
        self.entry_nome_cadastro = tk.Entry(frame, bg="#151524", fg="#ffffff", insertbackground="#ffffff")
        self.entry_nome_cadastro.pack(fill='x', pady=(0, 10))

        # Email
        tk.Label(frame, text="Email", anchor='w', bg="#1e1e2f", fg="#ffffff").pack(fill='x')
        self.entry_email_cadastro = tk.Entry(frame, bg="#151524", fg="#ffffff", insertbackground="#ffffff")
        self.entry_email_cadastro.pack(fill='x', pady=(0, 10))

        # Senha
        tk.Label(frame, text="Senha", anchor='w', bg="#1e1e2f", fg="#ffffff").pack(fill='x')
        self.entry_senha_cadastro = tk.Entry(frame, bg="#151524", fg="#ffffff", show="*", insertbackground="#ffffff")
        self.entry_senha_cadastro.pack(fill='x')



        def tentar_cadastrar():
            nome = self.entry_nome_cadastro.get().strip()
            email = self.entry_email_cadastro.get().strip()
            senha = self.entry_senha_cadastro.get().strip()

            if not nome or not email or not senha:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return
            if verificar_email_existe(email):
                messagebox.showerror("Erro", "Email já cadastrado.")
                return

            sucesso = cadastrar_usuario(nome, email, senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso! Faça login.")
                self.tela_login()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar usuário. Tente novamente.")

        tk.Button(self.root, text="Cadastrar", width=20, bg="#1e1e2f", fg="#ffffff", command=tentar_cadastrar).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, bg="#1e1e2f", fg="#ffffff", command=self.tela_inicial).pack()

    def tela_principal(self):
        self.limpar_tela()
        print("Usuario logado:", self.usuario_logado)

        # Frame centralizador
        frame = tk.Frame(self.root, bg="#1e1e2f", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Título
        tk.Label(frame, text="Social Media Analytics", font=("Helvetica", 18, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=(0, 15))

        # Descrição
        descricao = (
            "Uma ferramenta interativa que permite:\n"
            "• Registrar sua própria resposta\n"
            "• Comparar seu perfil com os dados do dataset\n"
            "• Visualizar gráficos de análise social"
        )
        tk.Label(frame, text=descricao, font=("Helvetica", 12), bg="#1e1e2f", fg="#ffffff", justify="left").pack(pady=(0, 25))

        # Botões estilizados
        style = {"bg": "#343452", "fg": "#ffffff", "width": 20, "font": ("Helvetica", 12, "bold"), "relief": "flat", "activebackground": "#2c2c3e", "activeforeground": "#ffffff"}

        btn_minhas_respostas = tk.Button(frame, text="Minhas Respostas", command=self.ver_minha_resposta, **style)
        btn_minhas_respostas.pack(pady=5)

        btn_graficos = tk.Button(frame, text="Gráficos", command=self.tela_graficos, **style)
        btn_graficos.pack(pady=5)

        btn_ver_dataset = tk.Button(frame, text="Ver Dataset", command=self.ver_dados_dataset_tabela, **style)
        btn_ver_dataset.pack(pady=5)

        btn_sair = tk.Button(frame, text="Sair", command=self.fazer_logout, **style)
        btn_sair.pack(pady=(15, 0))

    def ver_minha_resposta(self):
        self.limpar_tela()
        print("Usuario logado:", self.usuario_logado)
        print("Usuario logado:", self.usuario_logado[1])

        # Frame centralizador para deixar tudo alinhado no centro da janela
        frame = tk.Frame(self.root, bg="#1e1e2f", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(frame, text="Cadastrar Resposta", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        resposta = obter_resposta_usuario(self.usuario_logado[0])

        tk.Label(frame, text="Idade", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        idade = tk.Entry(frame, bg="#151524", fg="#ffffff")
        idade.pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Trabalha?", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        trabalha = tk.StringVar(value="Sim")
        tk.OptionMenu(frame, trabalha, "Sim", "Não").pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Horas Dia", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        horas_dia = tk.Entry(frame, bg="#151524", fg="#ffffff")
        horas_dia.pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Impacto", bg="#1e2e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        impacto = tk.StringVar(value="Positivo")
        tk.OptionMenu(frame, impacto, "Positivo", "Negativo").pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Rede Social Mais Usada", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        plataforma = tk.StringVar(value="YouTube")
        tk.OptionMenu(frame, plataforma, "YouTube", "Twitter", "Instagram", "Facebook", "TikTok").pack(fill='x', pady=(0, 10))

        tk.Label(frame, text="Horário de Pico", bg="#1e2e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
        horario = tk.StringVar(value="Manhã")
        tk.OptionMenu(frame, horario, "Manhã", "Tarde", "Noite").pack(fill='x')
        
        if resposta:
            idade_valor = idade.get()
            trabalha_valor = trabalha.get()
            horas_dia_valor = horas_dia.get()
            impacto_valor = impacto.get()
            plataforma_valor = plataforma.get()
            horario_valor = horario.get()

            def tela_atualizar():
                    self.limpar_tela()

                    # Frame centralizador para alinhar tudo no centro da janela
                    frame = tk.Frame(self.root, bg="#1e1e2f", padx=20, pady=20)
                    frame.place(relx=0.5, rely=0.5, anchor='center')

                    tk.Label(frame, text="Atualizar Resposta", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

                    resposta = obter_resposta_usuario(self.usuario_logado[0])

                    tk.Label(frame, text="Trabalha?", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
                    trabalha = tk.StringVar(value="Sim")
                    tk.OptionMenu(frame, trabalha, "Sim", "Não").pack(fill='x', pady=(0, 10))

                    tk.Label(frame, text="Horas Dia", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
                    horas_dia = tk.Entry(frame, bg="#151524", fg="#ffffff")
                    horas_dia.pack(fill='x', pady=(0, 10))

                    tk.Label(frame, text="Impacto", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
                    impacto = tk.StringVar(value="Positivo")
                    tk.OptionMenu(frame, impacto, "Positivo", "Negativo").pack(fill='x', pady=(0, 10))

                    tk.Label(frame, text="Rede Social Mais Usada", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
                    plataforma = tk.StringVar(value="YouTube")
                    tk.OptionMenu(frame, plataforma, "YouTube", "Twitter", "Instagram", "Facebook", "TikTok").pack(fill='x', pady=(0, 10))

                    tk.Label(frame, text="Horário de Pico", bg="#1e1e2f", fg="#ffffff").pack(anchor='w', pady=(0, 3))
                    horario = tk.StringVar(value="Manhã")
                    tk.OptionMenu(frame, horario, "Manhã", "Tarde", "Noite").pack(fill='x')

            
                    def atualizar():
                        try:
                            atualizar_resposta(
                                self.usuario_logado[0],
                                idade.get(),
                                trabalha.get(),
                                float(horas_dia.get()),
                                impacto.get(),
                                plataforma.get(),
                                horario.get()
                            )
                            messagebox.showinfo("Atualizar", "Resposta atualizada!")
                            self.ver_minha_resposta()  # Atualiza a tela automaticamente
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
                    
                    tk.Button(self.root, text="Atualizar Resposta", bg="#1e1e2f", fg="#ffffff", command=atualizar).pack()
                    tk.Button(self.root, text="Cancelar", bg="#1e1e2f", fg="#ffffff", width=20, command=self.ver_minha_resposta).pack()

            def excluir():
                try:
                    excluir_resposta(self.usuario_logado[0])
                    messagebox.showinfo("Excluir", "Resposta excluída!")
                    self.ver_minha_resposta()  # Atualiza a tela automaticamente
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir: {e}")
            
            self.limpar_tela()
            
            tk.Label(self.root, text="Minha Resposta", bg="#1e1e2f", fg="#ffffff").pack()

            resposta = obter_resposta_usuario(self.usuario_logado[0])
            resposta_tratada = resposta[2:8]
            colunas_tratadas = ["Idade", "Trabalha", "Horas Dia", "Impacto", "Plataforma", "Horário Pico"]

            df = pd.DataFrame([resposta_tratada], columns=colunas_tratadas)

            # Criar Treeview
            tree = ttk.Treeview(self.root, columns=colunas_tratadas, show='headings', height=1)

            # Configurar colunas
            for col in colunas_tratadas:
                tree.heading(col, text=col)
                tree.column(col, anchor='center')  # Centralizar texto

            # Inserir os dados na tabela
            tree.insert('', 'end', values=resposta_tratada)

            tree.pack(pady=10)


            tk.Button(self.root, text="Atualizar Resposta", bg="#1e1e2f", fg="#ffffff", command=tela_atualizar).pack()
            tk.Button(self.root, text="Excluir Resposta", bg="#1e1e2f", fg="#ffffff", command=excluir).pack()

        else:
            def cadastrar():
                try:
                    cadastrar_resposta(
                        self.usuario_logado[0],
                        idade.get(),
                        trabalha.get(),
                        float(horas_dia.get()),
                        impacto.get(),
                        plataforma.get(),
                        horario.get()
                    )
                    messagebox.showinfo("Cadastrar", "Resposta cadastrada!")
                    self.ver_minha_resposta()  # Atualiza a tela automaticamente
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

            tk.Button(self.root, text="Cadastrar", bg="#1e1e2f", fg="#ffffff", command=cadastrar).pack()

        tk.Button(self.root, text="Voltar", bg="#1e1e2f", fg="#ffffff", command=self.tela_principal).pack(pady=5)

    def tela_graficos(self):
        self.limpar_tela()
        
        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(expand=True)

        tk.Label(frame, text="Gráficos", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=(0, 20))

        df = pd.read_csv('dataset.csv') 
        resposta = obter_resposta_usuario(self.usuario_logado[0])
        print(resposta)

        tk.Button(frame, text="Dispersão", bg="#1e1e2f", fg="#ffffff", 
                  command=lambda: mostrar_grafico(grafico_dispersao(df, resposta))).pack(fill='x', pady=5)

        tk.Button(frame, text="Barras Laterais", bg="#1e1e2f", fg="#ffffff",
                  command=lambda: mostrar_grafico(grafico_barras_lateral(df))).pack(fill='x', pady=5)
        
        tk.Button(frame, text="Pizza", bg="#1e1e2f", fg="#ffffff", 
                  command=lambda: mostrar_grafico(grafico_pizza(df))).pack(fill='x', pady=5)
        
        tk.Button(frame, text="Barras Horário", bg="#1e1e2f", fg="#ffffff", 
                  command=lambda: mostrar_grafico(grafico_barras_horario(df))).pack(fill='x', pady=5)

        tk.Button(frame, text="Voltar", bg="#1e1e2f", fg="#ffffff", command=self.tela_principal).pack(fill='x', pady=(20, 0))


    def ver_dados_dataset(self): 
            self.limpar_tela()

            frame = tk.Frame(self.root, bg="#1e1e2f")
            frame.pack(expand=True)

            tk.Label(frame, text="Dados do Dataset", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=(0, 20))

            df = pd.read_csv('dataset.csv')

            texto = tk.Text(frame, height=20, width=80, bg="#1e1e2f", fg="#ffffff")
            texto.pack()
            texto.insert('end', df.to_string())

            tk.Button(frame, text="Voltar", bg="#1e1e2f", fg="#ffffff", command=self.tela_principal).pack(pady=20)

        

    def ver_dados_dataset_tabela(self):
        self.limpar_tela()
        df = pd.read_csv('dataset.csv')
        df.columns = df.columns.str.strip()


        nomes_colunas = ["idade", "trabalha", "horas", "impacto", "plataforma", "horario"]
        # Correspondência das colunas do CSV para pegar os dados
        colunas_csv = ["idade,trabalha,horas_dia_num,impacto_relacoes,plataforma_mais_usada,horario_pico"]

        container = tk.Frame(self.root, bg="#1e1e2f")
        container.pack(expand=True, padx=20, pady=20)

        tk.Label(container, text="Dados do Dataset", bg="#1e1e2f", fg="#ffffff", font=("Arial", 16, "bold")).pack(pady=(0,15))

        # Frame para os headers (labels)
        header_frame = tk.Frame(container, bg="#1e1e2f")
        header_frame.pack(fill="x")

        for nome in nomes_colunas:
            lbl = tk.Label(header_frame, text=nome, bg="#1e1e2f", fg="#ffffff", font=("Arial", 12, "bold"), width=15, anchor="center")
            lbl.pack(side="left", padx=2)

        # Frame para organizar a tabela e o scroll, centralizado
        tabela_frame = tk.Frame(self.root, bg="#1e1e2f")
        tabela_frame.pack(pady=20, padx=20, expand=True)

        # Scrollbars
        scroll_y = tk.Scrollbar(tabela_frame, orient="vertical")
        scroll_x = tk.Scrollbar(tabela_frame, orient="horizontal")

        # Treeview com altura para 15 linhas visíveis
        tabela = ttk.Treeview(
            tabela_frame,
            show="headings",
            height=15,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        tabela['columns'] = list(df.columns)

        # Configurar colunas: texto centralizado e largura de 150 (ajuste se quiser)
        for col in df.columns:
            tabela.heading(col, text=col)
            tabela.column(col, anchor="center", width=150)

        # Inserir dados do dataset na tabela
        for i in df.index:
            tabela.insert("", "end", values=list(df.loc[i]))

        # Configurar scrollbars
        scroll_y.config(command=tabela.yview)
        scroll_x.config(command=tabela.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        tabela.pack(expand=True, fill="both")

        scroll_y.config(command=tabela.yview)
        scroll_x.config(command=tabela.xview)

    # Inserir dados
        for i in df.index:
            linha = []
            for col_csv in colunas_csv:
                valor = df[col_csv][i] if col_csv in df.columns else ""
                linha.append(str(valor))
        # Insere a linha como uma string separada por tab (para manter visual separação)
            tabela.insert("", "end", text="\t".join(linha))

        # Botão voltar, centralizado e com espaçamento
        tk.Button(
            self.root,
            text="Voltar",
            bg="#1e1e2f",
            fg="#ffffff",
            command=self.tela_principal
        ).pack(pady=15)


    def fazer_logout(self):
        self.usuario_logado = None
        self.tela_inicial()


if __name__ == "__main__":
    app = App()
    app.root.mainloop()