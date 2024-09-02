import pandas as pd
import os
from datetime import datetime

def process_file_for_grad(file_path):
    """
    Function to process files for Graduação (Superior).
    Renames 'Tipo de Vaga' to 'Forma de Ingresso' for Graduação level.
    """
    df = pd.read_excel(file_path)
    
    # Splitting the "Cargo" column into 'Curso', 'Modalidade', 'Campus', 'Turno', 'Tipo de Vaga'
    cargo_split = df['Cargo'].str.split(' - ', expand=True)
    
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
    

    df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
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

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 'Deferidas', 'Homologadas', 'FormaIngresso']]
    
    return final_df


def process_file_for_tec(file_path):
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
        
    
    df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Técnico Integrado em","")
                                    .replace("Técnico Integrado","")
                                    .replace("Técnico Subsequente em","").strip().upper())
    df['Modalidade'] = df['Modalidade'].apply(lambda r: str(r).replace("Curso Técnico","").strip())

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 
                   'Deferidas', 'Homologadas', 'FormaIngresso']]
    
    return final_df


def process_file_for_sub(file_path):
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
        
    
    df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Técnico Subsequente","")
                                    .replace("Técnico Subsequente em","").strip().upper())
    

    # Selecting and reordering the desired columns
    final_df = df[['Curso', 'Modalidade', 'Campus', 'Turno', 'Nivel', 'Inscritos', 'Pagos', 
                   'Deferidas', 'Homologadas', 'FormaIngresso']]
    
    return final_df


def diff(df1, df2, tipo="Curso"):
    
    df11 = df1.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df11.set_index(tipo, inplace=True)

    df22 = df2.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df22.set_index(tipo, inplace=True)

    return (df22 - df11).reset_index().sort_values("Inscritos")


def get_last_modified_file(path):

    # Obtém o tempo de modificação em segundos desde a época
    timestamp = os.path.getmtime(path)

    # Converte o timestamp para uma data legível
    data_modificacao = datetime.fromtimestamp(timestamp)

    return data_modificacao.strftime("%d/%m/%Y %H:%M:%S")