from fastapi import FastAPI
from typing import Optional
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Inicializar la aplicación FastAPI
app = FastAPI()

# Cargar el dataset procesado
movies_df = pd.read_csv('C:/Users/ss/Desktop/c/proyecto-mlops/data/movies_processed.csv', low_memory=False)

# Convertir columnas anidadas a listas
def convert_to_list(column):
    return column.apply(lambda x: eval(x) if isinstance(x, str) else [])

movies_df['genres'] = convert_to_list(movies_df['genres'])
movies_df['cast'] = convert_to_list(movies_df['cast'])
movies_df['crew'] = convert_to_list(movies_df['crew'])

# Convertir release_date a datetime
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')

# Endpoint raíz
@app.get('/')
def read_root():
    return {'mensaje': 'Bienvenido a la API de películas'}

# 1. Cantidad de filmaciones por mes
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    mes_numero = meses.get(mes.lower(), None)
    if mes_numero is None:
        return {'mensaje': 'Mes no válido. Ingrese un mes en español.'}
    
    cantidad = movies_df[movies_df['release_date'].dt.month == mes_numero].shape[0]
    return {'mensaje': f'{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}'}

# 2. Cantidad de filmaciones por día
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'sabado': 5, 'domingo': 6
    }
    dia_numero = dias.get(dia.lower(), None)
    if dia_numero is None:
        return {'mensaje': 'Día no válido. Ingrese un día en español.'}
    
    cantidad = movies_df[movies_df['release_date'].dt.dayofweek == dia_numero].shape[0]
    return {'mensaje': f'{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}'}

# 3. Score de una película por título
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    titulo = titulo.strip().lower()
    matching_movies = movies_df[movies_df['title'].str.strip().str.lower() == titulo]
    if matching_movies.empty:
        return {'mensaje': f'Película "{titulo}" no encontrada en el dataset.'}
    
    movie = matching_movies.iloc[0]
    return {
        'mensaje': f'La película {movie["title"]} fue estrenada en el año {movie["release_year"]} '
                   f'con un score/popularidad de {movie["popularity"]}'
    }

# 4. Votos de una película por título
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    titulo = titulo.strip().lower()
    matching_movies = movies_df[movies_df['title'].str.strip().str.lower() == titulo]
    if matching_movies.empty:
        return {'mensaje': f'Película "{titulo}" no encontrada en el dataset.'}
    
    movie = matching_movies.iloc[0]
    if movie['vote_count'] < 2000:
        return {'mensaje': f'La película "{titulo}" no cumple con la condición de tener al menos 2000 valoraciones.'}
    
    return {
        'mensaje': f'La película {movie["title"]} fue estrenada en el año {movie["release_year"]}. '
                   f'La misma cuenta con un total de {movie["vote_count"]} valoraciones, con un promedio de {movie["vote_average"]}.'
    }

# 5. Información de un actor por nombre
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    actor_movies = movies_df[movies_df['cast'].apply(lambda x: nombre_actor in [actor['name'] for actor in x])]
    if actor_movies.empty:
        return {'mensaje': f'Actor "{nombre_actor}" no encontrado en el dataset.'}
    
    cantidad_peliculas = len(actor_movies)
    retorno_total = actor_movies['return'].sum()
    retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    
    return {
        'mensaje': f'El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, '
                   f'el mismo ha conseguido un retorno de {retorno_total:.2f} con un promedio de {retorno_promedio:.2f} por filmación.'
    }

# 6. Información de un director por nombre
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    director_movies = movies_df[movies_df['crew'].apply(lambda x: nombre_director in [crew['name'] for crew in x])]
    if director_movies.empty:
        return {'mensaje': f'Director "{nombre_director}" no encontrado en el dataset.'}
    
    retorno_total = director_movies['return'].sum()
    peliculas = []
    for _, row in director_movies.iterrows():
        peliculas.append({
            'titulo': row['title'],
            'fecha_lanzamiento': row['release_date'],
            'retorno_individual': row['return'],
            'costo': row['budget'],
            'ganancia': row['revenue']
        })
    
    return {
        'mensaje': f'El director {nombre_director} ha conseguido un retorno total de {retorno_total:.2f}.',
        'peliculas': peliculas
    }

# 7. Sistema de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    # Encontrar el índice de la película por título
    movie_index = movies_df[movies_df['title'].str.lower() == titulo.lower()].index
    if len(movie_index) == 0:
        return {"error": "Película no encontrada"}
    
    movie_index = movie_index[0]
    
    # Calcular similitud de coseno
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[movie_index]))
    
    # Ordenar las películas por similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_movies = sim_scores[1:6]  # Excluir la película misma y tomar las 5 más similares
    
    # Obtener los títulos de las películas recomendadas
    recommended_titles = [movies_df.iloc[i[0]]['title'] for i in top_movies]
    return {"recomendaciones": recommended_titles}