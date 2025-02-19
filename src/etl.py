import pandas as pd
import ast

def load_data():
    """
    Carga los datasets desde los archivos CSV.
    """
    movies_path = 'data/movies_dataset.csv'
    credits_path = 'data/credits.csv'

    # Cargar los datasets
    movies_df = pd.read_csv(movies_path, low_memory=False)
    credits_df = pd.read_csv(credits_path)

    return movies_df, credits_df

def transform_data(movies_df, credits_df):
    """
    Realiza las transformaciones necesarias en los datos.
    """
    # Asegúrate de que la columna 'id' tenga el mismo tipo en ambos DataFrames
    movies_df['id'] = movies_df['id'].astype(str)
    credits_df['id'] = credits_df['id'].astype(str)

    # Combinar los datasets usando la columna 'id'
    merged_data = pd.merge(movies_df, credits_df, on='id', how='left')

    # Función para evaluar campos anidados de forma segura
    def safe_eval(x):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return None

    # Desanidar belongs_to_collection
    merged_data['belongs_to_collection'] = merged_data['belongs_to_collection'].apply(
        lambda x: safe_eval(x).get('name', None) if safe_eval(x) and isinstance(safe_eval(x), dict) else None
    )

    # Desanidar genres
    merged_data['genres'] = merged_data['genres'].apply(
        lambda x: [genre['name'] for genre in safe_eval(x)] if safe_eval(x) and isinstance(safe_eval(x), list) else []
    )

    # Desanidar production_companies
    merged_data['production_companies'] = merged_data['production_companies'].apply(
        lambda x: [company['name'] for company in safe_eval(x)] if safe_eval(x) and isinstance(safe_eval(x), list) else []
    )

    # Desanidar production_countries
    merged_data['production_countries'] = merged_data['production_countries'].apply(
        lambda x: [country['name'] for country in safe_eval(x)] if safe_eval(x) and isinstance(safe_eval(x), list) else []
    )

    # Desanidar spoken_languages
    merged_data['spoken_languages'] = merged_data['spoken_languages'].apply(
        lambda x: [lang['name'] for lang in safe_eval(x)] if safe_eval(x) and isinstance(safe_eval(x), list) else []
    )

    # Manejo de valores nulos
    merged_data['revenue'] = pd.to_numeric(merged_data['revenue'], errors='coerce').fillna(0)
    merged_data['budget'] = pd.to_numeric(merged_data['budget'], errors='coerce').fillna(0)

    # Eliminar filas con valores nulos en release_date
    merged_data = merged_data.dropna(subset=['release_date'])

    # Formatear fechas y crear columna release_year
    merged_data['release_date'] = pd.to_datetime(merged_data['release_date'], format='%Y-%m-%d', errors='coerce')
    merged_data['release_year'] = merged_data['release_date'].dt.year

    # Crear columna return
    merged_data['return'] = merged_data.apply(
        lambda row: row['revenue'] / row['budget'] if row['budget'] > 0 else 0, axis=1
    )

    # Eliminar columnas innecesarias
    columns_to_drop = ['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']
    merged_data = merged_data.drop(columns=columns_to_drop)

    return merged_data

def save_data(transformed_data):
    """
    Guarda el dataset procesado en un archivo CSV.
    """
    transformed_data.to_csv('data/movies_processed.csv', index=False)

if __name__ == '__main__':
    # Cargar datos
    movies_df, credits_df = load_data()

    # Transformar datos
    transformed_data = transform_data(movies_df, credits_df)

    # Guardar datos procesados
    save_data(transformed_data)

    print("Transformaciones completadas. Datos guardados en 'data/movies_processed.csv'.")