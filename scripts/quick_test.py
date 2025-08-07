#!/usr/bin/env python3
"""
Script rápido para testar as principais rotas da API.
Versão simplificada sem dependências externas.
"""

import requests
import time
from typing import Dict, List

# Configuração
BASE_URL = "http://localhost:8080"
API_BASE = f"{BASE_URL}/api/v1"

def test_endpoint(method: str, endpoint: str, **kwargs) -> Dict:
    """Testa um endpoint específico."""
    # Tratar endpoint raiz especial
    if endpoint == "":
        url = f"{BASE_URL}/"
    else:
        url = f"{API_BASE}{endpoint}"
    
    start_time = time.time()
    try:
        response = requests.request(method, url, **kwargs)
        response_time = time.time() - start_time
        
        # Tratar casos especiais onde 401 e 404 são comportamentos esperados
        success = 200 <= response.status_code < 300
        if endpoint == "/books/999/" and response.status_code == 404:
            success = True  # 404 é esperado para ID inexistente
        elif "wrong" in str(kwargs.get('data', '')) and response.status_code == 401:
            success = True  # 401 é esperado para credenciais inválidas
        
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response_time": response_time,
            "success": success,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": 0,
            "response_time": time.time() - start_time,
            "success": False,
            "error": str(e)
        }

def run_quick_tests():
    """Executa testes rápidos das principais rotas."""
    print("🚀 Testando API Book Search...")
    print(f"📍 URL: {BASE_URL}")
    print("-" * 50)
    
    # Primeiro, obter um ID válido para testar
    valid_id = None
    try:
        response = requests.get(f"{API_BASE}/books/")
        if response.status_code == 200:
            books = response.json()
            if books:
                valid_id = books[0]['id']
    except:
        pass
    
    tests = [
        # Endpoint raiz
        ("GET", ""),
        
        # Health
        ("GET", "/health/"),
        
        # Books
        ("GET", "/books/"),
        ("GET", "/books/top-rated/"),
        ("GET", "/books/search?title=Senhor"),
        ("GET", "/books/search?category=Fantasia"),
        ("GET", "/books/filter-by-price?min_price=25"),
    ]
    
    # Adicionar testes de ID se temos um ID válido
    if valid_id:
        tests.append(("GET", f"/books/{valid_id}/"))
    else:
        tests.append(("GET", "/books/1/"))  # Fallback
    
    tests.extend([
        ("GET", "/books/999/"),  # Deve falhar
        
        # Categories
        ("GET", "/categories/"),
        
        # Stats
        ("GET", "/stats/overview/"),
        ("GET", "/stats/categories/"),
        
        # Analytics
        ("GET", "/analytics/metrics/"),
        ("GET", "/analytics/ml-predictions/"),
        ("GET", "/analytics/performance/"),
    ])
    
    results = []
    for method, endpoint in tests:
        print(f"🔍 Testando {method} {endpoint}...")
        result = test_endpoint(method, endpoint)
        results.append(result)
        
        status = "✅" if result["success"] else "❌"
        print(f"   {status} {result['status_code']} ({result['response_time']:.3f}s)")
        
        if not result["success"] and "error" in result:
            print(f"   Erro: {result['error']}")
    
    # Resumo
    print("\n📊 RESUMO:")
    print("-" * 50)
    total = len(results)
    success = sum(1 for r in results if r["success"])
    print(f"Total: {total} | Sucessos: {success} | Falhas: {total - success}")
    
    if success == total:
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️  Alguns testes falharam.")

if __name__ == "__main__":
    run_quick_tests() 