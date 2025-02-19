import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    return movies, credits

def visualize_movie_distribution(movies):
    print("Columnas del DataFrame de películas:", movies.columns)
    if 'genre' not in movies.columns:
        print("Error: La columna 'genre' no se encuentra en el DataFrame de películas.")
        return
    plt.figure(figsize=(10, 6))
    sns.countplot(data=movies, x='genre', order=movies['genre'].value_counts().index)
    plt.title('Distribution of Movies by Genre')
    plt.xticks(rotation=45)
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.show()

def generate_statistics(movies):
    stats = {
        'total_movies': movies.shape[0],
        'average_rating': movies['rating'].mean() if 'rating' in movies.columns else 'N/A',
        'most_common_genre': movies['genre'].mode()[0] if 'genre' in movies.columns else 'N/A'
    }
    return stats

def main():
    movies, credits = load_data('../data/movies_dataset.csv', '../data/credits.csv')
    visualize_movie_distribution(movies)
    stats = generate_statistics(movies)
    print(stats)

if __name__ == "__main__":
    main()