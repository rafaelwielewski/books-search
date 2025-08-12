# Book Search API

API para busca e consulta de livros com recursos de Machine Learning e monitoramento.

## 🚀 Funcionalidades

### Core API
- **Livros**: Consulta, busca e filtros por preço, categoria e avaliação
- **Categorias**: Listagem de categorias disponíveis
- **Estatísticas**: Métricas gerais e por categoria
- **Health Check**: Monitoramento de saúde da API

### 🤖 Pipeline ML-Ready
- **Features**: Dados formatados para extração de features (`/api/v1/ml/features`)
- **Training Data**: Dataset para treinamento de modelos (`/api/v1/ml/training-data`)
- **Predictions**: Endpoint para receber predições de modelos ML (`/api/v1/ml/predictions`)
- **Model Info**: Informações sobre modelos disponíveis (`/api/v1/ml/model-info`)

### 📊 Monitoramento & Analytics
- **Logs Estruturados**: Todas as chamadas são logadas com métricas de performance
- **Métricas de Performance**: Tempo de resposta, taxa de erro, distribuição de requests
- **Dashboard Streamlit**: Interface visual para monitoramento em tempo real
- **Analytics Endpoints**: Métricas detalhadas via API (`/api/v1/analytics/*`)

## 🛠️ Instalação

### Pré-requisitos
- Python 3.12+
- Poetry

### Setup Inicial
```bash
# Clone o repositório
git clone <repository-url>
cd book-search

# Instalação com Poetry
make setup
# ou
./setup.sh
```

## 🚀 Execução

### API
```bash
# Desenvolvimento (com reload automático)
make dev

# Produção
make run

# Ou diretamente com Poetry
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Dashboard
```bash
# Executar dashboard
make dashboard

# Ou diretamente
poetry run streamlit run dashboard.py --server.port 8501
```

### API + Dashboard Simultaneamente
```bash
make start-all
```

## 📚 Endpoints

### Core API
- `GET /api/v1/books` - Listar todos os livros
- `GET /api/v1/books/{id}` - Buscar livro por ID
- `GET /api/v1/books/search` - Buscar por título ou categoria
- `GET /api/v1/books/price-range` - Filtrar por faixa de preço
- `GET /api/v1/books/top-rated` - Livros mais bem avaliados
- `GET /api/v1/categories` - Listar categorias
- `GET /api/v1/stats/overview` - Estatísticas gerais
- `GET /api/v1/stats/categories` - Estatísticas por categoria
- `GET /api/v1/health` - Status da API

### ML Endpoints
- `GET /api/v1/ml/features` - Dados formatados para features ML
- `GET /api/v1/ml/training-data` - Dataset para treinamento
- `POST /api/v1/ml/predictions` - Receber predições de modelos
- `GET /api/v1/ml/model-info` - Informações dos modelos

### Analytics Endpoints
- `GET /api/v1/analytics/metrics` - Métricas gerais da API
- `GET /api/v1/analytics/ml-predictions` - Estatísticas de predições ML
- `GET /api/v1/analytics/performance` - Métricas detalhadas de performance

## 📊 Dashboard

O dashboard Streamlit oferece:

### 📈 Overview
- Métricas gerais da API
- Status de saúde
- Atividade recente

### 📊 API Metrics
- Total de requests
- Tempo médio de resposta
- Taxa de erro
- Distribuição por endpoint e método HTTP

### 🤖 ML Analytics
- Estatísticas de predições ML
- Confiança média dos modelos
- Predições por livro
- Informações dos modelos

### ⚡ Performance
- Distribuição de tempo de resposta
- Performance por endpoint
- Breakdown de erros
- Saúde do sistema

### 📝 Real-time Logs
- Visualização de logs em tempo real
- Estatísticas de logs
- Filtros por tipo de evento

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
book-search/
├── api/
│   ├── domain/
│   │   ├── models/          # Modelos de dados
│   │   └── usecases/        # Casos de uso
│   ├── infra/
│   │   └── repository/      # Repositórios
│   ├── presentation/
│   │   ├── middlewares/     # Middlewares (logs, performance)
│   │   └── routes/          # Rotas da API
│   |── utils/               # Utilitários (logger)
│   |── main.py              # Arquivo principal da API
│   └── dashboard.py         # Dashboard Streamlit
├── data/                    # Dados CSV
├── logs/                    # Logs estruturados
└── pyproject.toml          # Dependências Poetry
```

### Comandos Úteis
```bash
# Instalar dependências
poetry install

# Executar testes
make test

# Pre-commit hooks
make pre-commit

# Executar API
make dev

# Executar dashboard
make dashboard

# Executar ambos
make start-all
```

## 📈 Monitoramento

### Logs Estruturados
Todos os requests são logados com:
- Timestamp
- Request ID
- Método HTTP
- URL
- Status code
- Tempo de resposta
- IP do cliente
- User Agent

### Métricas Capturadas
- **Performance**: Tempo de resposta, throughput
- **Erros**: Tipos de erro, taxa de erro
- **Uso**: Requests por endpoint, método HTTP
- **ML**: Predições, confiança, modelos

### Headers de Performance
- `X-Response-Time`: Tempo de resposta em ms
- `X-Request-ID`: ID único do request

## 🤖 Machine Learning

### Features Disponíveis
- Comprimento do título
- Categoria codificada
- Preço normalizado
- Avaliação normalizada
- Indicador de desconto
- Categorias de preço e avaliação

### Target Variables
- `is_popular`: Livro popular (rating >= 4.0)
- `is_expensive`: Livro caro (preço >= 70)
- `recommendation_score`: Score de recomendação

### Modelos Disponíveis
- **book_recommendation_model**: Modelo de recomendação
- **price_prediction_model**: Modelo de predição de preço

## 🔍 Exemplos de Uso

### Buscar livros por categoria
```bash
curl "http://localhost:8080/api/v1/books/search?category=ficção"
```

### Obter features para ML
```bash
curl "http://localhost:8080/api/v1/ml/features"
```

### Enviar predição ML
```bash
curl -X POST "http://localhost:8080/api/v1/ml/predictions" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "book_123",
    "features": {
      "prediction": 0.85,
      "confidence": 0.92
    }
  }'
```

### Ver métricas da API
```bash
curl "http://localhost:8080/api/v1/analytics/metrics"
```

## 📝 Logs

Os logs são salvos em `logs/api.log` com formato estruturado:
- `API_CALL`: Requests bem-sucedidos
- `API_ERROR`: Erros da API
- `ML_PREDICTION`: Predições de modelos ML
- `PERFORMANCE_METRIC`: Métricas de performance

## 🚀 Deploy

### Local
```bash
make run
```

### Docker
```bash
make dev-docker
```

## 📚 Documentação

- **API Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Dashboard**: http://localhost:8501

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
