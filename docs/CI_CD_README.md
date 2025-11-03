# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions for comprehensive CI/CD automation that validates container builds, runs API tests, and performs integration testing on every commit.

## Pipeline Structure

### Jobs Overview

1. **validate-containers**: Docker build validation and basic checks
2. **test-containers**: Container functionality and service health tests
3. **api-tests**: REST API endpoint testing
4. **integration-tests**: Full workflow testing from research creation to completion
5. **security-scan**: Vulnerability scanning with Trivy
6. **cleanup**: Resource cleanup (always runs)

### Trigger Configuration

```yaml
on:
  push:
    branches: [ francis ]  # Currently set to francis branch
  pull_request:
    branches: [ francis ]  # PRs to francis branch
```

**Note**: Change `francis` to `main` when ready for production deployment.

## Test Coverage

### Container Validation
- ✅ Docker image builds successfully
- ✅ Python 3.12 runtime available
- ✅ Key dependencies installed (CrewAI, FastAPI, Streamlit)
- ✅ Image tagging and caching

### Service Health Checks
- ✅ All containers start properly
- ✅ Redis connectivity (PING command)
- ✅ API health endpoint (`/health`)
- ✅ UI service accessibility
- ✅ Docker Compose orchestration

### API Testing
- ✅ Health endpoint functionality
- ✅ Research list retrieval
- ✅ Research creation (POST)
- ✅ Research retrieval (GET)
- ✅ Queue status monitoring
- ✅ Error handling (404 responses)

### Integration Testing
- ✅ Complete research workflow
- ✅ Status progression tracking
- ✅ Execution time validation
- ✅ Timeout handling (10 minutes max)
- ✅ Result verification

### Security Scanning
- ✅ Trivy vulnerability scanning
- ✅ SARIF report generation
- ✅ GitHub Security tab integration

## Running Tests Locally

### Prerequisites
```bash
# Install test dependencies
pip install requests pytest

# Ensure Docker and Docker Compose are available
docker --version
docker compose version
```

### Run API Tests
```bash
# Start the application
docker compose up -d

# Wait for services to be ready
sleep 45

# Run API tests
python -m pytest tests/test_api.py -v

# Or run smoke tests directly
python tests/test_api.py
```

### Run Integration Tests
```bash
# Full workflow test (may take several minutes)
python -c "
import requests
import time

# Start research
response = requests.post('http://localhost:8000/research', json={'topic': 'Test Topic'})
research_id = response.json()['id']

# Monitor completion
while True:
    status = requests.get(f'http://localhost:8000/research/{research_id}').json()['status']
    if status == 'completed':
        print('✅ Integration test passed!')
        break
    time.sleep(5)
"
```

## Pipeline Configuration

### Environment Variables
- `API_BASE_URL`: API endpoint for testing (default: `http://localhost:8000`)
- `REGISTRY`: Container registry (default: `ghcr.io`)
- `IMAGE_NAME`: Repository name for tagging

### Timeouts and Limits
- **Container startup**: 30-45 seconds
- **API test timeout**: 5 seconds per request
- **Integration test timeout**: 10 minutes (120 attempts × 5 seconds)
- **Security scan**: Filesystem scan with SARIF output

### Resource Requirements
- **Runner**: Ubuntu latest (GitHub-hosted)
- **Docker**: Buildx with caching enabled
- **Memory**: Sufficient for running multiple containers
- **Network**: External access for dependency downloads

## Troubleshooting

### Common Issues

**Container Build Failures**
```bash
# Check Docker build logs
docker build --progress=plain .

# Validate Dockerfile syntax
docker build --dry-run .
```

**API Test Failures**
```bash
# Check service logs
docker compose logs api

# Test API manually
curl http://localhost:8000/health

# Check container networking
docker network ls
```

**Integration Test Timeouts**
```bash
# Check worker status
docker ps | grep worker

# Monitor queue status
curl http://localhost:8000/queue/status

# Check Redis connectivity
docker exec tv-research-redis redis-cli ping
```

**Security Scan Issues**
```bash
# Run Trivy locally
docker run --rm -v $(pwd):/app aquasecurity/trivy fs /app

# Check SARIF output
cat trivy-results.sarif | jq '.runs[0].results'
```

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export PYTHONUNBUFFERED=1
export LOG_LEVEL=DEBUG
```

## Branch Strategy

### Current Setup (Francis Branch)
- All CI/CD runs on `francis` branch
- Manual testing and validation
- Ready for production migration

### Production Migration
1. Update workflow triggers to `main` branch
2. Test thoroughly on `francis` first
3. Merge to `main` when confident
4. Monitor first few production runs

## Performance Optimization

### Caching Strategies
- Docker layer caching with GitHub Actions
- Dependency caching for Python packages
- Build context optimization

### Parallel Execution
- Jobs run in parallel where possible
- Dependency chains prevent conflicts
- Cleanup job runs regardless of success/failure

### Resource Management
- Automatic cleanup of containers and volumes
- Docker system pruning after tests
- Efficient use of GitHub Actions minutes

## Monitoring and Alerts

### Success Criteria
- ✅ All jobs pass without failures
- ✅ Security scan has no critical vulnerabilities
- ✅ Integration tests complete within timeout
- ✅ API endpoints respond correctly

### Failure Notifications
- GitHub Actions provides automatic status checks
- PR status updates for branch protection
- Detailed logs available in Actions tab

## Future Enhancements

### Additional Test Coverage
- Load testing with multiple concurrent requests
- Performance benchmarking
- Cross-browser UI testing
- Database migration testing

### Deployment Integration
- Automatic deployment to staging on success
- Blue-green deployment strategies
- Rollback capabilities
- Environment-specific configurations

### Advanced Security
- SAST (Static Application Security Testing)
- Dependency vulnerability scanning
- Secret scanning and rotation
- Compliance checks (SOC2, GDPR, etc.)

---

## Quick Reference

**Trigger Pipeline**: Push to `francis` branch or create PR

**View Results**: GitHub Actions tab → CI/CD Pipeline

**Run Locally**: `docker compose up -d && python tests/test_api.py`

**Debug Issues**: Check container logs with `docker compose logs`

**Security Reports**: Available in Security tab → Vulnerability alerts
