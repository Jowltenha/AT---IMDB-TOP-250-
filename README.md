# 🎬 Projeto IMDb Top 250 Analyzer

## Descrição do Projeto

Este projeto em Python realiza um fluxo completo de **Web Scraping**, **Persistência de Dados** e **Análise de Dados**. O objetivo é extrair informações dos 250 filmes mais bem avaliados do IMDb, salvar esses dados em um banco SQLite (usando SQLAlchemy) e, finalmente, processar e exportar os resultados usando a biblioteca Pandas.

**Funcionalidades principais:**
1.  **Scraping:** Extração de Título, Ano e Nota do IMDb.
2.  **POO/ORM:** Mapeamento de objetos para tabelas de banco de dados.
3.  **Persistência:** Salvamento dos dados em `imdb.db`.
4.  **Análise:** Classificação de notas ("Obra-prima", "Excelente") e criação de resumos por categoria e ano.
5.  **Exportação:** Geração dos arquivos `.csv` e `.json` para análise externa.

## 🛠️ Como Instalar e Executar

### Pré-requisitos

Você precisa ter o Python 3.x instalado.

### 1. Instalação das Dependências

Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas listadas no `requirements.txt`:

```bash

Lista as dependências que precisam ser instaladas.

requests # (Opcional, se você for trocar urllib por requests)
urllib3 # (Módulo usado no scraping, mas geralmente incluso no ambiente)
beautifulsoup4
pandas
SQLAlchemy
