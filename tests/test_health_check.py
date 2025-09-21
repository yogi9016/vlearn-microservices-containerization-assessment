import pytest
import requests

# Base URLs of the services
SERVICES = {
    "user-service": "http://localhost:3000/health",
    "product-service": "http://localhost:3001/health",
    "order-service": "http://localhost:3002/health",
    "gateway-service": "http://localhost:3003/health"
}

@pytest.mark.parametrize("service_name, url", SERVICES.items())
def test_service_health(service_name, url):
    """
    Health check for microservices.
    Expects HTTP 200 response from the /health endpoint.
    """
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"{service_name} is down or /health endpoint failed."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"{service_name} health check failed: {e}")