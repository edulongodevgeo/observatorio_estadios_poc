# acompanhamentos.py
import streamlit as st
import pandas as pd
import plotly.express as px


def show_acompanhamentos(df_estadios, df_equipes):
    #st.title("Acompanhamentos e Gráficos")

    # Merge entre as tabelas de estadios e equipes
    df_merged = pd.merge(df_estadios, df_equipes, how='left', left_on='id_estadio', right_on='id_estadio')


    # Crie o gráfico de barras
    #st.subheader("Quantidade de Estádios por Estado")
    df_qtd_estadios = df_estadios.drop_duplicates(subset=['uf', 'estadio']).groupby('uf')['estadio'].count().reset_index()
    fig_qtd_estadios = px.bar(df_qtd_estadios, x='uf', y='estadio', color='estadio',
                                labels={'estadio': 'Quantidade de Estádios'},
                                title='Quantidade de Estádios por UF')

    # Calcule a média da quantidade de estádios por estado
    media_qtd_estadios = df_qtd_estadios['estadio'].mean()

    # Adicione a linha horizontal para a média por estado
    fig_qtd_estadios.add_hline(y=media_qtd_estadios, line_dash="dash", line_color="red",
                                    annotation_text=f'Média por Estado: {media_qtd_estadios:.2f}', 
                                    annotation_position="bottom right")

    # Renderize o gráfico
    st.plotly_chart(fig_qtd_estadios)

   
    # Gráfico de Barras: Quantidade de Estádios por Série
    #st.subheader("Quantidade de Estádios por Série")
    df_qtd_estadios_serie = df_merged.drop_duplicates(subset=['serie', 'estadio']).groupby('serie')['estadio'].count().reset_index()
    fig_qtd_estadios_serie = px.bar(df_qtd_estadios_serie, x='serie', y='estadio', color='estadio',
                                    labels={'estadio': 'Quantidade de Estádios'},
                                    title='Quantidade de Estádios por Série')
    st.plotly_chart(fig_qtd_estadios_serie)
    
    # Crie o gráfico de barras
    #st.subheader("Capacidade Média por Estado")
    df_estadios['capacidade'] = pd.to_numeric(df_estadios['capacidade'], errors='coerce')
    df_media_capacidade = df_estadios.groupby('uf')['capacidade'].mean().reset_index()
    fig_media_capacidade = px.bar(df_media_capacidade, x='uf', y='capacidade', color='capacidade',
                                  labels={'capacidade': 'Capacidade Média'},
                                  title='Capacidade Média por UF')

    # Calcule a média global
    media_global = df_estadios['capacidade'].mean()

    # Adicione a linha horizontal para a média global
    fig_media_capacidade.add_hline(y=media_global, line_dash="dash", line_color="red",
                                    annotation_text=f'Média Global: {media_global:.2f}', 
                                    annotation_position="bottom right")

    # Renderize o gráfico
    st.plotly_chart(fig_media_capacidade)
    
    
    # Gráfico de Barras: Mínimo e Máximo de Capacidade por Estado
    #st.subheader("Mínimo e Máximo de Capacidade por Estado")
    # Convertendo a coluna 'capacidade' para numérica
    df_estadios['capacidade'] = pd.to_numeric(df_estadios['capacidade'], errors='coerce')
    # Calculando o mínimo e o máximo de capacidade por estado
    df_min_max_capacidade = df_estadios.groupby('uf')['capacidade'].agg(['min', 'max']).reset_index()
    # Renomeando as colunas para facilitar a compreensão no gráfico
    df_min_max_capacidade.rename(columns={'min': 'Mínimo', 'max': 'Máximo'}, inplace=True)
    # Criando o gráfico de barras
    fig_min_max_capacidade = px.bar(df_min_max_capacidade, x='uf', y=['Mínimo', 'Máximo'],
                                    barmode='group',
                                    labels={'value': 'Capacidade', 'variable': 'Tipo'},
                                    title='Mínimo e Máximo de Capacidade por UF')
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_min_max_capacidade)

  # Mapa de Estádios por Estado
    #st.subheader("Mapa de Estádios por Estado")
    fig_mapa_estadios = px.scatter_geo(df_estadios, lat='latitude', lon='longitude', color='uf',
                                       hover_name='estadio', size_max=15, template='plotly_dark',
                                       title='Distribuição Espacial dos Estádios por UF')
    st.plotly_chart(fig_mapa_estadios)