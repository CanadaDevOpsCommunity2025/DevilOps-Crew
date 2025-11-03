#!/usr/bin/env python3
"""
Basic API Tests for TV Channel Research System

These tests validate the core API functionality without requiring
full container orchestration.
"""

import pytest
import requests
import time
import json
from typing import Dict, Any


class TestAPI:
    """Test suite for API endpoints"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health endpoint test passed")

    def test_list_research_empty(self):
        """Test listing research results when empty"""
        response = self.session.get(f"{self.base_url}/research")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        print("✅ List research (empty) test passed")

    def test_create_research_task(self):
        """Test creating a research task"""
        payload = {"topic": "API Test Topic"}
        response = self.session.post(
            f"{self.base_url}/research",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert data["topic"] == payload["topic"]
        assert data["status"] in ["queued", "pending", "running"]

        # Store the research ID for other tests
        self.research_id = data["id"]
        print(f"✅ Create research task test passed (ID: {self.research_id})")

        return data

    def test_get_research_task(self):
        """Test getting a specific research task"""
        if not hasattr(self, 'research_id'):
            self.test_create_research_task()

        response = self.session.get(f"{self.base_url}/research/{self.research_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == self.research_id
        assert "status" in data
        assert "created_at" in data
        print("✅ Get research task test passed")

    def test_research_status_progression(self):
        """Test that research status progresses correctly"""
        if not hasattr(self, 'research_id'):
            self.test_create_research_task()

        # Check status progression over time
        max_checks = 10
        for i in range(max_checks):
            response = self.session.get(f"{self.base_url}/research/{self.research_id}")
            assert response.status_code == 200

            data = response.json()
            status = data["status"]

            print(f"Status check {i+1}: {status}")

            # Valid status progression
            valid_statuses = ["queued", "running", "trend_research_completed",
                            "news_aggregation_completed", "content_strategy_completed",
                            "final_reporting_running", "completed", "failed"]

            assert status in valid_statuses

            # If completed or failed, stop checking
            if status in ["completed", "failed"]:
                print(f"✅ Research reached final status: {status}")
                break

            time.sleep(3)  # Wait before next check

        print("✅ Status progression test passed")

    def test_delete_research_task(self):
        """Test deleting a research task"""
        if not hasattr(self, 'research_id'):
            self.test_create_research_task()

        response = self.session.delete(f"{self.base_url}/research/{self.research_id}")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        print("✅ Delete research task test passed")

    def test_get_deleted_research_task(self):
        """Test that deleted research task returns 404"""
        if not hasattr(self, 'research_id'):
            return  # Skip if no research ID

        response = self.session.get(f"{self.base_url}/research/{self.research_id}")
        assert response.status_code == 404
        print("✅ Get deleted research task test passed (404)")

    def test_api_error_handling(self):
        """Test API error handling"""
        # Test invalid research ID
        response = self.session.get(f"{self.base_url}/research/invalid-id")
        assert response.status_code == 422  # FastAPI validation error

        # Test non-existent endpoint
        response = self.session.get(f"{self.base_url}/nonexistent")
        assert response.status_code == 404

        print("✅ API error handling test passed")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Tests\n")

        test_methods = [
            self.test_health_endpoint,
            self.test_list_research_empty,
            self.test_create_research_task,
            self.test_get_research_task,
            self.test_research_status_progression,
            self.test_api_error_handling,
            self.test_delete_research_task,
            self.test_get_deleted_research_task,
        ]

        passed = 0
        failed = 0

        for test_method in test_methods:
            try:
                print(f"\n{'='*50}")
                print(f"🔍 Running: {test_method.__name__}")
                print('='*50)

                test_method()
                passed += 1
                print(f"✅ PASSED: {test_method.__name__}")

            except Exception as e:
                failed += 1
                print(f"❌ FAILED: {test_method.__name__} - {e}")

        print(f"\n{'='*60}")
        print("📊 API TEST RESULTS")
        print('='*60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Total:  {passed + failed}")

        if failed == 0:
            print("🎉 ALL API TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME API TESTS FAILED")
            return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run API tests for TV Channel Research")
    parser.add_argument("--url", default="http://localhost:8000",
                       help="API base URL (default: http://localhost:8000)")
    parser.add_argument("--skip-integration", action="store_true",
                       help="Skip integration tests that require workers")

    args = parser.parse_args()

    print(f"🧪 Testing API at: {args.url}")

    tester = TestAPI(args.url)

    if args.skip_integration:
        # Run only basic endpoint tests
        try:
            tester.test_health_endpoint()
            tester.test_list_research_empty()
            tester.test_api_error_handling()
            print("🎉 Basic API tests passed!")
            return True
        except Exception as e:
            print(f"❌ Basic API tests failed: {e}")
            return False
    else:
        # Run full test suite
        return tester.run_all_tests()


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
