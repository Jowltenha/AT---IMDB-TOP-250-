# main.py

import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import classes 
import scraping
import database
import analysis

# --- 0. Carregar Configuração ---

try:
    with open('config.json', 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
    print(f"Configurações carregadas do config.json.")
except FileNotFoundError:
    print("ERRO: Arquivo config.json não encontrado. Verifique o caminho.")
    exit()

IMDB_URL = CONFIG.get("IMDB_URL")
N_FILMES = CONFIG.get("N_FILMES", 250)
DATABASE_URL = CONFIG.get("DATABASE_URL")

# --- PRINCIPAL ---

def run_projeto():
    # ----------------------------------------------------
    # RASPAGEM E CRIAÇÃO DE OBJETOS (Exercícios 1-5)
    # ----------------------------------------------------
    
    print("\n\n--- INÍCIO DO FLUXO: RASPAGEM E OBJETOS ---")
    
    # 1. Scraping
    dados_filmes = scraping.extrair_dados_imdb(IMDB_URL, N_FILMES)
    
    # 2. Criação de Objetos e Catálogo (Exercício 5)
    catalogo = []
    
    # 2.1. Criação dos objetos Movie
    for dado in dados_filmes:
        try:
            nota_f = float(dado['nota'].replace(',', '.'))
            # O ano pode vir como string, garantimos a conversão segura para int
            ano_i = int(dado['ano']) if dado['ano'].isdigit() else 0 
            catalogo.append(classes.Movie(titulo=dado['titulo'], ano=ano_i, nota=nota_f))
        except (ValueError, KeyError, AttributeError):
            pass 
            
    # 2.2. Adição dos objetos Series fictícios
    series1 = classes.Series(titulo="The Witcher", ano=2019, temporadas=3, episodios=24)
    series2 = classes.Series(titulo="Arcane", ano=2021, temporadas=1, episodios=9)
    catalogo.append(series1)
    catalogo.append(series2)
    
    print(f"\n Total de Itens no Catálogo (Ex. 5): {len(catalogo)}")
    
    # 2.3. Exibir os itens (Correção para incluir as Séries)
    
    print("\n--- PRIMEIRAS 10 ENTRADAS (Filmes) ---")
    # Exibe os 10 primeiros (que são filmes)
    for item in catalogo[:10]:
        print(item)
    
    print("\n--- ÚLTIMAS 2 ENTRADAS (Séries) ---")
    # Exibe os 2 últimos (que são as séries).
    for item in catalogo[-2:]:
        print(item)
        
    print("\n---- Fim da Demonstração do Exercício 5 ----")
    
    # ----------------------------------------------------
    #  BANCO DE DADOS (Exercícios 6)
    # ----------------------------------------------------
    
    print("\n\n--- PERSISTÊNCIA NO BANCO DE DADOS (Ex. 6) ---")
    try:
        engine = database.setup_database(DATABASE_URL)
        print("Banco de dados 'imdb.db' e tabelas criadas/verificadas.")
        
        Session = sessionmaker(bind=engine)
        session = Session()

        database.inserir_filmes(session, dados_filmes)
        database.inserir_series(session)
        
        session.close()

    except SQLAlchemyError as e:
        print(f"ERRO FATAL ao configurar/inserir no DB: {e}")
        return

    # ----------------------------------------------------
    # ANÁLISE DE DADOS (Exercícios 7-10)
    # ----------------------------------------------------
    
    print("\n\n--- ANÁLISE DE DADOS (Ex. 7-10) ---")

    try:
        # Carrega DataFrames (Ex. 7)
        df_movies, df_series = database.load_dataframes(engine)
        print("\nDados lidos do 'imdb.db' com sucesso para DataFrames.")
        print("\n--- MOVIES DataFrame (Top 3) ---")
        print(df_movies.head(3))
        # Note: df_series não é impresso aqui, mas é carregado para exportação.

        # Análise (Ex. 8.1)
        df_movies = analysis.analisar_filmes(df_movies)

        # Classificação e Resumo (Ex. 9 & 10)
        analysis.resumir_por_categoria(df_movies)
        
        # Exportação (Ex. 8.2)
        print("\n--- FASE FINAL: EXPORTAÇÃO (Ex. 8.2) ---")
        analysis.exportar_dados(df_movies, df_series)

    except Exception as e:
        print(f"ERRO durante a Análise/Exportação: {e}")


run_projeto()