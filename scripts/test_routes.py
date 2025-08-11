#!/usr/bin/env python3
"""
Script para testar todas as rotas da API Book Search.
Executa testes para todas as rotas disponíveis e exibe os resultados.
"""

import requests
import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from colorama import init, Fore, Style

# Inicializar colorama para cores no terminal
init(autoreset=True)

# Configuração da API
BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api/v1"

@dataclass
class TestResult:
    """Classe para armazenar resultados dos testes."""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error_message: str = ""
    response_data: Any = None

class APITester:
    """Classe para testar todas as rotas da API."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.session = requests.Session()
        self.access_token = None
        self.test_results: List[TestResult] = []
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> TestResult:
        """Faz uma requisição e retorna o resultado do teste."""
        url = f"{self.api_base}{endpoint}"
        
        # Adicionar token de autenticação se disponível
        if self.access_token:
            headers = kwargs.get('headers', {})
            headers['Authorization'] = f"Bearer {self.access_token}"
            kwargs['headers'] = headers
        
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, **kwargs)
            response_time = time.time() - start_time
            
            success = 200 <= response.status_code < 300
            error_message = ""
            
            if not success:
                try:
                    error_data = response.json()
                    error_message = error_data.get('detail', 'Erro desconhecido')
                except:
                    error_message = response.text
            
            return TestResult(
                endpoint=endpoint,
                method=method,
                status_code=response.status_code,
                response_time=response_time,
                success=success,
                error_message=error_message,
                response_data=response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            )
            
        except requests.exceptions.RequestException as e:
            return TestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    def test_root_endpoint(self) -> TestResult:
        """Testa o endpoint raiz."""
        print(f"{Fore.CYAN}🔍 Testando endpoint raiz...")
        # Testar o endpoint raiz correto da API (sem prefixo /api/v1)
        url = f"{self.base_url}/"
        start_time = time.time()
        
        try:
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            success = 200 <= response.status_code < 300
            error_message = ""
            
            if not success:
                try:
                    error_data = response.json()
                    error_message = error_data.get('detail', 'Erro desconhecido')
                except:
                    error_message = response.text
            
            return TestResult(
                endpoint="/",
                method="GET",
                status_code=response.status_code,
                response_time=response_time,
                success=success,
                error_message=error_message,
                response_data=response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            )
            
        except requests.exceptions.RequestException as e:
            return TestResult(
                endpoint="/",
                method="GET",
                status_code=0,
                response_time=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    def test_health_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de health."""
        print(f"{Fore.CYAN}🏥 Testando endpoints de health...")
        results = []
        
        # Health check
        results.append(self._make_request("GET", "/health"))
        
        return results
    
    def test_auth_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de autenticação."""
        print(f"{Fore.CYAN}🔐 Testando endpoints de autenticação...")
        results = []
        
        # Login com credenciais corretas
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        login_result = self._make_request(
            "POST", 
            "/auth/login", 
            data=login_data
        )
        results.append(login_result)
        
        # Extrair token se login foi bem-sucedido
        if login_result.success and login_result.response_data:
            self.access_token = login_result.response_data.get('access_token')
            print(f"{Fore.GREEN}✅ Token obtido com sucesso")
        
        # Login com credenciais incorretas (teste de segurança - esperado falhar)
        wrong_login_data = {
            "username": "wrong",
            "password": "wrong"
        }
        wrong_login_result = self._make_request(
            "POST", 
            "/auth/login", 
            data=wrong_login_data
        )
        # Marcar como sucesso se retornou 401 (comportamento esperado)
        if wrong_login_result.status_code == 401:
            wrong_login_result.success = True
            wrong_login_result.error_message = ""
        results.append(wrong_login_result)
        
        # Refresh token (se temos token válido)
        if self.access_token:
            results.append(self._make_request("POST", "/auth/refresh"))
        
        return results
    
    def test_books_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de livros."""
        print(f"{Fore.CYAN}📚 Testando endpoints de livros...")
        results = []
        
        # Listar todos os livros
        results.append(self._make_request("GET", "/books"))
        
        # Livros mais bem avaliados
        results.append(self._make_request("GET", "/books/top-rated"))
        
        # Busca por título
        results.append(self._make_request("GET", "/books/search?title=Senhor"))
        
        # Busca por categoria
        results.append(self._make_request("GET", "/books/search?category=Fantasia"))
        
        # Busca por título e categoria
        results.append(self._make_request("GET", "/books/search?title=Anéis&category=Fantasia"))
        
        # Filtro por preço mínimo
        results.append(self._make_request("GET", "/books/filter-by-price?min_price=25"))
        
        # Filtro por preço máximo
        results.append(self._make_request("GET", "/books/filter-by-price?max_price=30"))
        
        # Filtro por faixa de preço
        results.append(self._make_request("GET", "/books/filter-by-price?min_price=20&max_price=35"))
        
        # Buscar livros por UUIDs válidos
        books_response = self._make_request("GET", "/books")
        if books_response.success and books_response.response_data:
            books = books_response.response_data
            if len(books) >= 3:
                # Usar os primeiros 3 UUIDs válidos
                valid_uuids = [books[0]['id'], books[1]['id'], books[2]['id']]
                for uuid in valid_uuids:
                    results.append(self._make_request("GET", f"/books/{uuid}"))
            else:
                # Fallback se não há livros suficientes
                results.append(self._make_request("GET", "/books/1"))
        else:
            results.append(self._make_request("GET", "/books/1"))
        
        # Buscar livro por UUID inexistente
        non_existent_result = self._make_request("GET", "/books/99999999-9999-9999-9999-999999999999")
        # Marcar como sucesso se retornou 404 (comportamento esperado)
        if non_existent_result.status_code == 404:
            non_existent_result.success = True
            non_existent_result.error_message = ""
        results.append(non_existent_result)
        
        return results
    
    def test_categories_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de categorias."""
        print(f"{Fore.CYAN}📂 Testando endpoints de categorias...")
        results = []
        
        # Listar todas as categorias
        results.append(self._make_request("GET", "/categories"))
        
        return results
    
    def test_stats_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de estatísticas."""
        print(f"{Fore.CYAN}📊 Testando endpoints de estatísticas...")
        results = []
        
        # Estatísticas gerais
        results.append(self._make_request("GET", "/stats/overview"))
        
        # Estatísticas por categoria
        results.append(self._make_request("GET", "/stats/categories"))
        
        return results
    
    def test_scraping_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de scraping."""
        print(f"{Fore.CYAN}🕷️ Testando endpoints de scraping...")
        results = []
        
        # Trigger scraping (requer autenticação)
        if self.access_token:
            results.append(self._make_request("POST", "/scraping/trigger"))
        else:
            # Teste sem autenticação (deve falhar)
            results.append(self._make_request("POST", "/scraping/trigger"))
        
        return results
    
    def test_analytics_endpoints(self) -> List[TestResult]:
        """Testa os endpoints de analytics."""
        print(f"{Fore.CYAN}📈 Testando endpoints de analytics...")
        results = []
        
        # Métricas gerais da API
        results.append(self._make_request("GET", "/analytics/metrics"))
        
        # Estatísticas de predições ML
        results.append(self._make_request("GET", "/analytics/ml-predictions"))
        
        # Métricas detalhadas de performance
        results.append(self._make_request("GET", "/analytics/performance"))
        
        return results
    
    def run_all_tests(self) -> List[TestResult]:
        """Executa todos os testes."""
        print(f"{Fore.YELLOW}🚀 Iniciando testes da API Book Search...")
        print(f"{Fore.YELLOW}📍 URL Base: {self.base_url}")
        print(f"{Fore.YELLOW}⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        all_results = []
        
        # Testar endpoint raiz
        all_results.append(self.test_root_endpoint())
        
        # Testar endpoints de health
        all_results.extend(self.test_health_endpoints())
        
        # Testar endpoints de autenticação
        all_results.extend(self.test_auth_endpoints())
        
        # Testar endpoints de livros
        all_results.extend(self.test_books_endpoints())
        
        # Testar endpoints de categorias
        all_results.extend(self.test_categories_endpoints())
        
        # Testar endpoints de estatísticas
        all_results.extend(self.test_stats_endpoints())
        
        # Testar endpoints de analytics
        all_results.extend(self.test_analytics_endpoints())
        
        # Testar endpoints de scraping (comentado para evitar demora)
        # all_results.extend(self.test_scraping_endpoints())
        
        self.test_results = all_results
        return all_results
    
    def print_results(self):
        """Exibe os resultados dos testes de forma organizada."""
        print(f"\n{Fore.YELLOW}📋 RESULTADOS DOS TESTES")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - successful_tests
        
        print(f"{Fore.CYAN}📊 Estatísticas Gerais:")
        print(f"   Total de testes: {total_tests}")
        print(f"   ✅ Sucessos: {successful_tests}")
        print(f"   ❌ Falhas: {failed_tests}")
        print(f"   📈 Taxa de sucesso: {(successful_tests/total_tests)*100:.1f}%")
        
        print(f"\n{Fore.CYAN}📝 Detalhes dos Testes:")
        print("-" * 80)
        
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result.success else "❌"
            status_color = Fore.GREEN if result.success else Fore.RED
            method_color = Fore.BLUE
            
            print(f"{i:2d}. {status_icon} {status_color}{result.method:6s}{Style.RESET_ALL} "
                  f"{result.endpoint}")
            print(f"    Status: {status_color}{result.status_code}{Style.RESET_ALL} | "
                  f"Tempo: {result.response_time:.3f}s")
            
            if not result.success and result.error_message:
                print(f"    Erro: {Fore.RED}{result.error_message}{Style.RESET_ALL}")
            
            # Mostrar dados da resposta para alguns endpoints importantes
            if result.success and result.response_data:
                if "books" in result.endpoint and isinstance(result.response_data, list):
                    print(f"    📚 Livros retornados: {len(result.response_data)}")
                elif "categories" in result.endpoint and isinstance(result.response_data, list):
                    print(f"    📂 Categorias: {result.response_data}")
                elif "stats" in result.endpoint and isinstance(result.response_data, dict):
                    print(f"    📊 Dados: {result.response_data}")
            
            print()
        
        # Resumo final
        print(f"{Fore.YELLOW}🎯 RESUMO FINAL")
        print("=" * 80)
        if failed_tests == 0:
            print(f"{Fore.GREEN}🎉 Todos os testes passaram! A API está funcionando perfeitamente.")
        else:
            print(f"{Fore.RED}⚠️  {failed_tests} teste(s) falharam. Verifique os detalhes acima.")
        
        print(f"{Fore.CYAN}💡 Dica: Execute 'uvicorn api.main:app --reload' para iniciar a API localmente")

def main():
    """Função principal do script."""
    try:
        tester = APITester()
        tester.run_all_tests()
        tester.print_results()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️  Testes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\n{Fore.RED}💥 Erro durante a execução dos testes: {e}")

if __name__ == "__main__":
    main() 