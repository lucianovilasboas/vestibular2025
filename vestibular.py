import streamlit as st 
import pandas as pd 
import plotly.express as px
from funcoes import process_file_for_tec, process_file_for_grad, process_file_for_sub, diff 

st.set_page_config(page_title="Vestibular",  page_icon="📊", layout="wide")

ano1 = "2024-1"
ano2 = "2025-1"


ano = st.sidebar.selectbox (
   "Ano...",
    [ano2, ano1],
   index=0,
   placeholder="Selecione um ano...",
)


dfMed = process_file_for_tec(f'dados/{ano}_GestaoResultado_ResumoInscricoes_TEC.xlsx')
dfGra = process_file_for_grad(f'dados/{ano}_GestaoResultado_ResumoInscricoes_GRAD.xlsx')

if ano == ano2:
   dfSub = process_file_for_sub(f'dados/{ano}_GestaoResultado_ResumoInscricoes_SUB.xlsx')  
   df = pd.concat([dfGra, dfMed, dfSub])
else:
    df = pd.concat([dfGra, dfMed])

df['Modalidade_Curso'] = df['Modalidade'].apply(lambda x: str(x)[:3]) + ' - ' + df['Curso'] 


# st.dataframe( df_filtered )
# st.balloons() 

st.header(f'📈 Vestibular IFMG {ano}')

cola, colb = st.columns(2)


with cola:
    campus = st.selectbox (
    "Campus...",
        df["Campus"].sort_values().unique(),
    index=13,
    placeholder="Selecione o campus...",
    )

with colb:
    situacao = st.selectbox(
        "Situação da inscrição...",
        ["Inscritos","Pagos", "Deferidas","Homologadas"],
        index=0,
    )

df_filtered = df[ df['Campus']==campus ]


st.subheader(f'Total de {situacao} no Campus {campus} em {ano}', divider='rainbow')
col2 = st.container()

st.subheader(f'Total de Inscrições por Cursos e campus (todo IFMG) em {ano}', divider='rainbow')
col1 = st.container()

st.subheader(f'Total de Inscrições por Cursos (todo IFMG) em {ano}', divider='rainbow')
col3 = st.container()

st.subheader(f'Total de Inscrições por Campus em {ano}', divider='rainbow')
options_col4 = st.multiselect(
    "Situação da inscrição...",
    ["Inscritos","Pagos", "Deferidas","Homologadas"],
    ["Inscritos"], key='options_col4'
)
col4 = st.container()

st.subheader(f'Total de Inscrições por Edital em {ano}', divider='rainbow')
col10 = st.container()

st.subheader(f'Comparando {ano2} com {ano1} (Todo IFMG)', divider='blue')
options_col7 = st.multiselect(
    "Situação da inscrição...",
    ["Inscritos","Pagos", "Deferidas","Homologadas"],
    ["Inscritos"], key='options_col7'
)
st.subheader(f'Técnico Integrado ({ano2} - {ano1})', divider='rainbow')
col7 = st.container()

st.subheader(f'Superior ({ano2} - {ano1})', divider='rainbow')
col8 = st.container()

st.subheader(f'Subsequente ({ano2} - {ano1})', divider='rainbow')
col9 = st.container()
col9.write("Em desenvolvimento...")


dffTC = diff(process_file_for_tec(f'dados/{ano1}_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            process_file_for_tec(f'dados/{ano2}_GestaoResultado_ResumoInscricoes_TEC.xlsx'), 
            "Campus")

dffGC = diff(process_file_for_grad(f'dados/{ano1}_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            process_file_for_grad(f'dados/{ano2}_GestaoResultado_ResumoInscricoes_GRAD.xlsx'), 
            "Campus")


fig2 = px.bar(df_filtered, x="Modalidade_Curso", y=situacao,  barmode="group", color="FormaIngresso", text_auto='.2s')
fig2.update_xaxes(title='')
col2.plotly_chart(fig2, use_container_width=True)


fig1 = px.bar(df.sort_values(by='Curso'), x="Modalidade_Curso", y="Inscritos", color="Campus",  text_auto='.2s')
fig1.update_xaxes(title='')
col1.plotly_chart(fig1, use_container_width=True)

curso_total = df.groupby("Modalidade_Curso")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)

fig3 = px.bar(curso_total, x="Modalidade_Curso", y="Inscritos", color="Modalidade_Curso", text_auto='.2s')
fig3.update_xaxes(title='')
fig3.update_layout(showlegend=False)
col3.plotly_chart(fig3, use_container_width=True)

campus_total = df.groupby("Campus")[options_col4].sum().reset_index().sort_values(by=options_col4[0], ascending=False)
fig4 = px.bar(campus_total, x="Campus", y=options_col4, text_auto='.2s')
fig4.update_xaxes(title='')
fig4.update_layout(showlegend=False)
col4.plotly_chart(fig4, use_container_width=True)


modalidade_total = df.groupby("Modalidade")[options_col4].sum().reset_index().sort_values(by=options_col4[0], ascending=False)
fig10 = px.bar(modalidade_total, x="Modalidade", y=options_col4, text_auto='.2s')
fig10.update_xaxes(title='')
fig10.update_layout(showlegend=False) 
col10.plotly_chart(fig10, use_container_width=True)


fig7 = px.bar(dffTC, x="Campus", y=options_col7, text_auto='.2s')
fig7.update_xaxes(side='top', title='')
col7.plotly_chart(fig7, use_container_width=True)


fig8 = px.bar(dffGC, x="Campus", y=options_col7, text_auto='.2s')
fig8.update_xaxes(side='top', title='')
col8.plotly_chart(fig8, use_container_width=True)


