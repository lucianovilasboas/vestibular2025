import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title="Vestibular",  page_icon="📊", layout="wide")

# def ler_excel(excel):

#     df = pd.read_excel(excel)
#     df[['Curso','Campus','Turno']]  = df['Cargo'].str.split('-',expand=True)
#     df  = df[['Curso','Tipo de Vaga','Campus','Turno',"Nivel","Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"]]
#     df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
#     df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","") )
#     df['Curso'] = df['Curso'].apply(lambda r: r
#                                     .replace("Técnico Integrado em","")
#                                     .replace("Técnico Integrado","")
#                                     .replace("Técnico Subsequente em",""))

#     return df 

def ler_excel(excel):

    df = pd.read_excel(excel)
    df[['Curso','Campus','Turno']]  = df['Cargo'].str.split('-',expand=True)
    df  = df[['Curso','Tipo de Vaga','Campus','Turno',"Nivel","Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"]]
    df.rename({"Isenções deferidas": 'Deferidas', "Inscrições homologadas": 'Homologadas'}, axis=1, inplace=True) 
    df['Campus'] = df['Campus'].apply(lambda r: r.replace("Campus","").replace("campus","").strip().upper() )
    df['Curso'] = df['Curso'].apply(lambda r: r
                                    .replace("Técnico Integrado em","")
                                    .replace("Técnico Integrado","")
                                    .replace("Técnico Subsequente em","").strip().upper())

    return df 

def diferenca(ano1,ano2):

    dfMed_2023 = ler_excel(ano1)
    dfMed_2024 = ler_excel(ano2)


    dff = pd.DataFrame()

    dff['Curso'] = dfMed_2023['Curso']
    dff['Campus'] = dfMed_2023['Campus']
    dff['Tipo de Vaga'] = dfMed_2023['Tipo de Vaga']
    dff['2023'] = dfMed_2023['Inscritos']
    dff['2024'] = dfMed_2024['Inscritos']
    dff['diff_Inscritos'] = dfMed_2024['Inscritos'] - dfMed_2023['Inscritos']
    dff['diff_Homologadas'] = dfMed_2024['Homologadas'] - dfMed_2023['Homologadas']

    return dff


def diff(df1, df2, tipo="Curso"):
    
    df11 = df1.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df11.set_index(tipo, inplace=True)

    df22 = df2.groupby(tipo)[["Inscritos","Pagos", "Deferidas","Homologadas"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
    df22.set_index(tipo, inplace=True)

    return (df22 - df11).reset_index().sort_values("Inscritos")


ano = st.sidebar.selectbox (
   "Ano...",
    ["2024-1","2023-1"],
   index=0,
   placeholder="Selecione um ano...",
)


dfMed = ler_excel(f'dados/{ano}_GestaoResultado_ResumoInscricoes_TEC.xlsx')
dfGra = ler_excel(f'dados/{ano}_GestaoResultado_ResumoInscricoes_GRAD.xlsx')

df = pd.concat([dfGra, dfMed])


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

st.subheader(f'Cursos e campus (todo IFMG) em {ano}', divider='rainbow')
col1 = st.container()
st.subheader(f'Cursos (todo IFMG) em {ano}', divider='rainbow')
col3 = st.container()
st.subheader(f'Campus (todo IFMG) em {ano}', divider='rainbow')
col4 = st.container()
st.subheader(f'Campus {campus} em {ano}', divider='rainbow')
col2 = st.container()


st.subheader(f'Tecnicos: diferença de inscrições de 2024 para 2023 (Todo IFMG)', divider='rainbow')
col5 = st.container()

st.subheader(f'Graduação: diferença de inscrições de 2024 para 2023 (Todo IFMG)', divider='rainbow')
col6 = st.container()


st.subheader(f'Técnico: diferença de inscrições de 2024 para 2023 (Todo IFMG)', divider='rainbow')
col7 = st.container()

st.subheader(f'Graduação: diferença de inscrições de 2024 para 2023 (Todo IFMG)', divider='rainbow')
col8 = st.container()


dffT = diferenca(
    'dados/2023-1_GestaoResultado_ResumoInscricoes_TEC.xlsx', 
    'dados/2024-1_GestaoResultado_ResumoInscricoes_TEC.xlsx'
)

dffG = diferenca(
    'dados/2023-1_GestaoResultado_ResumoInscricoes_GRAD.xlsx', 
    'dados/2024-1_GestaoResultado_ResumoInscricoes_GRAD.xlsx'
)



dffTC = diff(ler_excel(f'dados/2023-1_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            ler_excel(f'dados/2024-1_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            "Campus")

dffGC = diff(ler_excel(f'dados/2023-1_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            ler_excel(f'dados/2024-1_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            "Campus")


fig2 = px.bar(df_filtered, x="Curso", y=["Inscritos","Homologadas"],  barmode="group", text_auto='.2s')
col2.plotly_chart(fig2, use_container_width=True)

fig1 = px.bar(df.sort_values(by='Curso'), x="Curso", y="Inscritos", color="Campus",  text_auto='.2s')
col1.plotly_chart(fig1, use_container_width=True)

curso_total = df.groupby("Curso")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)

fig3 = px.bar(curso_total, x="Curso", y="Inscritos", color="Curso", text_auto='.2s')
col3.plotly_chart(fig3, use_container_width=True)

campus_total = df.groupby("Campus")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)
fig4 = px.bar(campus_total, x="Campus", y=["Inscritos"], color="Campus", text_auto='.2s')
col4.plotly_chart(fig4, use_container_width=True)


dffT_total =dffT.groupby("Campus")[["diff_Inscritos","diff_Homologadas"]].sum().reset_index().sort_values(by='diff_Inscritos', ascending=True)
fig5 = px.bar(dffT_total, x="Campus", y=["diff_Inscritos"], color="Campus", text_auto='.2s')
col5.plotly_chart(fig5, use_container_width=True)


dffG_total =dffG.groupby("Campus")[["diff_Inscritos","diff_Homologadas"]].sum().reset_index().sort_values(by='diff_Inscritos', ascending=True)
fig6 = px.bar(dffG_total, x="Campus", y=["diff_Inscritos"], color="Campus", text_auto='.2s')
col6.plotly_chart(fig6, use_container_width=True)




fig7 = px.bar(dffTC, x="Campus", y=["Homologadas"], color="Campus", text_auto='.2s')
col7.plotly_chart(fig7, use_container_width=True)


fig8 = px.bar(dffGC, x="Campus", y=["Homologadas"], color="Campus", text_auto='.2s')
col8.plotly_chart(fig8, use_container_width=True)