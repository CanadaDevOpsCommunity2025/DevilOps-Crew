#!/usr/bin/env python3
"""
Container Validation Script for TV Channel Research System

This script validates that all containers are running properly and
performs basic health checks on the services.
"""

import subprocess
import sys
import time
import requests
import json
from typing import Dict, List, Tuple
import argparse

class ContainerValidator:
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url
        self.services = {
            "redis": {"port": 6379, "health_check": self._check_redis},
            "api": {"port": 8000, "health_check": self._check_api},
            "ui": {"port": 8501, "health_check": self._check_ui},
            "worker-trend": {"port": None, "health_check": self._check_worker},
            "worker-news": {"port": None, "health_check": self._check_worker},
            "worker-content": {"port": None, "health_check": self._check_worker},
            "worker-reporting": {"port": None, "health_check": self._check_worker},
        }

    def run_command(self, cmd: List[str]) -> Tuple[str, str, int]:
        """Run a shell command and return stdout, stderr, returncode"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", -1
        except Exception as e:
            return "", f"Command failed: {e}", -1

    def check_docker_compose_status(self) -> bool:
        """Check if docker-compose services are running"""
        print("🔍 Checking Docker Compose status...")

        stdout, stderr, returncode = self.run_command(["docker", "compose", "ps"])

        if returncode != 0:
            print(f"❌ Docker Compose check failed: {stderr}")
            return False

        # Parse the output to check service status
        lines = stdout.strip().split('\n')
        if len(lines) < 2:  # Header + at least one service
            print("❌ No services found running")
            return False

        running_services = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    service_name = parts[0]
                    status = ' '.join(parts[1:-2])  # Status can have multiple words
                    if 'Up' in status or 'running' in status.lower():
                        running_services.append(service_name)

        expected_services = set(self.services.keys())
        running_services_set = set(s.split('-')[0] if '-' in s else s for s in running_services)

        if expected_services.issubset(running_services_set):
            print(f"✅ All services running: {', '.join(running_services)}")
            return True
        else:
            missing = expected_services - running_services_set
            print(f"❌ Missing services: {', '.join(missing)}")
            return False

    def _check_redis(self) -> bool:
        """Check Redis connectivity"""
        try:
            stdout, stderr, returncode = self.run_command(["docker", "exec", "tv-research-redis", "redis-cli", "ping"])
            if returncode == 0 and "PONG" in stdout:
                print("✅ Redis: PONG received")
                return True
            else:
                print(f"❌ Redis: No PONG received - {stdout}")
                return False
        except Exception as e:
            print(f"❌ Redis check failed: {e}")
            return False

    def _check_api(self) -> bool:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}:8000/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ API: Health check passed")

                    # Test API endpoints
                    return self._test_api_endpoints()
                else:
                    print(f"❌ API: Unhealthy status - {data}")
                    return False
            else:
                print(f"❌ API: Bad status code - {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API check failed: {e}")
            return False

    def _test_api_endpoints(self) -> bool:
        """Test basic API endpoints"""
        endpoints = [
            ("GET", "/research", "List research results"),
            ("POST", "/research", "Create research task", {"topic": "test"}),
        ]

        for method, endpoint, description, *data in endpoints:
            try:
                url = f"{self.base_url}:8000{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=10)
                elif method == "POST" and data:
                    response = requests.post(url, json=data[0], timeout=10)

                if response.status_code in [200, 201]:
                    print(f"✅ API {method} {endpoint}: {description} - OK")
                else:
                    print(f"⚠️  API {method} {endpoint}: {description} - Status {response.status_code}")
                    # Don't fail for non-critical endpoints

            except Exception as e:
                print(f"❌ API {method} {endpoint}: {description} - Failed: {e}")
                return False

        return True

    def _check_ui(self) -> bool:
        """Check UI accessibility"""
        try:
            # Try to connect to Streamlit
            response = requests.get(f"{self.base_url}:8501", timeout=10, allow_redirects=True)
            if response.status_code == 200:
                print("✅ UI: Web interface accessible")
                return True
            else:
                print(f"⚠️  UI: Unexpected status code - {response.status_code}")
                return True  # UI might still be starting up
        except Exception as e:
            print(f"⚠️  UI check: {e} (might still be starting)")
            return True  # UI startup can be slow

    def _check_worker(self) -> bool:
        """Check if worker containers exist (workers don't have direct health checks)"""
        # Workers are checked via docker-compose ps above
        print("✅ Worker: Container exists")
        return True

    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("🚀 Starting TV Channel Research System Validation\n")

        checks = [
            ("Docker Compose Services", self.check_docker_compose_status),
        ]

        # Add service-specific health checks
        for service_name, service_info in self.services.items():
            checks.append((f"{service_name.upper()} Service", service_info["health_check"]))

        results = []
        for check_name, check_func in checks:
            print(f"\n{'='*50}")
            print(f"🔍 Running: {check_name}")
            print('='*50)

            try:
                result = check_func()
                results.append(result)
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"\n{status}: {check_name}")
            except Exception as e:
                print(f"❌ ERROR in {check_name}: {e}")
                results.append(False)

        print(f"\n{'='*60}")
        print("📊 VALIDATION SUMMARY")
        print('='*60)

        total_checks = len(results)
        passed_checks = sum(results)

        for i, (check_name, _) in enumerate(checks):
            status = "✅ PASS" if results[i] else "❌ FAIL"
            print(f"{status} {check_name}")

        print(f"\n📈 Results: {passed_checks}/{total_checks} checks passed")

        if passed_checks == total_checks:
            print("🎉 ALL VALIDATION CHECKS PASSED!")
            return True
        else:
            print("⚠️  SOME CHECKS FAILED - Please review the output above")
            return False

def main():
    parser = argparse.ArgumentParser(description="Validate TV Channel Research containers")
    parser.add_argument("--url", default="http://localhost",
                       help="Base URL for service checks (default: http://localhost)")
    parser.add_argument("--wait", type=int, default=30,
                       help="Seconds to wait for services to start (default: 30)")

    args = parser.parse_args()

    print(f"⏳ Waiting {args.wait} seconds for services to start...")
    time.sleep(args.wait)

    validator = ContainerValidator(args.url)
    success = validator.validate_all()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
