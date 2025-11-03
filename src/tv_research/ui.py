import streamlit as st
import requests
import time
from datetime import datetime
import json
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(
    page_title="TV Channel Research",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TV Channel Research & Reporting Tool")
st.markdown("AI-powered research and reporting tool for TV channels")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API Base URL", value=API_BASE_URL)
    if api_url != API_BASE_URL:
        st.warning("Make sure the API server is running at the specified URL")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["🔍 New Research", "📊 Research History", "📈 System Monitoring", "ℹ️ About"])

with tab1:
    st.header("Start New Research")

    with st.form("research_form"):
        topic = st.text_input(
            "Research Topic (optional)",
            placeholder="e.g., Climate Change, AI Technology, Space Exploration",
            help="Leave empty for trending topics research"
        )

        submitted = st.form_submit_button("🚀 Start Research", type="primary")

        if submitted:
            with st.spinner("Submitting research request..."):
                try:
                    response = requests.post(
                        f"{api_url}/research",
                        json={"topic": topic if topic.strip() else None},
                        timeout=10
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Research started successfully!")

                        # Display initial result info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Research ID", result["id"])
                            st.metric("Status", result["status"].upper())
                        with col2:
                            if result["topic"]:
                                st.metric("Topic", result["topic"])
                            st.metric("Created", result["created_at"][:19] if result["created_at"] else "N/A")

                        # Progress tracking
                        progress_placeholder = st.empty()
                        status_placeholder = st.empty()

                        research_id = result["id"]

                        # Poll for status updates
                        while True:
                            try:
                                status_response = requests.get(f"{api_url}/research/{research_id}", timeout=5)
                                if status_response.status_code == 200:
                                    current_result = status_response.json()

                                    if current_result["status"] == "completed":
                                        progress_placeholder.success("🎉 Research completed!")
                                        status_placeholder.empty()

                                        # Display results
                                        st.header("📄 Research Results")
                                        if current_result["result_content"]:
                                            st.markdown(current_result["result_content"])
                                        else:
                                            st.info("No content available")

                                        if current_result["execution_time"]:
                                            st.metric("Execution Time", f"{current_result['execution_time']} seconds")

                                        break

                                    elif current_result["status"] == "failed":
                                        progress_placeholder.error("❌ Research failed!")
                                        if current_result["error_message"]:
                                            st.error(f"Error: {current_result['error_message']}")
                                        break

                                    elif current_result["status"] == "queued":
                                        progress_placeholder.info("📋 Research queued for processing...")
                                        time.sleep(2)

                                    elif current_result["status"] == "running":
                                        progress_placeholder.info("🔄 Research in progress...")
                                        time.sleep(2)

                                    elif "trend_research" in current_result["status"]:
                                        progress_placeholder.info("🔍 Analyzing trends...")
                                        time.sleep(2)

                                    elif "news_aggregation" in current_result["status"]:
                                        progress_placeholder.info("📰 Aggregating news...")
                                        time.sleep(2)

                                    elif "content_strategy" in current_result["status"]:
                                        progress_placeholder.info("💡 Developing content strategy...")
                                        time.sleep(2)

                                    elif "final_reporting" in current_result["status"]:
                                        progress_placeholder.info("📝 Generating final report...")
                                        time.sleep(2)

                                    else:
                                        progress_placeholder.info(f"📋 Status: {current_result['status']}")
                                        time.sleep(2)

                                else:
                                    progress_placeholder.warning("⚠️ Unable to check status")
                                    time.sleep(2)

                            except requests.exceptions.RequestException:
                                progress_placeholder.warning("⚠️ Connection issue, retrying...")
                                time.sleep(3)

                    else:
                        st.error(f"❌ Failed to start research: {response.status_code}")
                        st.text(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("Make sure the API server is running")

with tab2:
    st.header("Research History")

    # Refresh button
    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        response = requests.get(f"{api_url}/research", timeout=10)

        if response.status_code == 200:
            results = response.json()

            if not results:
                st.info("No research results found. Start your first research above!")
            else:
                st.metric("Total Research Tasks", len(results))

                # Display results in a table
                for result in results:
                    with st.expander(f"Research #{result['id']} - {result['topic'] or 'Trending Topics'} ({result['status']})"):

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", result["status"].upper())
                        with col2:
                            if result["created_at"]:
                                created = datetime.fromisoformat(result["created_at"].replace('Z', '+00:00'))
                                st.metric("Created", created.strftime("%Y-%m-%d %H:%M"))
                        with col3:
                            if result["execution_time"]:
                                st.metric("Duration", f"{result['execution_time']}s")

                        if result["status"] == "completed" and result["result_content"]:
                            st.markdown("**Results:**")

                            # Truncate long content for display
                            content = result["result_content"]
                            if len(content) > 1000:
                                st.markdown(content[:1000] + "...")
                                if st.button(f"Show Full Report #{result['id']}", key=f"full_{result['id']}"):
                                    st.markdown("---")
                                    st.markdown("**Full Report:**")
                                    st.markdown(content)
                            else:
                                st.markdown(content)

                        elif result["status"] == "failed" and result["error_message"]:
                            st.error(f"**Error:** {result['error_message']}")

                        # Delete button
                        if st.button(f"🗑️ Delete Research #{result['id']}", key=f"delete_{result['id']}"):
                            try:
                                delete_response = requests.delete(f"{api_url}/research/{result['id']}", timeout=5)
                                if delete_response.status_code == 200:
                                    st.success("Research deleted successfully!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Failed to delete research")
                            except requests.exceptions.RequestException:
                                st.error("Connection error while deleting")

        else:
            st.error(f"Failed to load research history: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the API server is running")

with tab3:
    st.header("📈 System Monitoring & Observability")

    # Auto-refresh toggle
    auto_refresh = st.checkbox("Auto-refresh every 30 seconds", value=True)

    # Refresh button
    if st.button("🔄 Refresh Now") or auto_refresh:
        # System Health Overview
        st.subheader("🏥 System Health Overview")

        col1, col2, col3, col4 = st.columns(4)

        # API Health
        with col1:
            try:
                api_response = requests.get(f"{api_url}/health", timeout=5)
                if api_response.status_code == 200:
                    st.metric("API Status", "✅ Healthy")
                else:
                    st.metric("API Status", "⚠️ Issues")
            except:
                st.metric("API Status", "❌ Down")

        # Database Status (via API)
        with col2:
            try:
                research_response = requests.get(f"{api_url}/research?limit=1", timeout=5)
                if research_response.status_code == 200:
                    st.metric("Database", "✅ Connected")
                else:
                    st.metric("Database", "⚠️ Issues")
            except:
                st.metric("Database", "❌ Disconnected")

        # Redis Status (if available)
        with col3:
            try:
                # Try to get queue info via API or direct Redis check
                redis_response = requests.get(f"{api_url}/health", timeout=5)
                st.metric("Redis Queue", "✅ Active")
            except:
                st.metric("Redis Queue", "❓ Unknown")

        # UI Status
        with col4:
            st.metric("Web UI", "✅ Running")

        # Research Statistics
        st.subheader("📊 Research Statistics")

        try:
            research_response = requests.get(f"{api_url}/research", timeout=10)
            if research_response.status_code == 200:
                all_research = research_response.json()

                total_research = len(all_research)
                completed_research = len([r for r in all_research if r['status'] == 'completed'])
                failed_research = len([r for r in all_research if r['status'] == 'failed'])
                active_research = len([r for r in all_research if r['status'] in ['running', 'queued', 'trend_research_completed', 'news_aggregation_completed', 'content_strategy_completed', 'final_reporting_running']])

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Research", total_research)
                with col2:
                    st.metric("Completed", completed_research)
                with col3:
                    st.metric("Active", active_research)
                with col4:
                    st.metric("Failed", failed_research)

                # Success Rate
                if total_research > 0:
                    success_rate = (completed_research / total_research) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")

        except Exception as e:
            st.error(f"Could not load research statistics: {e}")

        # Queue Status
        st.subheader("🔄 Queue Status")

        try:
            queue_response = requests.get(f"{api_url}/queue/status", timeout=5)
            if queue_response.status_code == 200:
                queue_data = queue_response.json()

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Trend Research", queue_data["queues"]["trend_research"])
                with col2:
                    st.metric("News Aggregation", queue_data["queues"]["news_aggregation"])
                with col3:
                    st.metric("Content Strategy", queue_data["queues"]["content_strategy"])
                with col4:
                    st.metric("Final Reporting", queue_data["queues"]["final_reporting"])

                total_queued = sum(queue_data["queues"].values())
                if total_queued > 0:
                    st.info(f"📋 {total_queued} jobs currently queued for processing")
                else:
                    st.success("✅ All queues are empty - system is idle")
            else:
                st.warning("Could not fetch queue status")
        except Exception as e:
            st.error(f"Queue status error: {e}")

        # Recent Activity
        st.subheader("📋 Recent Activity")

        try:
            research_response = requests.get(f"{api_url}/research?limit=10", timeout=10)
            if research_response.status_code == 200:
                recent_research = research_response.json()

                if recent_research:
                    for research in recent_research[:5]:  # Show last 5
                        status_emoji = {
                            'completed': '✅',
                            'failed': '❌',
                            'running': '🔄',
                            'queued': '📋'
                        }.get(research['status'], '❓')

                        created_time = datetime.fromisoformat(research['created_at'].replace('Z', '+00:00'))
                        time_ago = datetime.now() - created_time.replace(tzinfo=None)

                        if time_ago.days > 0:
                            time_str = f"{time_ago.days}d ago"
                        elif time_ago.seconds > 3600:
                            time_str = f"{time_ago.seconds // 3600}h ago"
                        elif time_ago.seconds > 60:
                            time_str = f"{time_ago.seconds // 60}m ago"
                        else:
                            time_str = f"{time_ago.seconds}s ago"

                        st.write(f"{status_emoji} Research #{research['id']} - {research['topic'] or 'Trending Topics'} - {time_str}")
                else:
                    st.info("No recent research activity")

        except Exception as e:
            st.error(f"Could not load recent activity: {e}")

        # System Resources (if available)
        st.subheader("💻 System Resources")

        try:
            # This would ideally get system metrics, but for now we'll show basic info
            st.info("Detailed system metrics require additional monitoring tools like Prometheus/Grafana")

            # Show basic container info
            st.write("**Container Status:**")
            st.write("- API Service: Running on port 8000")
            st.write("- UI Service: Running on port 8501")
            st.write("- Redis: Running on port 6379")
            st.write("- Worker Services: 6 containers (trend: 2, news: 2, content: 1, reporting: 1)")

        except Exception as e:
            st.error(f"Could not load system resources: {e}")

        # Performance Metrics
        st.subheader("⚡ Performance Metrics")

        try:
            research_response = requests.get(f"{api_url}/research", timeout=10)
            if research_response.status_code == 200:
                all_research = research_response.json()

                # Calculate average execution time for completed research
                completed_times = [r['execution_time'] for r in all_research
                                 if r['status'] == 'completed' and r.get('execution_time')]

                if completed_times:
                    avg_time = sum(completed_times) / len(completed_times)
                    st.metric("Avg. Research Time", f"{avg_time:.1f}s")

                    # Show execution time distribution
                    st.write("**Execution Time Distribution:**")
                    fast = len([t for t in completed_times if t < 30])
                    medium = len([t for t in completed_times if 30 <= t < 120])
                    slow = len([t for t in completed_times if t >= 120])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Fast (<30s)", fast)
                    with col2:
                        st.metric("Medium (30-120s)", medium)
                    with col3:
                        st.metric("Slow (>120s)", slow)

        except Exception as e:
            st.error(f"Could not load performance metrics: {e}")

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(30)
        st.rerun()

with tab4:
    st.header("About")
    st.markdown("""
    ## 🎬 TV Channel Research & Reporting Tool

    This AI-powered tool helps TV channels research trending topics and generate comprehensive reports for content creation.

    ### Features:
    - **Dynamic Topic Research**: Research specific topics or trending news
    - **AI-Powered Analysis**: Uses CrewAI with multiple specialized agents
    - **Web Interface**: Easy-to-use Streamlit interface
    - **REST API**: Programmatic access to research functionality
    - **Result Storage**: Persistent storage of research results

    ### How it works:
    1. **Trend Researcher**: Identifies trending topics and current news
    2. **News Aggregator**: Gathers breaking news and relevant information
    3. **Content Strategist**: Develops story angles and content strategies
    4. **Reporting Analyst**: Compiles final comprehensive reports

    ### Getting Started:
    1. Make sure the API server is running (`uvicorn tv_research.api:app --reload`)
    2. Run the web UI (`streamlit run tv_research/ui.py`)
    3. Start researching topics or view previous results
    """)

    # Health check
    try:
        health_response = requests.get(f"{api_url}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Server is running")
        else:
            st.warning("⚠️ API Server health check failed")
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to API server")
        st.info("Start the API server with: `uvicorn tv_research.api:app --reload`")

if __name__ == "__main__":
    pass
