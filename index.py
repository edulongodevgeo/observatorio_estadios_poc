import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static
import acompanhamentos as acompanhamentos
import criadores as criadores


# URL da API para dados de estadios
url_estadios = "https://script.google.com/macros/s/AKfycbxXLuq-aI8L--wVGv3k5_aVddf4i36qEotGYC4sfCK1giSgUYTQu-1zZ_gp2LjKtAMn/exec?action=getAllEstadios"

# URL da API para dados de equipes/times
url_equipes = "https://script.google.com/macros/s/AKfycbxXLuq-aI8L--wVGv3k5_aVddf4i36qEotGYC4sfCK1giSgUYTQu-1zZ_gp2LjKtAMn/exec?action=getAllEquipes"

# Fazendo a solicitação à API para dados de estadios
response_estadios = requests.get(url_estadios)

# Verificando se a resposta foi bem-sucedida (código de status 200) para dados de estadios
if response_estadios.status_code == 200:
    # Tentando obter os dados do JSON para estadios
    try:
        data_estadios = response_estadios.json()
        # Convertendo os dados em um DataFrame do Pandas para estadios
        df_estadios = pd.DataFrame(data_estadios)
    except ValueError as e:
        st.error(f"Erro ao decodificar JSON para estadios: {e}")
        df_estadios = pd.DataFrame()  # Criando um DataFrame vazio
else:
    st.error(f"Falha na solicitação à API para estadios. Código de status: {response_estadios.status_code}")
    df_estadios = pd.DataFrame()  # Criando um DataFrame vazio

# Fazendo a solicitação à API para dados de equipes/times
response_equipes = requests.get(url_equipes)

# Verificando se a resposta foi bem-sucedida (código de status 200) para dados de equipes/times
if response_equipes.status_code == 200:
    # Tentando obter os dados do JSON para equipes/times
    try:
        data_equipes = response_equipes.json()
        # Convertendo os dados em um DataFrame do Pandas para equipes/times
        df_equipes = pd.DataFrame(data_equipes)
    except ValueError as e:
        st.error(f"Erro ao decodificar JSON para equipes/times: {e}")
        df_equipes = pd.DataFrame()  # Criando um DataFrame vazio
else:
    st.error(f"Falha na solicitação à API para equipes/times. Código de status: {response_equipes.status_code}")
    df_equipes = pd.DataFrame()  # Criando um DataFrame vazio

# Unir os DataFrames de estadios e equipes com base no id_estadio
df_combined = pd.merge(df_estadios, df_equipes, on='id_estadio', how='left')

# Adicionando um título ao topo
st.title("Observatório de Estádios Brasileiros")

# Obtendo a escolha do usuário
page = st.sidebar.selectbox("Escolha a página:", ["Home", "Desenvolvedores", "Acompanhamentos"])

if page == "Home":
    # Adicionando opções de basemap
    basemaps = {
        "OpenStreetMap": folium.TileLayer("OpenStreetMap"),
        "CartoDB Positron": folium.TileLayer("CartoDB Positron"),
        "CartoDB Dark_Matter": folium.TileLayer("CartoDB Dark_Matter"),
        "Esri Satellite": folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri Satellite"),
        # Adicione mais basemaps conforme necessário
    }

    # Escolha do usuário para o basemap
    selected_basemap = st.selectbox("Escolha o basemap:", list(basemaps.keys()))

    # Filtros unificados abaixo do mapa
    # st.sidebar.header("Filtros")
    # for col in df_combined.columns:
    #     filter_value = st.sidebar.text_input(f"Digite o valor para o filtro em '{col}' (ou deixe em branco para mostrar todos):", '')
    #     if filter_value:
    #         df_combined = df_combined[df_combined[col].astype(str).str.contains(filter_value, case=False, na=False)]


    # Filtros unificados abaixo do mapa
    st.sidebar.header("Filtros")

    # Lista de colunas disponíveis para filtro
    filter_columns = st.sidebar.multiselect("Selecione as colunas para aplicar filtros:", df_combined.columns)

    for col in filter_columns:
        filter_value = st.sidebar.text_input(f"Digite o valor para o filtro em '{col}' (ou deixe em branco para mostrar todos). Use barra vertical '|' se quiser mais de uma alternativa. Ex.: Ao filtrar '{col}', insira A|B, para retornar dados de '{col}' A ou B.:", '')
        if filter_value:
            df_combined = df_combined[df_combined[col].astype(str).str.contains(filter_value, case=False, na=False)]


    
    # Criando o mapa com o basemap escolhido
    m = folium.Map(location=[-16.13026201203474, -47.94433593750001], zoom_start=4, control_scale=True,
                   tiles=basemaps[selected_basemap], attr="Map data © OpenStreetMap contributors")

    # Adicionando marcadores ao mapa com base nos critérios de filtro selecionados
    for _, row in df_combined.iterrows():
        try:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])
        except ValueError:
            st.warning(f"Valor inválido de latitude ou longitude para o estádio {row['estadio']}. Ignorando este estádio.")
            continue

        # Verificar se o estádio tem mais de uma equipe
        teams_at_stadium = df_combined[df_combined['id_estadio'] == row['id_estadio']]['equipe'].unique()
        teams_info = ', '.join(teams_at_stadium)

        popup_html = f"<strong>Estádio:</strong> {row['estadio']}<br>"
        popup_html += f"<strong>Cidade:</strong> {row['cidade']}<br>"
        popup_html += f"<strong>UF:</strong> {row['uf']}<br>"
        popup_html += f"<strong>Clube(s):</strong> {teams_info}"

        folium.Marker(
            location=(latitude, longitude),
            popup=folium.Popup(html=popup_html, max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Renderizando o mapa no Streamlit
    folium_static(m)

    # Exibindo a tabela filtrada no Streamlit abaixo do mapa
    st.write("### Dados Filtrados:")
    st.dataframe(df_combined)

# Restante do código...

elif page == "Desenvolvedores":
    criadores.show_creators()


elif page == "Acompanhamentos":
    acompanhamentos.show_acompanhamentos(df_estadios, df_equipes)


