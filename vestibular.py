import streamlit as st 
import pandas as pd 
import plotly.express as px
from funcoes import process_file_for_integrado, process_file_for_superior, process_file_for_subsequente, diff, get_last_modified_file 


st.set_page_config(page_title="Vestibular IFMG 2025",  page_icon="📊", layout="wide")

# anox = "2022-1"
ano0 = "2023-1"
ano1 = "2024-1"
ano2 = "2025-1"

ano = st.sidebar.selectbox (
   "Ano...",
    [ano2, ano1, ano0],
   index=0,
   placeholder="Selecione um ano...",
)

dfMed = process_file_for_integrado(f'dados/{ano}_GestaoResultado_ResumoInscricoes_Integrado.xlsx')
dfGra = process_file_for_superior(f'dados/{ano}_GestaoResultado_ResumoInscricoes_Superior.xlsx')

if ano == "2025-1":
   dfSub = process_file_for_subsequente(f'dados/{ano}_GestaoResultado_ResumoInscricoes_Subsequente.xlsx')  
   df = pd.concat([dfGra, dfMed, dfSub])
else:
   df = pd.concat([dfGra, dfMed])

df['Modalidade_Curso'] = df['Modalidade'].apply(lambda x: str(x)[:3]) + ' - ' + df['Curso'] 


df_all = pd.read_excel("dados/processed/all_data.xlsx")

# st.dataframe( df_filtered )
# st.balloons() 

st.header(f'✔️ Vestibular IFMG {ano}')
html_code = f"<div id=\"update\">Ultima atualização: {get_last_modified_file('dados/2025-1_GestaoResultado_ResumoInscricoes_Integrado.xlsx')}</div>"
st.markdown(html_code, unsafe_allow_html=True)
st.warning('Importante! Para esse levantamento estamos considerando apenas a primeira opção de curso do candidato.', icon="⚠️")



st.subheader(f'📊 Total de Inscrições em {ano}', divider='rainbow')
# col0 = st.container()
soma_colunas = df[["Inscritos", "Pagos", "Isenções deferidas", "Inscrições homologadas"]].sum()
df_soma = pd.DataFrame(soma_colunas, columns=["total"]).reset_index()
# fig0 = px.pie(df_soma, values='total', names='index')
# fig0.update_traces(textinfo='value+percent', textfont_size=22)
# col0.plotly_chart(fig0, use_container_width=True)


colx = st.container()
figx = px.bar(df_soma, x="total", y="index", color="index", text_auto='.2s')
figx.update_xaxes(title='')
figx.update_yaxes(tickformat=",d", title='', tickfont=dict(size=16))
figx.update_traces(texttemplate='%{value:.0f}',textfont_size=24)
figx.update_layout(showlegend=False)
colx.plotly_chart(figx, use_container_width=True) 

cola, colb = st.columns(2)

with cola:
    campus = st.selectbox (
    "📶 Campus...",
        df["Campus"].sort_values().unique(),
    index=0,
    placeholder="Selecione o campus...",
    )

df_filtered = df[ df['Campus']==campus ]


with colb:
    situacao = st.selectbox(
        "📶 Situação da inscrição...",
        ["Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"],
        index=3,
    )





st.subheader(f'📊 Total de {situacao} no Campus {campus} em {ano}', divider='rainbow')
col2 = st.container()
colc, cold = st.columns(2)
with colc:
    modalidade = st.selectbox(
        "📶 Modalidade...",
        df_filtered["Modalidade"].sort_values().unique(),
        index=0,
    )

df_filtered_x = df_filtered[ df_filtered['Modalidade']==modalidade ]

with cold:
    forma = st.selectbox(
        "📶 Forma de ingresso...",
        df_filtered_x["FormaIngresso"].sort_values().unique(),
        index=0,
    )    
st.subheader(f'📈 Evolução de {situacao} no Campus {campus} em 2025-1', divider='rainbow')
df_filtered2 = df_all[(df_all["Modalidade"] == modalidade) & (df_all["Campus"] == campus)&(df_all["FormaIngresso"] == forma)]
col22 = st.container()



st.subheader(f'📊 Total de Inscrições por Cursos e campus (todo IFMG) em {ano}', divider='rainbow')
col1 = st.container()

st.subheader(f'📊 Total de Inscrições por Cursos (todo IFMG) em {ano}', divider='rainbow')
col3 = st.container()

st.subheader(f'📊 Total de Inscrições por Campus em {ano}', divider='rainbow')
options_col4 = st.multiselect(
    "📶 Situação da inscrição...",
    ["Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"],
    ["Inscritos"], key='options_col4',
)
col4 = st.container()

st.subheader(f'📊 Total de Inscrições por Edital em {ano}', divider='rainbow')
col10 = st.container()


st.subheader(f'📊 Comparando os processos (Todo IFMG)', divider='blue')

col_ano1, col_ano2, options_col7 = st.columns(3)
   
with col_ano1:
    ano_sel1 = st.selectbox (
    "📶 Ano 1...",
        [ano0, ano1, ano2 ],
    index=1,
    placeholder="Selecione o ano 1...",
    )

with col_ano2:
    ano_sel2 = st.selectbox (
    "📶 Ano 2...",
        [ano2, ano1, ano0],
    index=0,
    placeholder="Selecione o ano 2...",
    )

with options_col7:
    options_col7 = st.multiselect(
        "📶 Situação da inscrição...",
        ["Inscritos","Pagos", "Isenções deferidas","Inscrições homologadas"],
        ["Inscritos"], key='options_col7'
    )


st.subheader(f'📊 Técnico Integrado: evolução de {ano_sel1} para {ano_sel2}.', divider='rainbow')
col7 = st.container()

st.subheader(f'📊 Superior: evolução de {ano_sel1} para {ano_sel2}.', divider='rainbow')
col8 = st.container()

# st.subheader(f'Subsequente ({ano_sel1} com {ano_sel2})', divider='rainbow')
# col9 = st.container()
# col9.write("Em desenvolvimento...")


dffTC = diff(process_file_for_integrado(f'dados/{ano_sel1}_GestaoResultado_ResumoInscricoes_Integrado.xlsx'), 
            process_file_for_integrado(f'dados/{ano_sel2}_GestaoResultado_ResumoInscricoes_Integrado.xlsx'), 
            "Campus")

dffGC = diff(process_file_for_superior(f'dados/{ano_sel1}_GestaoResultado_ResumoInscricoes_Superior.xlsx'), 
            process_file_for_superior(f'dados/{ano_sel2}_GestaoResultado_ResumoInscricoes_Superior.xlsx'), 
            "Campus")


fig2 = px.bar(df_filtered, x="Modalidade_Curso", y=situacao,  barmode="group", color="FormaIngresso", text_auto='.2s')
fig2.update_xaxes(title='')
fig2.update_yaxes(tickformat=",d")
fig2.update_traces(texttemplate='%{value:.0f}')

# Atualizar layout para mover a legenda para a parte inferior
fig2.update_layout(
    legend=dict(
        orientation="h",  # Orientação horizontal
        yanchor="bottom",  # Alinhar na parte inferior
        y=-0.3,  # Posição no eixo Y (ajuste conforme necessário)
        xanchor="center",  # Centralizar no eixo X
        x=0.5  # Posição central no eixo X
    )
)

col2.plotly_chart(fig2, use_container_width=True)


fig22 = px.line(df_filtered2, title=f"Campus {campus}", x="Timestamp", y=situacao, color="Curso", text=situacao)
fig22.update_xaxes(title='')
fig22.update_yaxes(tickformat=",d")

# fonte size do texto dos valores
fig22.update_traces(textfont_size=8)

# Exibe os valores no gráfico
fig22.update_traces(texttemplate='%{text:.0f}', textposition="top right")
fig22.update_layout(hovermode="x")
# Atualizar layout para mover a legenda para a parte inferior
fig22.update_layout(
    legend=dict(
        orientation="h",  # Orientação horizontal
        yanchor="bottom",  # Alinhar na parte inferior
        y=-0.3,  # Posição no eixo Y (ajuste conforme necessário)
        xanchor="center",  # Centralizar no eixo X
        x=0.5  # Posição central no eixo X
    )
)

col22.plotly_chart(fig22, use_container_width=True)




fig1 = px.bar(df.sort_values(by='Curso'), x="Modalidade_Curso", y="Inscritos", color="Campus",  text_auto='.2s')
fig1.update_xaxes(title='')
fig1.update_yaxes(tickformat=",d")
fig1.update_traces(texttemplate='%{value:.0f}')
fig1.update_layout(showlegend=False)
col1.plotly_chart(fig1, use_container_width=True)


curso_total = df.groupby("Modalidade_Curso")[["Inscritos"]].sum().reset_index().sort_values(by='Inscritos', ascending=False)

fig3 = px.bar(curso_total, x="Modalidade_Curso", y="Inscritos", color="Modalidade_Curso", text_auto='.2s')
fig3.update_xaxes(title='')
fig3.update_yaxes(tickformat=",d")
fig3.update_traces(texttemplate='%{value:.0f}')
fig3.update_layout(showlegend=False)
col3.plotly_chart(fig3, use_container_width=True)

campus_total = df.groupby("Campus")[options_col4].sum().reset_index().sort_values(by=options_col4[0], ascending=False)
fig4 = px.bar(campus_total, x="Campus", y=options_col4, text_auto='.2s')
fig4.update_xaxes(title='')
fig4.update_yaxes(tickformat=",d")
fig4.update_traces(texttemplate='%{value:.0f}')
fig4.update_layout(showlegend=False)
col4.plotly_chart(fig4, use_container_width=True)


modalidade_total = df.groupby("Modalidade")[options_col4].sum().reset_index().sort_values(by=options_col4[0], ascending=False)
fig10 = px.bar(modalidade_total, x="Modalidade", y=options_col4, text_auto='.2s')
fig10.update_xaxes(title='')
fig10.update_yaxes(tickformat=",d")
fig10.update_traces(texttemplate='%{value:.0f}')
fig10.update_layout(showlegend=False) 
col10.plotly_chart(fig10, use_container_width=True)


fig7 = px.bar(dffTC, x="Campus", y=options_col7, text_auto='.2s')
fig7.update_xaxes(side='top', title='')
fig7.update_yaxes(tickformat=",d")
fig7.update_traces(texttemplate='%{value:.0f}')
col7.plotly_chart(fig7, use_container_width=True)


fig8 = px.bar(dffGC, x="Campus", y=options_col7, text_auto='.2s')
fig8.update_xaxes(side='top', title='')
fig8.update_yaxes(tickformat=",d")
fig8.update_traces(texttemplate='%{value:.0f}')
col8.plotly_chart(fig8, use_container_width=True)


