import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import ast
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Función para cargar los datos
def load_data():
    possible_paths = [
        'data/movies_processed.csv',  # Ruta relativa desde src/
        '../data/movies_processed.csv',  # Ruta relativa desde el directorio raíz
        'C:/Users/ss/Desktop/c/proyecto-mlops/data/movies_processed.csv'  # Ruta absoluta
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Cargando datos desde {path}")
            return pd.read_csv(path, low_memory=False)
    
    raise FileNotFoundError("El archivo 'movies_processed.csv' no fue encontrado en ninguna ruta.")

# Función para desanidar columnas
def desanidar_columna(columna):
    try:
        # Si es una cadena, intenta convertirla en una lista
        if isinstance(columna, str) and columna.strip():
            return ast.literal_eval(columna)
        # Si no es una cadena o está vacía, devuelve una lista vacía
        return []
    except (ValueError, SyntaxError):
        # En caso de error, devuelve una lista vacía
        return []

# Cargar el dataset
movies_df = load_data()

# Verificar el formato de las columnas antes de desanidar
logger.info(f"Formato de la columna 'genres' antes de desanidar: {movies_df['genres'].head()}")
logger.info(f"Formato de la columna 'cast' antes de desanidar: {movies_df['cast'].head()}")
logger.info(f"Formato de la columna 'crew' antes de desanidar: {movies_df['crew'].head()}")

# Desanidar las columnas anidadas
movies_df['genres'] = movies_df['genres'].apply(desanidar_columna)
movies_df['cast'] = movies_df['cast'].apply(desanidar_columna)
movies_df['crew'] = movies_df['crew'].apply(desanidar_columna)

# Verificar el formato de las columnas después de desanidar
logger.info(f"Formato de la columna 'genres' después de desanidar: {movies_df['genres'].head()}")
logger.info(f"Formato de la columna 'cast' después de desanidar: {movies_df['cast'].head()}")
logger.info(f"Formato de la columna 'crew' después de desanidar: {movies_df['crew'].head()}")

# Crear una columna combinada
def create_combined_features(row):
    # Extraer géneros
    genres = ' '.join([genre for genre in row['genres']]) if row['genres'] else ''
    
    # Extraer nombres de actores
    cast = ' '.join([member.get('name', '') for member in row['cast']]) if row['cast'] else ''
    
    # Extraer nombres del equipo técnico
    crew = ' '.join([member.get('name', '') for member in row['crew']]) if row['crew'] else ''
    
    # Combinar todos los datos en una sola cadena
    return f"{row['title']} {genres} {cast} {crew}"

movies_df['combined_features'] = movies_df.apply(create_combined_features, axis=1)

# Vectorizar los datos
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies_df['combined_features'])

# Convertir a matriz dispersa para optimizar memoria
tfidf_matrix = csr_matrix(tfidf_matrix)

# Entrenar un modelo NearestNeighbors
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(tfidf_matrix)

# Función de recomendación
def recomendacion(titulo):
    try:
        logger.info(f"Buscando recomendaciones para el título: {titulo}")
        titulo = titulo.strip().lower()  # Normalizar el título
        matching_movies = movies_df[movies_df['title'].str.strip().str.lower() == titulo]
        
        if matching_movies.empty:
            logger.warning(f'Película "{titulo}" no encontrada en el dataset.')
            return {'mensaje': f'Película "{titulo}" no encontrada en el dataset.'}
        
        idx = matching_movies.index[0]
        logger.info(f"Índice de la película encontrada: {idx}")
        distances, indices = model_knn.kneighbors(tfidf_matrix[idx], n_neighbors=6)
        logger.info(f"Distancias: {distances}")
        logger.info(f"Índices: {indices}")
        recommended_movies = movies_df['title'].iloc[indices.flatten()[1:]].tolist()
        logger.info(f"Películas recomendadas: {recommended_movies}")
        return {'mensaje': f'Películas recomendadas para {titulo}: {recommended_movies}'}
    except Exception as e:
        logger.error(f"Error en la función de recomendación: {e}\n{traceback.format_exc()}")
        return {'mensaje': 'Error interno del servidor'}

# Ejemplo de uso
if __name__ == '__main__':
    print(recomendacion('The Dark Knight'))