import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["Data from CSV file", "Image from url", "Data from Mysql 1", "Data from Mysql 2"])

with tab1:
   df = pd.read_csv('dados.csv')
   st.header("Dados")
   st.dataframe(df)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)



with tab3:
# Initialize connection.
   conn = st.experimental_connection( 'mysql', type="sql" )
   st.header("Docentes")
   df = conn.query('SELECT * FROM `docentes` WHERE 1;', ttl=600)
   st.dataframe(df)

with tab4:
   conn = st.experimental_connection( 'mysql', type="sql" )
   st.header("Calendario")
   df = conn.query('SELECT * FROM `calendario` ORDER BY `id` DESC', ttl=600)
   st.dataframe(df)

   