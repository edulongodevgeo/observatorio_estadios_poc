# acompanhamentos.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show_acompanhamentos(df_estadios, df_equipes):
    st.title("Acompanhamentos e Gráficos")

    # Merge entre as tabelas de estadios e equipes
    df_merged = pd.merge(df_estadios, df_equipes, how='left', left_on='id_estadio', right_on='id_estadio')


    # Gráfico de Barras: Quantidade de Estádios por Estado
    st.subheader("Quantidade de Estádios por Estado")
    df_qtd_estadios = df_estadios.drop_duplicates(subset=['uf', 'estadio']).groupby('uf')['estadio'].count().reset_index()
    fig_qtd_estadios = px.bar(df_qtd_estadios, x='uf', y='estadio', color='estadio',
                            labels={'estadio': 'Quantidade de Estádios'},
                            title='Quantidade de Estádios por Estado')
    st.plotly_chart(fig_qtd_estadios)

   
    # Gráfico de Barras: Quantidade de Estádios por Série
    st.subheader("Quantidade de Estádios por Série")
    df_qtd_estadios_serie = df_merged.drop_duplicates(subset=['serie', 'estadio']).groupby('serie')['estadio'].count().reset_index()
    fig_qtd_estadios_serie = px.bar(df_qtd_estadios_serie, x='serie', y='estadio', color='estadio',
                                    labels={'estadio': 'Quantidade de Estádios'},
                                    title='Quantidade de Estádios por Série')
    st.plotly_chart(fig_qtd_estadios_serie)
    
    # Gráfico de Barras: Capacidade Média por Estado
    st.subheader("Capacidade Média por Estado")
    df_estadios['capacidade'] = pd.to_numeric(df_estadios['capacidade'], errors='coerce')
    df_media_capacidade = df_estadios.groupby('uf')['capacidade'].mean().reset_index()
    fig_media_capacidade = px.bar(df_media_capacidade, x='uf', y='capacidade', color='capacidade',
                                  labels={'capacidade': 'Capacidade Média'},
                                  title='Capacidade Média por Estado')
    st.plotly_chart(fig_media_capacidade)

  # Mapa de Estádios por Estado
    st.subheader("Mapa de Estádios por Estado")
    fig_mapa_estadios = px.scatter_geo(df_estadios, lat='latitude', lon='longitude', color='uf',
                                       hover_name='estadio', size_max=15, template='plotly_dark',
                                       title='Estádios por Estado')
    st.plotly_chart(fig_mapa_estadios)