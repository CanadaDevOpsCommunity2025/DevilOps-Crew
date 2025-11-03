#!/usr/bin/env python3
"""
API Integration Tests for TV Research Tool
Run with: python -m pytest tests/test_api.py -v
"""

import pytest
import requests
import time
import os
from typing import Dict, Any

# Test configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

class TestAPI:
    """Test suite for TV Research API"""

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"

    def test_research_list(self):
        """Test getting research list"""
        response = requests.get(f"{API_BASE_URL}/research")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_research_creation(self):
        """Test creating new research"""
        research_data = {
            "topic": "API Test Topic"
        }

        response = requests.post(f"{API_BASE_URL}/research", json=research_data)
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert data["topic"] == research_data["topic"]
        assert data["status"] in ["queued", "running", "completed"]

        return data["id"]

    def test_research_retrieval(self):
        """Test getting specific research"""
        # First create a research
        research_id = self.test_research_creation()

        # Then retrieve it
        response = requests.get(f"{API_BASE_URL}/research/{research_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == research_id
        assert "status" in data
        assert "topic" in data

    def test_queue_status(self):
        """Test queue status endpoint"""
        response = requests.get(f"{API_BASE_URL}/queue/status")
        assert response.status_code == 200

        data = response.json()
        assert "queues" in data
        assert "timestamp" in data
        assert isinstance(data["queues"], dict)

        # Check expected queue types
        expected_queues = ["trend_research", "news_aggregation", "content_strategy", "final_reporting"]
        for queue in expected_queues:
            assert queue in data["queues"]

    def test_invalid_research_id(self):
        """Test retrieving non-existent research"""
        response = requests.get(f"{API_BASE_URL}/research/99999")
        assert response.status_code == 404

    def test_research_workflow_completion(self):
        """Test complete research workflow (may take time)"""
        # Create research
        research_data = {"topic": "Workflow Test Topic"}
        response = requests.post(f"{API_BASE_URL}/research", json=research_data)
        assert response.status_code == 200

        research_id = response.json()["id"]

        # Monitor progress (with timeout)
        max_attempts = 120  # 10 minutes max for CI/CD
        attempt = 0

        while attempt < max_attempts:
            response = requests.get(f"{API_BASE_URL}/research/{research_id}")
            assert response.status_code == 200

            data = response.json()
            status = data["status"]

            if status == "completed":
                # Verify execution time is tracked
                assert "execution_time" in data
                assert data["execution_time"] is not None
                assert data["execution_time"] > 0
                break
            elif status == "failed":
                pytest.fail(f"Research failed: {data.get('error_message', 'Unknown error')}")

            time.sleep(5)
            attempt += 1
        else:
            pytest.fail("Research workflow timed out")

def test_container_validation():
    """Test that containers are properly built and functional"""
    import subprocess

    # Test Python version in container
    result = subprocess.run(
        ["docker", "run", "--rm", "tv-research:test", "python", "--version"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Python 3.12" in result.stdout

    # Test key dependencies
    result = subprocess.run(
        ["docker", "run", "--rm", "tv-research:test", "pip", "list"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "crewai" in result.stdout
    assert "fastapi" in result.stdout
    assert "streamlit" in result.stdout

if __name__ == "__main__":
    # Run basic smoke tests
    print("🧪 Running API smoke tests...")

    api = TestAPI()

    try:
        api.test_health_endpoint()
        print("✅ Health endpoint test passed")

        api.test_research_list()
        print("✅ Research list test passed")

        api.test_queue_status()
        print("✅ Queue status test passed")

        print("🎉 All smoke tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)
