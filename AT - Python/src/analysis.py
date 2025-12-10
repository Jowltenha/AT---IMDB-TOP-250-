# analysis.py

import pandas as pd

def classificar_nota(nota: float) -> str:
    """Classifica a nota (rating) em categorias textuais."""
    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return "Erro na Nota"

    if nota >= 9.0:
        return "Obra-prima"
    elif nota >= 8.0:
        return "Excelente"
    elif nota >= 7.0:
        return "Bom"
    else:
        return "Mediano"

def analisar_filmes(df_movies: pd.DataFrame):
    """Executa a análise de ordenação e filtro."""
    
    if df_movies.empty:
        print("DataFrame de filmes vazio para análise.")
        return
        
    df_movies.sort_values(by='rating', ascending=False, inplace=True)
    
    df_top_rated = df_movies[df_movies['rating'] > 9.0]
    
    print("\n--- Análise: Filmes com Nota > 9.0 ---")
    print(f"Total de filmes encontrados com nota > 9.0: {len(df_top_rated)}")
    
    if not df_top_rated.empty:
        print("\nTOP 5 Filmes (Nota > 9.0):")
        print(df_top_rated.head(5)[['title', 'rating']])
        
    return df_movies # Retorna o DF ordenado para a próxima etapa

def resumir_por_categoria(df_movies: pd.DataFrame):
    """Cria a coluna de categoria e o resumo por ano."""
    
    if df_movies.empty:
        print("DataFrame de filmes vazio para resumo.")
        return

    # Cria a coluna 'categoria'
    df_movies['categoria'] = df_movies['rating'].apply(classificar_nota)
    
    # Garante que 'year' seja int
    df_movies['year'] = pd.to_numeric(df_movies['year'], errors='coerce').fillna(0).astype(int)

    # Tabela Resumo
    resumo_df = df_movies.groupby(['categoria', 'year']).size().reset_index(name='Contagem')
    tabela_resumo = resumo_df.pivot_table(
        index='categoria', columns='year', values='Contagem', fill_value=0
    )
    
    ordem_categorias = ["Obra-prima", "Excelente", "Bom", "Mediano"]
    tabela_resumo = tabela_resumo.reindex(ordem_categorias, fill_value=0)

    print("\n--- Resumo: Filmes por Categoria e Ano ---")
    print(tabela_resumo)
    
    # Exibe os 10 primeiros filmes classificados
    print("\n--- Top 10 Filmes Classificados ---")
    print(df_movies[['title', 'rating', 'categoria']].head(10))

def exportar_dados(df_movies: pd.DataFrame, df_series: pd.DataFrame):
    """Exporta os DataFrames para CSV e JSON."""
    
    export_data = [(df_movies, 'movies'), (df_series, 'series')]

    for df, base_name in export_data:
        if df.empty:
            continue

        # --- Exportação para CSV ---
        csv_file = f"{base_name}.csv"
        try:
            df.to_csv(csv_file, index=False)
            print(f" Exportado com sucesso: {csv_file}")
        except Exception as e:
            print(f" ERRO ao salvar {csv_file}: {e}")

        # --- Exportação para JSON ---
        json_file = f"{base_name}.json"
        try:
            df.to_json(json_file, orient='records', lines=True, indent=4)
            print(f" Exportado com sucesso: {json_file}")
        except Exception as e:
            print(f" ERRO ao salvar {json_file}: {e}")