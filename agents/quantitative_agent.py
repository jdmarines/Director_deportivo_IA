import pandas as pd

class QuantitativeAgent:
    """
    Este agente se encarga de todo el análisis de datos estructurados (el CSV).
    Carga los datos una vez y proporciona métodos para consultarlos.
    """
    def __init__(self, data/stats.csv):
        """
        El constructor carga el dataset del CSV en un DataFrame de Pandas.
        """
        try:
            print(f"Cargando dataset desde: {data/stats.csv}")
            self.df = pd.read_csv(data/stats.csv)
            print("Dataset cargado exitosamente.")
            # Opcional: Mostrar las primeras filas para verificar
            # print(self.df.head())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {data/stats.csv}")
            self.df = None

    def get_player_stats(self, player_name: str) -> dict:
        """
        Busca un jugador por su nombre y devuelve sus estadísticas.
        """
        if self.df is None:
            return {"error": "El dataset no está cargado."}
        
        # Busca al jugador (ignorando mayúsculas/minúsculas)
        player_data = self.df[self.df['Player'].str.contains(player_name, case=False, na=False)]
        
        if player_data.empty:
            return {"error": f"No se encontraron datos para el jugador: {player_name}"}
        
        # Convierte la primera fila encontrada a un diccionario y lo devuelve
        return player_data.iloc[0].to_dict()

    def find_top_players(self, metric: str, top_n: int = 5) -> list:
        """
        Encuentra los 'top_n' jugadores en una métrica específica.
        """
        if self.df is None:
            return [{"error": "El dataset no está cargado."}]
            
        if metric not in self.df.columns:
            return [{"error": f"La métrica '{metric}' no existe en el dataset."}]

        # Ordena el DataFrame por la métrica y toma los primeros 'top_n'
        top_players_df = self.df.sort_values(by=metric, ascending=False).head(top_n)
        
        # Devuelve una lista de diccionarios con la información de los jugadores
        return top_players_df[['Player', 'Club', 'Age', metric]].to_dict('records')

# Ejemplo de cómo se usaría (esto no es necesario en el archivo del agente, es solo para probar)
if __name__ == '__main__':
    # Asegúrate de que la ruta sea correcta
    agent = QuantitativeAgent('data/fbref_stats_2024-2025.csv')
    if agent.df is not None:
        # Prueba 1: Obtener estadísticas de un jugador
        player_stats = agent.get_player_stats("Bukayo Saka")
        print("\nEstadísticas de Bukayo Saka:")
        print(player_stats)
        
        # Prueba 2: Encontrar los 5 máximos goleadores
        top_scorers = agent.find_top_players(metric="Performance_Gls", top_n=5)
        print("\nTop 5 Goleadores:")
        print(top_scorers)
