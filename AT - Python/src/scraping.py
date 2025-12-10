# scraping.py

import urllib.request
from bs4 import BeautifulSoup
import time

def extrair_dados_imdb(url: str, n_filmes: int):
    """
    Realiza o scraping na URL do IMDb e retorna uma lista de dicionários
    com os dados de filmes, limitando o resultado a n_filmes.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("---Baixando html da pagina do IMDB---")
    time.sleep(1)

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resposta:
            conteudo_html = resposta.read().decode('utf-8')
    except Exception as e:
        print(f"ERRO BIZZARO: {e}")
        return []

    print("HTML baixado com sucesso. Extraindo os títulos...")

    soup = BeautifulSoup(conteudo_html, 'html.parser')
    filmes_geral_data = []

    listar_itens = soup.find_all('li', class_='ipc-metadata-list-summary-item')

    for item in listar_itens:
        if len(filmes_geral_data) >= n_filmes:
            break
            
        filme_data = {} 
        
        # TÍTULO
        IMDB_Titulos = item.find('h3', class_='ipc-title__text')
        if IMDB_Titulos:
            titulo_filmes_completo = IMDB_Titulos.get_text(strip=True)
            filme_data['titulo'] = titulo_filmes_completo

        # ANO
        IMDB_Anos = item.find('span', class_='sc-b4f120f6-7 hoOxkw cli-title-metadata-item')
        if IMDB_Anos:
            ano_filmes = IMDB_Anos.get_text(strip=True)
            if ano_filmes and len(ano_filmes) == 4 and ano_filmes.isdigit():
                filme_data['ano'] = ano_filmes
            else:
                filme_data['ano'] = 'XXXX'

        # NOTA
        IMDB_Nota = item.find('span', class_='ipc-rating-star--rating')
        if IMDB_Nota:
            nota_filme = IMDB_Nota.get_text(strip=True)
            filme_data['nota'] = nota_filme
        else:
            filme_data['nota'] = 'N/D'

        if 'titulo' in filme_data:
            filmes_geral_data.append(filme_data)

    return filmes_geral_data