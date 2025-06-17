import pandas as pd
import plotly.express as px
import os
import tkinter as tk
from tkinter import ttk
import webview  # import necessário para webview
import plotly.graph_objects as go
import numpy as np
import webbrowser


def carregar_dataset():
    df = pd.read_csv('dataset.csv')
    return df

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

def grafico_dispersao(df, resposta):
    # Define manualmente as cores para "trabalha"
    cores = {'Sim': 'red', 'Não': 'blue'}

    fig = px.scatter(
        df,
        x='idade',
        y='horas_dia_num',
        color='trabalha',
        size='horas_dia_num',
        color_discrete_map=cores,
        title="Dispersão: Idade x Horas por Dia",
        labels={
            'idade': 'Idade',
            'horas_dia_num': 'Horas',
            'trabalha': 'Trabalha'
        },
        hover_data={
            'idade': True,
            'horas_dia_num': True,
            'trabalha': True
        }
    )

    # Ponto do usuário
    fig.add_trace(go.Scatter(
        x=[resposta[2]],
        y=[resposta[4]],
        mode='markers',
        marker=dict(size=15, color='purple', line=dict(width=3, color='black')),
        name='Você',
        hovertemplate=(
            'Idade: %{x}<br>' +
            'Horas: %{y}<br>' +
            'Trabalha: ' + str(resposta[3]) + '<extra></extra>'
        )
    ))

    # Linha de tendência
    x = df['idade']
    y = df['horas_dia_num']
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)

    fig.add_trace(go.Scatter(
        x=sorted(x),
        y=poly1d_fn(sorted(x)),
        mode='lines',
        name='Tendência',
        line=dict(color='black', dash='dash')
    ))

    # Definindo limites dinâmicos com início em zero
    max_x = x.max() * 1.1  # 10% acima do maior valor de idade
    max_y = y.max() * 1.1  # 10% acima do maior valor de horas

    fig.update_layout(
        xaxis=dict(range=[0, max_x]),
        yaxis=dict(range=[0, max_y]),
        legend_title_text='Trabalha'
    )

    # Caminho completo (cria no diretório atual)
    caminho = os.path.join(os.getcwd(), 'grafico_dispersao.html')
    fig.write_html(caminho)

    return caminho


# def grafico_dispersao(df, resposta):
#     print("entrou")
#     fig = px.scatter(df, x='idade', y='horas_dia_num', color='trabalha',
#                      title="Dispersão: Idade x Horas por Dia")
#     fig.add_scatter(x=[resposta[2]], y=[resposta[4]],
#                     mode='markers', marker=dict(size=15, color='red'), name='Você')

#     caminho = 'grafico_dispersao.html'
#     fig.write_html(caminho)

#     print("Arquivo criado?", os.path.isfile(caminho))  # Deve imprimir True
#     return caminho


def grafico_barras_lateral(df):
    print("entrou")
    fig = px.bar(df, x='plataforma_mais_usada', color='impacto_relacoes', barmode='group',
                 title="Plataforma Mais Usada x Impacto nas Relações")
    caminho = 'grafico_barras_lateral.html'
    fig.write_html(caminho)
    
    print("Arquivo criado?", os.path.isfile(caminho))  # Deve imprimir True
    return caminho

def grafico_pizza(df):
    print("entrou")
    fig = px.pie(df, names='impacto_relacoes', title='Impacto nas Relações')
    caminho = 'grafico_pizza.html'
    fig.write_html(caminho)

    print("Arquivo criado?", os.path.isfile(caminho))  # Deve imprimir True
    return caminho

def grafico_barras_horario(df):
    print("entrou")
    fig = px.histogram(df, x='horario_pico', color='trabalha',
                       title='Horário de Pico x Trabalha')
    caminho = 'grafico_barras_horario.html'
    fig.write_html(caminho)

    print("Arquivo criado?", os.path.isfile(caminho))  # Deve imprimir True
    return caminho

def mostrar_grafico(caminho_html):
    print("entrou2")
    webview.create_window("Gráfico Plotly", caminho_html)
    webview.start()