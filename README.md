
### 🔁 Pipeline de Dados

1. **Ingestão**: Scraping de todos os livros da plataforma.
2. **Transformação**: Dados estruturados e salvos em CSV.
3. **API REST**: FastAPI carrega os dados e expõe os endpoints.
4. **Consumo**: Cientistas de dados e sistemas podem acessar os dados pela API.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- FastAPI
- Uvicorn
- BeautifulSoup4
- Pandas
- Pydantic
- Swagger UI (auto gerado pelo FastAPI)
- (opcional) Streamlit para dashboard
- (opcional) JWT para autenticação

---

## 📥 Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/Gnoario/book-search.git
cd book-api

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o scraping (gera books.csv)
python scripts/scrape_books.py OU uvicorn api.main:app --relod - Executar api de scrapping

# Rode a API localmente
uvicorn api.main:app --reload
