import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown('''
            <style>
            div.block-container { 
            padding: 50px 
            }

            html, body, [class*="css"]  {
                overflow: hidden !important;
            }
            </style>
            ''', unsafe_allow_html=True)
st.title('Accidents in brazilian roads')

acidentes = pd.read_parquet('Accidents/data/acidentes.parquet').astype({'tipo_veiculo': 'object'}).set_index('momento')

st.sidebar.header('Filtros')
vehicles = st.sidebar.multiselect(
    "Selecione os veículos",
    options=acidentes.tipo_veiculo.unique(),
    default=acidentes.tipo_veiculo.unique()
)

acidentes = acidentes[acidentes.tipo_veiculo.isin(vehicles)]

col1, col2, col3, col4 = st.columns(4)
width, height = 1000, 300
data = acidentes.resample('d').count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Dia', 'br': 'Total acidentes'},  width=width, height=height)
col1.plotly_chart(fig)


data = acidentes.groupby('dia_semana').count().reset_index()
fig = px.line(data, x = 'dia_semana', y = 'br', labels={'dia_semana': 'semana', 'br': 'Total acidentes'},  width=width, height=height)
col2.plotly_chart(fig)


data = acidentes.groupby(acidentes.index.month).count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Mês', 'br': 'Total acidentes'},  width=width, height=height)
col3.plotly_chart(fig)


data = acidentes.groupby(acidentes.index.hour).count().reset_index()
fig = px.line(data, x = 'momento', y = 'br', labels={'momento': 'Hora', 'br': 'Total acidentes'},  width=width, height=height)
col4.plotly_chart(fig)



col5, col6, col7 = st.columns(3)

data = acidentes.causa_acidente.value_counts().head(10)
fig = px.bar(data, orientation='h', labels={'causa_acidente': 'Causa acidente', 'value': 'Total acidentes'})
fig.update_traces(
    customdata=data.values.reshape(-1, 1), # Add the values to customdata
    hovertemplate='%{customdata[0]}<extra></extra>' # Display only the customdata value
)
fig.update_layout(showlegend=False)
fig.update_yaxes(categoryorder='total ascending')
col5.plotly_chart(fig)


gdf =gpd.read_file('Accidents/data/states-br.json')
m = folium.Map(location=[gdf.geometry.centroid.y.mean()-2, gdf.geometry.centroid.x.mean()-5], zoom_start=3.7)
col7.write([gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()])
folium.GeoJson(gdf).add_to(m)

# Display the map in Streamlit
with col7:
    st_folium(m)