import pandas as pd
import os
from datetime import datetime
import pytz
import streamlit as st

def process_file_for_superior(file_path):
    """
    Function to process files for Graduação (Superior).
    Renames 'Tipo de Vaga' to 'Forma de Ingresso' for Graduação level.
    """
    df = pd.read_excel(file_path)
    
    # Splitting the "Cargo" column into 'Curso', 'Modalidade', 'Campus', 'Turno', 'Tipo de Vaga'
    cargo_split = df['Cargo'].str.split(r' - ', expand=True)
    
    if cargo_split.shape[1] == 3:
        df['Curso'] = cargo_split[0]
        df['Campus'] = cargo_split[1]
        df['Turno'] = cargo_split[2]
        df['Modalidade'] = 'Superior'
        df['FormaIngresso'] = df['Tipo de Vaga']
    else: 
        df['Curso'] = cargo_split[0]
        df['Modalidade'] = cargo_split[1]
        df['Campus'] = cargo_split[2]
        df['Turno'] = cargo_split[3]
        df['FormaIngresso'] = cargo_split[4]
    

    # df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Tecnologia em","").strip().upper())
    
    lista_licenciatura = ["PEDAGOGIA","MATEMÁTICA","FÍSICA","EDUCAÇÃO FÍSICA","CIÊNCIAS BIOLÓGICAS","GEOGRAFIA"]
    lista_tecnologico =  ["LOGÍSTICA","ANÁLISE E DESENVOLVIMENTO DE SISTEMAS","CONSERVAÇÃO E RESTAURO","DESIGN DE INTERIORES","GESTÃO AMBIENTAL","GESTÃO DA QUALIDADE","PROCESSOS GERENCIAIS"]

    def tipo_curso(x):
        if x in lista_licenciatura: return "Licenciatura"
        if x in lista_tecnologico: return "Tecnológico"
        return "Bacharelado"    

    df["Modalidade"] =  df["Curso"].apply(tipo_curso)
    # Primeira letra maiúscula 
    df["Nivel"] = df["Nivel"].apply(lambda x: x.capitalize())

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 'Isenções deferidas', 'Inscrições homologadas', 'FormaIngresso']]
    
    return final_df


def process_file_for_integrado(file_path):
    """
    Function to process files for Técnico level.
    Keeps the column name as 'Tipo de Vaga'.
    """
    df = pd.read_excel(file_path)
    
    # Splitting the "Cargo" column into 'Curso', 'Modalidade', 'Campus', 'Turno', 'Tipo de Vaga'
    cargo_split = df['Cargo'].str.split(' - ', expand=True)
    
    df['Curso'] = cargo_split[0] 
    df['Campus'] = cargo_split[1]
    df['Turno'] = cargo_split[2]
    df['Modalidade'] = df['Tipo de Vaga'] if 'Tipo de Vaga' in df.columns else 'Integrado'
    df['FormaIngresso'] = 'Processo Seletivo'
        
    
    # df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Técnico Integrado em","")
                                    .replace("Técnico Integrado","")
                                    .replace("Técnico Subsequente em","").strip().upper())
    df['Modalidade'] = df['Modalidade'].apply(lambda r: str(r).replace("Curso Técnico","").strip())

    # Primeira letra maiúscula 
    df["Nivel"] = df["Nivel"].apply(lambda x: x.capitalize())

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 
                   'Isenções deferidas', 'Inscrições homologadas', 'FormaIngresso']]
    
    return final_df


def process_file_for_subsequente(file_path):
    """
    Function to process files for Subsequente level.
    Keeps the column name as 'Tipo de Vaga'.
    """
    df = pd.read_excel(file_path)
    
    # Splitting the "Cargo" column into 'Curso', 'Modalidade', 'Campus', 'Turno', 'Tipo de Vaga'
    cargo_split = df['Cargo'].str.split(' - ', expand=True)
    
    df['Curso'] = cargo_split[0]
    df['Campus'] = cargo_split[1]
    df['Turno'] = cargo_split[2]
    df['Modalidade'] = df['Tipo de Vaga'] if 'Tipo de Vaga' in df.columns else 'Subsequente'
    df['FormaIngresso'] = 'Processo Seletivo'
        
    
    # df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Técnico Subsequente","")
                                    .replace("Técnico Subsequente em","").strip().upper())
    
    # Primeira letra maiúscula 
    df["Nivel"] = df["Nivel"].apply(lambda x: x.capitalize())

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 
                   'Isenções deferidas', 'Inscrições homologadas', 'FormaIngresso']]
    
    return final_df


def diff(df1, df2, tipo="Curso"):
    
    df11 = df1.groupby(tipo)[["Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df11.set_index(tipo, inplace=True)

    df22 = df2.groupby(tipo)[["Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df22.set_index(tipo, inplace=True)

    dfdiff = df22 - df11
    return dfdiff.reset_index().sort_values("Inscritos")


def get_last_modified_file(path): 

    # Obtém o tempo de modificação em segundos desde a época
    timestamp = os.path.getmtime(path)

    # Converte o timestamp para uma data legível
    data_modificacao = datetime.fromtimestamp(timestamp) 

    # Define o fuso horário para "America/Sao_Paulo"
    fuso_horario = pytz.timezone("America/Sao_Paulo")

    data_modificacao = data_modificacao.astimezone(fuso_horario)

    return data_modificacao.strftime("%d/%m/%Y %H:%M:%S")


# Função para amostrar por intervalo regular com dois valores por dia
def amostrar_dois_por_dia(df):

    # Função auxiliar para amostrar dois valores por dia, mantendo o primeiro e o último Timestamp
    def amostrar_grupo(grupo):
        # Adiciona uma coluna 'Data' extraída de 'Timestamp' para agrupar por dia
        grupo['Data'] = grupo['Timestamp'].dt.date
        # Função para garantir dois registros por dia (primeiro e último do dia)
        def amostrar_dia(dia_grupo):
            if len(dia_grupo) > 2:
                return pd.concat( [dia_grupo.iloc[[0]], dia_grupo.iloc[[-1]]] )
            else:
                return dia_grupo
        
        # Aplica a função de amostragem a cada dia
        return grupo.groupby('Data', group_keys=False).apply(amostrar_dia).drop(columns='Data')
    
    # Agrupa por 'Campus', 'Curso','Modalidade','FormaIngresso' e aplica a amostragem de dois valores por dia
    amostrado = df.groupby(['Campus', 'Curso','Modalidade','FormaIngresso'], group_keys=False).apply(amostrar_grupo).reset_index(drop=True)
    
    return amostrado.sort_values(by='Timestamp')




@st.cache_data(ttl=3600) # Força a atualização do cache a cada 1 hora (3600 segundos)
def load_data():
    df_all = pd.read_excel("dados/processed/all_data.xlsx")
    return amostrar_dois_por_dia(df_all)
