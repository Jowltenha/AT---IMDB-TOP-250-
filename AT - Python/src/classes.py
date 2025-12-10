# classes.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Define a classe base para mapeamento do SQLAlchemy
Base = declarative_base()

# --- Classes de POO ---

class TV:
    def __init__(self, titulo: str, ano: int):
        self.titulo = titulo
        self.ano = ano

    def __str__(self):
        return f"{self.titulo} ({self.ano})"

class Movie(TV):
    def __init__(self, titulo: str, ano: int, nota: float):
        super().__init__(titulo, ano)
        self.nota = nota

    def __str__(self):
        return f"{super().__str__()} – Nota: {self.nota}"
    
    def to_dict(self):
        return {
            "Tipo": "Movie",
            "titulo": self.titulo,
            "ano": self.ano,
            "nota": self.nota
        }

class Series(TV):
    def __init__(self, titulo: str, ano: int, temporadas: int, episodios: int):
        super().__init__(titulo, ano)
        self.temporadas = temporadas
        self.episodios = episodios

    def __str__(self):
        return f"{super().__str__()} – Temporadas: {self.temporadas}, Episódios: {self.episodios}"

    def to_dict(self):
        return {
            "Tipo": "Series",
            "titulo": self.titulo,
            "ano": self.ano,
            "temporadas": self.temporadas,
            "episodios": self.episodios
        }

# --- Classes de Modelo SQLAlchemy ---

class MovieModel(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    def __init__(self, title, year, rating):
        self.title = title
        self.year = year
        self.rating = rating

    def __repr__(self):
        return f"<Movie(title='{self.title}', year={self.year}, rating={self.rating})>"


class SeriesModel(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    seasons = Column(Integer, nullable=False)
    episodes = Column(Integer, nullable=False)

    def __init__(self, title, year, seasons, episodes):
        self.title = title
        self.year = year
        self.seasons = seasons
        self.episodes = episodes

    def __repr__(self):
        return f"<Series(title='{self.title}', seasons={self.seasons})>"