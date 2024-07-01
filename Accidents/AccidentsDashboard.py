import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px

st.title('Accidents in brazilian roads')


acidentes = pd.read_parquet('Accidents/data/acidentes.parquet').astype({'tipo_veiculo': 'object'}).set_index('momento')

st.sidebar.header('Filtros')
vehicles = st.sidebar.multiselect(
    "Selecione os veículos",
    options=acidentes.tipo_veiculo.unique(),
    default=acidentes.tipo_veiculo.unique()
)

acidentes = acidentes[acidentes.tipo_veiculo.isin(vehicles)]


data = acidentes.resample('d').count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Dia', 'br': 'Total acidentes'})
st.plotly_chart(fig)


data = acidentes.groupby('dia_semana').count().reset_index()
fig = px.line(data, x = 'dia_semana', y = 'br', labels={'dia_semana': 'semana', 'br': 'Total acidentes'})
st.plotly_chart(fig)


data = acidentes.groupby(acidentes.index.month).count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Mês', 'br': 'Total acidentes'})
st.plotly_chart(fig)

data = acidentes.groupby(acidentes.index.hour).count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Hora', 'br': 'Total acidentes'})
st.plotly_chart(fig)