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
            # Usamos el nombre de tu archivo como lo indicaste
            self.df = pd.read_csv(data/stats.csv)
            print("Dataset cargado exitosamente.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {data/stats.csv}")
            self.df = None

    def get_player_stats(self, player_name: str) -> dict:
        """
        Busca un jugador por su nombre y devuelve todas sus estadísticas.
        """
        if self.df is None:
            return {"error": "El dataset no está cargado."}
        
        # Busca al jugador en la columna 'Player'
        player_data = self.df[self.df['Player'].str.contains(player_name, case=False, na=False)]
        
        if player_data.empty:
            return {"error": f"No se encontraron datos para el jugador: {player_name}"}
        
        # Devuelve la primera coincidencia como un diccionario
        return player_data.iloc[0].to_dict()

    def find_top_players(self, metric: str, top_n: int = 5) -> list:
        """
        Encuentra los 'top_n' jugadores en una métrica específica (ej: 'Gls', 'Ast', 'xG').
        """
        if self.df is None:
            return [{"error": "El dataset no está cargado."}]
            
        if metric not in self.df.columns:
            # Importante: verifica que la métrica solicitada exista en el archivo
            return [{"error": f"La métrica '{metric}' no existe en el dataset. Las columnas disponibles son: {list(self.df.columns)}"}]

        # Ordena el DataFrame por la métrica y toma los 'top_n' mejores
        top_players_df = self.df.sort_values(by=metric, ascending=False).head(top_n)
        
        # Devuelve una lista de diccionarios con la información clave
        return top_players_df[['Player', 'Squad', 'Age', metric]].to_dict('records')

# Ejemplo de cómo se usaría (puedes ejecutar este archivo directamente para probar)
if __name__ == '__main__':
    # Asegúrate de que la ruta y el nombre del archivo sean correctos
    agent = QuantitativeAgent('data/stats.csv') # Cambia 'stats.csv' si tu archivo se llama diferente
    if agent.df is not None:
        
        # Prueba 1: Obtener estadísticas de un jugador
        player_stats = agent.get_player_stats("Max Aarons")
        print("\nEstadísticas de Max Aarons:")
        print(player_stats)
        
        # Prueba 2: Encontrar los 5 máximos goleadores usando la columna 'Gls'
        top_scorers = agent.find_top_players(metric="Gls", top_n=5)
        print("\nTop 5 Goleadores (Gls):")
        print(top_scorers)

        # Prueba 3: Encontrar los 5 máximos asistidores usando la columna 'Ast'
        top_assisters = agent.find_top_players(metric="Ast", top_n=5)
        print("\nTop 5 Asistidores (Ast):")
        print(top_assisters)
