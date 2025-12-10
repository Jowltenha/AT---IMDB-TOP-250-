# database.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from classes import Base, MovieModel, SeriesModel

def setup_database(db_url: str):
    """Cria a engine e as tabelas no banco de dados."""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

def inserir_filmes(session, dados_filmes: list):
    """Insere objetos MovieModel no banco de dados."""
    filmes_inseridos = 0
    for dado in dados_filmes:
        try:
            ano = int(dado['ano'])
            # Correção da nota para ponto decimal
            nota_corrigida = dado['nota'].replace(',', '.')
            rating = float(nota_corrigida)
        except ValueError:
            continue
        
        novo_filme = MovieModel(title=dado['titulo'], year=ano, rating=rating)
        
        try:
            session.add(novo_filme)
            session.commit()
            filmes_inseridos += 1
        except IntegrityError:
            session.rollback()
            
    print(f"\n{filmes_inseridos} filmes únicos inseridos/atualizados na tabela 'movies'.")
    return filmes_inseridos

def inserir_series(session):
    """Insere objetos SeriesModel fictícios no banco de dados."""
    series_data = [
        {"titulo": "The Witcher", "ano": 2019, "seasons": 3, "episodes": 24},
        {"titulo": "Arcane", "ano": 2021, "seasons": 1, "episodes": 9}
    ]
    series_inseridas = 0

    for data in series_data:
        nova_serie = SeriesModel(
            title=data['titulo'], 
            year=data['ano'], 
            seasons=data['seasons'], 
            episodes=data['episodes']
        )
        try:
            session.add(nova_serie)
            session.commit()
            series_inseridas += 1
        except IntegrityError:
            session.rollback()

    print(f"{series_inseridas} séries únicas inseridas/atualizadas na tabela 'series'.")
    return series_inseridas

def load_dataframes(engine):
    """Carrega dados das tabelas para DataFrames."""
    df_movies = pd.read_sql("SELECT * FROM movies", engine)
    df_series = pd.read_sql("SELECT * FROM series", engine)
    return df_movies, df_series
