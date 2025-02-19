import pytest
import pandas as pd
from src.etl import load_data, transform_data, save_data

def test_load_data():
    # Test loading data from CSV files
    movies_df = load_data('data/movies_dataset.csv')
    credits_df = load_data('data/credits.csv')
    
    assert isinstance(movies_df, pd.DataFrame)
    assert isinstance(credits_df, pd.DataFrame)
    assert not movies_df.empty
    assert not credits_df.empty

def test_transform_data():
    # Test transformation of data
    movies_df = load_data('data/movies_dataset.csv')
    transformed_df = transform_data(movies_df)
    
    # Add assertions based on expected transformations
    assert 'title' in transformed_df.columns
    assert 'genre' in transformed_df.columns
    assert transformed_df['title'].notnull().all()

def test_save_data(tmp_path):
    # Test saving transformed data
    movies_df = load_data('data/movies_dataset.csv')
    transformed_df = transform_data(movies_df)
    
    output_file = tmp_path / "transformed_movies.csv"
    save_data(transformed_df, output_file)
    
    saved_df = pd.read_csv(output_file)
    assert not saved_df.empty
    assert 'title' in saved_df.columns
    assert 'genre' in saved_df.columns