import streamlit as st
import pandas as pd # Es buena práctica importarlo si trabajas con DataFrames
from agents.quantitative_agent import QuantitativeAgent

st.set_page_config(layout="wide")

# --- Título de la Aplicación ---
st.title("⚽ Director Deportivo IA - Módulo Cuantitativo")
st.markdown("Esta es la primera fase del proyecto, donde probamos la conexión con el Agente Cuantitativo.")

# --- Inicialización del Agente ---
# Usamos el nombre de archivo que nos indicaste. 
# ¡Recuerda verificar si debe ser 'stats.csv' (con punto)!
csv_file_path = 'data/stats.csv' 

@st.cache_resource
def load_quantitative_agent():
    """
    Esta función carga el agente y Streamlit la cachea para no recargar el CSV cada vez.
    """
    agent = QuantitativeAgent(csv_path=csv_file_path)
    return agent

stats_agent = load_quantitative_agent()

# Verificamos si el agente se cargó correctamente antes de continuar
if stats_agent.df is None:
    st.error(f"No se pudo cargar el archivo CSV desde '{csv_file_path}'. Por favor, revisa la ruta y el nombre del archivo.")
else:
    # --- 1. Módulo Interactivo: Buscar un Jugador Específico ---
    st.header("🔍 Búsqueda Individual de Jugador")
    
    # Creamos un campo de texto para que el usuario escriba el nombre
    player_name_input = st.text_input("Escribe el nombre del jugador que quieres analizar:", placeholder="Ej: Bukayo Saka")
    
    # Creamos un botón para iniciar la búsqueda
    if st.button("Buscar Jugador"):
        if player_name_input: # Verificamos que el usuario haya escrito algo
            with st.spinner(f"Buscando datos para {player_name_input}..."):
                player_data = stats_agent.get_player_stats(player_name_input)
                
                if "error" in player_data:
                    st.error(player_data["error"])
                else:
                    st.success(f"Datos encontrados para {player_name_input}:")
                    # Mostramos los datos de forma más organizada
                    st.json(player_data)
        else:
            st.warning("Por favor, escribe el nombre de un jugador.")

    st.divider()

    # --- 2. Módulo Interactivo: Encontrar Top Jugadores por Métrica ---
    st.header("🏆 Ranking de Jugadores por Métrica")

    # Creamos dos columnas para organizar los controles
    col1, col2 = st.columns(2)

    with col1:
        # Creamos una lista de métricas interesantes del CSV para un menú desplegable
        # ¡Asegúrate de que estos nombres de columna existan en tu CSV!
        available_metrics = ['Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 'Starts']
        selected_metric = st.selectbox("Selecciona la métrica para el ranking:", options=available_metrics)

    with col2:
        # Un campo numérico para que el usuario elija cuántos jugadores ver
        top_n_input = st.number_input("Número de jugadores a mostrar (Top N):", min_value=1, max_value=20, value=5)

    if st.button("Generar Ranking"):
        with st.spinner(f"Buscando el Top {top_n_input} en '{selected_metric}'..."):
            top_players_data = stats_agent.find_top_players(metric=selected_metric, top_n=int(top_n_input))
            
            if "error" in top_players_data[0]:
                st.error(top_players_data[0]["error"])
            else:
                st.success(f"Top {top_n_input} Jugadores por '{selected_metric}':")
                # Mostramos los datos como una tabla bonita usando Pandas
                st.dataframe(pd.DataFrame(top_players_data))
