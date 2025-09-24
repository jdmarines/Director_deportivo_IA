import streamlit as st
import pandas as pd
from agents.quantitative_agent import QuantitativeAgent
# from agents.qualitative_agent import QualitativeAgent # <-- TEMPORALMENTE DESACTIVADO

st.set_page_config(layout="wide")

# --- Título de la Aplicación ---
st.title("⚽ Director Deportivo IA - MODO DIAGNÓSTICO")
st.warning("El módulo cualitativo ha sido desactivado temporalmente para una prueba de carga.")

# --- Inicialización de los Agentes ---
@st.cache_resource
def load_quantitative_agent():
    return QuantitativeAgent(csv_path='data/stats.csv')

# @st.cache_resource
# def load_qualitative_agent():
#     return QualitativeAgent(documents_path='data/articles') # <-- TEMPORALMENTE DESACTIVADO

print("Cargando agente cuantitativo...")
stats_agent = load_quantitative_agent()
# qualitative_agent = load_qualitative_agent() # <-- TEMPORALMENTE DESACTIVADO
print("Agente cuantitativo cargado.")

# Creamos dos columnas para organizar la interfaz
col1, col2 = st.columns(2)

# ==============================================================================
# COLUMNA 1: AGENTE CUANTITATIVO
# ==============================================================================
with col1:
    st.header("📊 Módulo Cuantitativo")
    st.markdown("Análisis basado en estadísticas de rendimiento.")

    # (El resto del código del agente cuantitativo no cambia)
    st.subheader("🔍 Búsqueda por Jugador")
    player_name_input = st.text_input("Nombre del jugador:", placeholder="Ej: Bukayo Saka")
    if st.button("Buscar Estadísticas"):
        if player_name_input and stats_agent.df is not None:
            with st.spinner(f"Buscando datos para {player_name_input}..."):
                player_data = stats_agent.get_player_stats(player_name_input)
                if "error" in player_data:
                    st.error(player_data["error"])
                else:
                    st.success(f"Datos encontrados para {player_name_input}:")
                    st.json(player_data)
    
    st.divider()

    st.subheader("🏆 Ranking de Jugadores")
    if stats_agent.df is not None:
        available_metrics = ['Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 'Starts']
        selected_metric = st.selectbox("Selecciona la métrica:", options=available_metrics)
        top_n_input = st.number_input("Número de jugadores a mostrar:", min_value=1, max_value=20, value=5)

        if st.button("Generar Ranking"):
            with st.spinner(f"Buscando el Top {top_n_input} en '{selected_metric}'..."):
                top_players_data = stats_agent.find_top_players(metric=selected_metric, top_n=int(top_n_input))
                if "error" in top_players_data[0]:
                    st.error(top_players_data[0]["error"])
                else:
                    st.success(f"Top {top_n_input} Jugadores por '{selected_metric}':")
                    st.dataframe(pd.DataFrame(top_players_data))

# ==============================================================================
# COLUMNA 2: AGENTE CUALITATIVO (DESACTIVADO)
# ==============================================================================
with col2:
    st.header("🧠 Módulo Cualitativo (RAG)")
    st.markdown("`Actualmente desactivado para la prueba.`")
