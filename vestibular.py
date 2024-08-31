import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title="Vestibular",  page_icon="📊", layout="wide")

ano1 = "2024-1"
ano2 = "2025-1"

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
    df['Modalidade'] = df['Tipo de Vaga'] if 'Tipo de Vaga' in df.columns else 'Curso Técnico Integrado'
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


def diff(df1, df2, tipo="Curso"):
    
    df11 = df1.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df11.set_index(tipo, inplace=True)

    df22 = df2.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df22.set_index(tipo, inplace=True)

    return (df22 - df11).reset_index().sort_values("Inscritos")


ano = st.sidebar.selectbox (
   "Ano...",
    [ano2, ano1],
   index=0,
   placeholder="Selecione um ano...",
)


dfMed = process_file_for_tec(f'dados/{ano}_GestaoResultado_ResumoInscricoes_TEC.xlsx')
dfGra = process_file_for_grad(f'dados/{ano}_GestaoResultado_ResumoInscricoes_GRAD.xlsx')

df = pd.concat([dfGra, dfMed])
df['Modalidade_Curso'] = df['Modalidade'].apply(lambda x: str(x)) + ' - ' + df['Curso']

campus = st.sidebar.selectbox (
   "Campus...",
    df["Campus"].sort_values().unique(),
   index=13,
   placeholder="Selecione o campus...",
)


df_filtered = df[ df['Campus']==campus ]


# st.dataframe( df_filtered )
# st.balloons() 

st.header(f'Vestibular IFMG {ano}')

situacao = st.selectbox(
    "Situação da inscrição...",
    ["Inscritos","Pagos", "Deferidas","Homologadas"],
    index=0,

)

st.subheader(f'Total de Inscrições no Campus {campus} em {ano}', divider='rainbow')
col2 = st.container()

st.subheader(f'Total de Inscrições por Cursos e campus (todo IFMG) em {ano}', divider='rainbow')
col1 = st.container()

st.subheader(f'Total de Inscrições por Cursos (todo IFMG) em {ano}', divider='rainbow')
col3 = st.container()

st.subheader(f'Total de Inscrições por Campus em {ano}', divider='rainbow')
col4 = st.container()



options = st.multiselect(
    "Situação da inscrição...",
    ["Inscritos","Pagos", "Deferidas","Homologadas"],
    ["Inscritos"]
)

st.subheader(f'Técnico: diferença de "{", ".join(options)}" de {ano2} para {ano1} (Todo IFMG)', divider='rainbow')
col7 = st.container()

st.subheader(f'Graduação: diferença de "{", ".join(options)}" de {ano2} para {ano1} (Todo IFMG)', divider='rainbow')
col8 = st.container()




dffTC = diff(process_file_for_tec(f'dados/{ano1}_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            process_file_for_tec(f'dados/{ano2}_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            "Campus")

dffGC = diff(process_file_for_grad(f'dados/{ano1}_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            process_file_for_grad(f'dados/{ano2}_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            "Campus")


fig2 = px.bar(df_filtered, x="Modalidade_Curso", y=situacao,  barmode="group", color="FormaIngresso", text_auto='.2s')
fig2.update_xaxes(title='')
col2.plotly_chart(fig2, use_container_width=True)


fig1 = px.bar(df.sort_values(by='Curso'), x="Curso", y="Inscritos", color="Campus",  text_auto='.2s')
fig1.update_xaxes(title='')
col1.plotly_chart(fig1, use_container_width=True)

curso_total = df.groupby("Curso")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)

fig3 = px.bar(curso_total, x="Curso", y="Inscritos", color="Curso", text_auto='.2s')
fig3.update_xaxes(title='')
fig3.update_layout(showlegend=False)
col3.plotly_chart(fig3, use_container_width=True)

campus_total = df.groupby("Campus")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
fig4 = px.bar(campus_total, x="Campus", y=["Inscritos"], color="Campus", text_auto='.2s')
fig4.update_xaxes(title='')
fig4.update_layout(showlegend=False)
col4.plotly_chart(fig4, use_container_width=True)





fig7 = px.bar(dffTC, x="Campus", y=options, text_auto='.2s')
fig7.update_xaxes(side='top', title='')
col7.plotly_chart(fig7, use_container_width=True)


fig8 = px.bar(dffGC, x="Campus", y=options, text_auto='.2s')
fig8.update_xaxes(side='top', title='')
col8.plotly_chart(fig8, use_container_width=True)