import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Book API Dashboard",
    page_icon="📊",
    layout="wide"
)

# API base URL
API_BASE_URL = "http://localhost:8080"

def fetch_api_data(endpoint):
    """Fetch data from API endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data from {endpoint}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def main():
    st.title("📊 Book API Dashboard")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "API Metrics", "ML Analytics", "Performance", "Real-time Logs"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "API Metrics":
        show_api_metrics()
    elif page == "ML Analytics":
        show_ml_analytics()
    elif page == "Performance":
        show_performance()
    elif page == "Real-time Logs":
        show_realtime_logs()

def show_overview():
    st.header("📈 API Overview")
    
    # Fetch basic stats
    stats_data = fetch_api_data("/api/v1/stats/overview")
    health_data = fetch_api_data("/api/v1/health")
    
    # Create metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    if stats_data:
        with col1:
            st.metric("Total Books", stats_data.get("total_books", 0))
        
        with col2:
            st.metric("Average Price", f"R$ {stats_data.get('average_price', 0):.2f}")
        
        with col3:
            st.metric("Average Rating", f"{stats_data.get('average_rating', 0):.1f}/5.0")
    
    if health_data:
        with col4:
            status = health_data.get("status", "unknown")
            status_color = "🟢" if status == "healthy" else "🔴"
            st.metric("API Status", f"{status_color} {status}")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    analytics_data = fetch_api_data("/api/v1/analytics/metrics")
    
    if analytics_data and analytics_data.get("recent_activity"):
        recent_df = pd.DataFrame(analytics_data["recent_activity"])
        if not recent_df.empty:
            recent_df["timestamp"] = pd.to_datetime(recent_df["timestamp"])
            st.dataframe(recent_df[["timestamp", "method", "path", "status_code", "duration_ms"]])
        else:
            st.info("No recent activity data available.")
    else:
        st.info("No recent activity data available.")

def show_api_metrics():
    st.header("📊 API Metrics")
    
    analytics_data = fetch_api_data("/api/v1/analytics/metrics")
    
    if analytics_data:
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Requests", analytics_data.get("total_requests", 0))
        
        with col2:
            st.metric("Average Response Time", f"{analytics_data.get('average_response_time', 0):.2f}ms")
        
        with col3:
            st.metric("Error Rate", f"{analytics_data.get('error_rate', 0):.2f}%")
        
        # Requests by endpoint
        if analytics_data.get("requests_by_endpoint"):
            st.subheader("📈 Requests by Endpoint")
            endpoint_data = analytics_data["requests_by_endpoint"]
            fig = px.bar(
                x=list(endpoint_data.keys()),
                y=list(endpoint_data.values()),
                title="Request Count by Endpoint"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Requests by method
        if analytics_data.get("requests_by_method"):
            st.subheader("🔧 Requests by HTTP Method")
            method_data = analytics_data["requests_by_method"]
            fig = px.pie(
                values=list(method_data.values()),
                names=list(method_data.keys()),
                title="Request Distribution by Method"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top endpoints
        if analytics_data.get("top_endpoints"):
            st.subheader("🏆 Top Endpoints")
            top_df = pd.DataFrame(analytics_data["top_endpoints"])
            fig = px.bar(
                top_df,
                x="endpoint",
                y="count",
                title="Top 5 Most Used Endpoints"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Unable to fetch API metrics data.")

def show_ml_analytics():
    st.header("🤖 ML Analytics")
    
    # ML predictions
    ml_data = fetch_api_data("/api/v1/analytics/ml-predictions")
    
    if ml_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Predictions", ml_data.get("total_predictions", 0))
        
        with col2:
            st.metric("Average Confidence", f"{ml_data.get('average_confidence', 0):.2f}")
        
        with col3:
            predictions_by_book = ml_data.get("predictions_by_book", {})
            st.metric("Books with Predictions", len(predictions_by_book))
        
        # Recent predictions
        if ml_data.get("recent_predictions"):
            st.subheader("🕒 Recent ML Predictions")
            recent_preds = pd.DataFrame(ml_data["recent_predictions"])
            if not recent_preds.empty:
                recent_preds["timestamp"] = pd.to_datetime(recent_preds["timestamp"])
                st.dataframe(recent_preds)
        
        # Predictions by book
        if ml_data.get("predictions_by_book"):
            st.subheader("📚 Predictions by Book")
            book_preds = []
            for book_id, data in ml_data["predictions_by_book"].items():
                book_preds.append({
                    "book_id": book_id,
                    "count": data["count"],
                    "avg_prediction": data["average_prediction"],
                    "avg_confidence": data["average_confidence"]
                })
            
            if book_preds:
                book_df = pd.DataFrame(book_preds)
                fig = px.scatter(
                    book_df,
                    x="avg_prediction",
                    y="avg_confidence",
                    size="count",
                    title="Prediction vs Confidence by Book"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # ML model info
    st.subheader("🤖 ML Models")
    model_info = fetch_api_data("/api/v1/ml/model-info")
    
    if model_info and model_info.get("models"):
        models_df = pd.DataFrame(model_info["models"])
        st.dataframe(models_df)
    else:
        st.info("No ML model information available.")

def show_performance():
    st.header("⚡ Performance Metrics")
    
    performance_data = fetch_api_data("/api/v1/analytics/performance")
    
    if performance_data:
        # System health
        if performance_data.get("system_health"):
            st.subheader("🏥 System Health")
            health = performance_data["system_health"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Uptime", f"{health.get('uptime_percentage', 0):.1f}%")
            
            with col2:
                st.metric("Total Requests", health.get("total_requests", 0))
            
            with col3:
                st.metric("Error Count", health.get("error_count", 0))
            
            with col4:
                st.metric("Success Rate", f"{health.get('success_rate', 0):.1f}%")
        
        # Response time distribution
        if performance_data.get("response_time_distribution"):
            st.subheader("⏱️ Response Time Distribution")
            rt_dist = performance_data["response_time_distribution"]
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Min", f"{rt_dist.get('min', 0):.2f}ms")
            
            with col2:
                st.metric("Max", f"{rt_dist.get('max', 0):.2f}ms")
            
            with col3:
                st.metric("Median", f"{rt_dist.get('median', 0):.2f}ms")
            
            with col4:
                st.metric("P95", f"{rt_dist.get('p95', 0):.2f}ms")
            
            with col5:
                st.metric("P99", f"{rt_dist.get('p99', 0):.2f}ms")
        
        # Endpoint performance
        if performance_data.get("endpoint_performance"):
            st.subheader("🎯 Endpoint Performance")
            endpoint_perf = performance_data["endpoint_performance"]
            
            perf_data = []
            for endpoint, data in endpoint_perf.items():
                perf_data.append({
                    "endpoint": endpoint,
                    "avg_response_time": data["avg_response_time"],
                    "request_count": data["request_count"],
                    "min_response_time": data["min_response_time"],
                    "max_response_time": data["max_response_time"]
                })
            
            if perf_data:
                perf_df = pd.DataFrame(perf_data)
                fig = px.bar(
                    perf_df,
                    x="endpoint",
                    y="avg_response_time",
                    title="Average Response Time by Endpoint"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Error breakdown
        if performance_data.get("error_breakdown"):
            st.subheader("❌ Error Breakdown")
            error_data = performance_data["error_breakdown"]
            
            if error_data:
                fig = px.pie(
                    values=list(error_data.values()),
                    names=list(error_data.keys()),
                    title="Error Distribution by Type"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Unable to fetch performance data.")

def show_realtime_logs():
    st.header("📝 Real-time Logs")
    
    # Log file viewer
    log_file = "logs/api.log"
    
    if os.path.exists(log_file):
        st.subheader("📄 Recent Log Entries")
        
        # Read last 50 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        if lines:
            # Show last 50 lines
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            
            # Create a text area for logs
            log_content = "".join(recent_lines)
            st.text_area("Recent Logs", log_content, height=400)
            
            # Auto-refresh
            if st.button("🔄 Refresh Logs"):
                st.rerun()
        else:
            st.info("No log entries found.")
    else:
        st.warning("Log file not found. Make sure the API is running and generating logs.")
    
    # Log statistics
    st.subheader("📊 Log Statistics")
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        api_calls = [line for line in lines if "API_CALL:" in line]
        errors = [line for line in lines if "API_ERROR:" in line]
        ml_predictions = [line for line in lines if "ML_PREDICTION:" in line]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total API Calls", len(api_calls))
        
        with col2:
            st.metric("Total Errors", len(errors))
        
        with col3:
            st.metric("ML Predictions", len(ml_predictions))

if __name__ == "__main__":
    main() 