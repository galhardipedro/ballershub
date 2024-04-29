import streamlit as st

import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import Error
import sys, os
from datetime import datetime, timedelta
import sqlite3

import warnings
warnings.filterwarnings('ignore')

import streamlit as st

# Function to create the SQLite database and table
def create_table():
    conn = sqlite3.connect('ballershub_survey.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS survey_questions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  interest_level INTEGER,
                  events INTEGER,
                  playing_frequency TEXT,
                  previous_leagues TEXT,
                  max_distance INTEGER,
                  age INTEGER,
                  location TEXT,
		  experience TEXT,
                  features TEXT)''')
    conn.commit()
    conn.close()

# Introdução
st.title('Basketball Community Platform Survey')
st.write('Por favor, responda as perguntas abaixo:')

# Perguntas Quantitativas e Qualitativas
with st.form('survey_questions'):

    st.write('1. Se você tivesse a oportunidade, qual seria o seu nível de interesse em participar de uma liga amadora de basquete?')
    interest_level = st.slider('Selecione seu nível de interesse', 0, 10, 5)

    st.write('2. Qual o seu nível de interesse em participar de eventos voltados para a comunidade do basquete no Brasil?')
    events = st.slider('Selecione o nível de interesse', 0, 10, 5)

    st.write('3. Com que frequência você joga basquete atualmente?')
    playing_frequency = st.radio('Selecione sua frequência de jogo:', ('Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre'))

    st.write('4. Você já participou de alguma liga amadora de basquete?')
    previous_leagues = st.radio('Sua resposta', ('Sim','Não'))

    st.write('5. Qual é a distância máxima que você estaria disposto(a) a percorrer para participar de uma liga de basquete?')
    max_distance = st.select_slider('Selecione a distância máxima (em km)', options=[1, 5, 10, 20, 50, 100])

    st.write('6. Quantos anos você tem?')
    age = st.number_input('Entre sua idade', min_value=18, max_value=50, value=30)

    st.write('7. Onde você mora?')
    location = st.text_input('Escreva bairro/cidade', key='location')

    st.write('8. O que você mais gostaria de experimentar em uma liga de basquete?')
    experience = st.text_area('Escreva sua resposta aqui', key='experience')

    st.write('9. Que recursos ou funcionalidades você gostaria de ver em uma plataforma online que promove e organiza ligas de basquete?')
    features = st.text_area('Escreva sua resposta aqui', key='features')


    submit_button = st.form_submit_button(label='Enviar')


# Exibir mensagem de sucesso após o envio do formulário
if submit_button:
    st.success('Recebemos o seu envio. Obrigado por participar da nossa pesquisa!')

# Função para inserir os dados no banco de dados
def insert_data(table_name, **kwargs):
    conn = sqlite3.connect('ballershub_survey.db')
    c = conn.cursor()
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?' for _ in range(len(kwargs))])
    values = tuple(kwargs.values())
    c.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', values)
    conn.commit()
    conn.close()

# Criar a tabela no banco de dados (se não existir)
create_table()

# Inserir os dados no banco de dados após o envio do formulário
if submit_button:
    insert_data('survey_questions', 
                interest_level=interest_level,
                events=events,
                playing_frequency=playing_frequency, 
                previous_leagues=previous_leagues, 
                max_distance=max_distance,
                age=age,
                location=location,
                experience=experience, 
                features=features)
