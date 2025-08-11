#!/usr/bin/env python3
"""
Test script for new ML and Analytics features.
Run this script to verify that all new endpoints are working.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
API_BASE_URL = "http://localhost:8080"

def test_ml_endpoints():
    """Test ML endpoints."""
    print("🤖 Testing ML Endpoints...")
    
    # Test features endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/ml/features")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Features endpoint: {data.get('total_records', 0)} records")
        else:
            print(f"❌ Features endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Features endpoint error: {e}")
    
    # Test training data endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/ml/training-data")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Training data endpoint: {data.get('total_samples', 0)} samples")
        else:
            print(f"❌ Training data endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Training data endpoint error: {e}")
    
    # Test model info endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/ml/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info endpoint: {data.get('total_models', 0)} models")
        else:
            print(f"❌ Model info endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model info endpoint error: {e}")
    
    # Test predictions endpoint
    try:
        prediction_data = {
            "book_id": "test_book_123",
            "features": {
                "prediction": 0.85,
                "confidence": 0.92
            }
        }
        response = requests.post(
            f"{API_BASE_URL}/api/v1/ml/predictions",
            json=prediction_data
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Predictions endpoint: prediction {data.get('prediction', 0)}")
        else:
            print(f"❌ Predictions endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Predictions endpoint error: {e}")

def test_analytics_endpoints():
    """Test Analytics endpoints."""
    print("\n📊 Testing Analytics Endpoints...")
    
    # Test metrics endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/analytics/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metrics endpoint: {data.get('total_requests', 0)} total requests")
        else:
            print(f"❌ Metrics endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Metrics endpoint error: {e}")
    
    # Test ML predictions analytics
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/analytics/ml-predictions")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ML predictions analytics: {data.get('total_predictions', 0)} predictions")
        else:
            print(f"❌ ML predictions analytics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ ML predictions analytics error: {e}")
    
    # Test performance endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/analytics/performance")
        if response.status_code == 200:
            data = response.json()
            health = data.get('system_health', {})
            print(f"✅ Performance endpoint: {health.get('uptime_percentage', 0)}% uptime")
        else:
            print(f"❌ Performance endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Performance endpoint error: {e}")

def test_core_endpoints():
    """Test core API endpoints to generate some activity."""
    print("\n🔧 Testing Core Endpoints (to generate activity)...")
    
    endpoints = [
        "/api/v1/books",
        "/api/v1/categories", 
        "/api/v1/stats/overview",
        "/api/v1/health/status"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def test_performance_headers():
    """Test that performance headers are being added."""
    print("\n⚡ Testing Performance Headers...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/books")
        if response.status_code == 200:
            response_time = response.headers.get('X-Response-Time')
            request_id = response.headers.get('X-Request-ID')
            
            if response_time:
                print(f"✅ X-Response-Time header: {response_time}")
            else:
                print("❌ X-Response-Time header missing")
            
            if request_id:
                print(f"✅ X-Request-ID header: {request_id}")
            else:
                print("❌ X-Request-ID header missing")
        else:
            print(f"❌ Failed to test headers: {response.status_code}")
    except Exception as e:
        print(f"❌ Header test error: {e}")

def main():
    """Run all tests."""
    print("🚀 Testing New Features")
    print("=" * 50)
    
    # Test core endpoints first to generate activity
    test_core_endpoints()
    
    # Wait a moment for logs to be written
    time.sleep(1)
    
    # Test new features
    test_ml_endpoints()
    test_analytics_endpoints()
    test_performance_headers()
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")
    print("\n📋 Next steps:")
    print("1. Check logs/api.log for structured logs")
    print("2. Visit http://localhost:8080/docs for API documentation")
    print("3. Run 'make dashboard' to start the monitoring dashboard")
    print("4. Visit http://localhost:8501 for the dashboard")

if __name__ == "__main__":
    main() 