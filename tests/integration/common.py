"""Common fixtures and utilities for integration tests."""

import urllib.request
import urllib.parse
import json

def api_url():
    """Return the base URL for the API."""
    return "http://localhost:7000/api"


def wait_for_api(timeout=30):
    """Wait for the API to be available."""
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = make_request("http://localhost:7000/health")
            if response["status"] == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    raise TimeoutError("API did not become available within the timeout period.")


def make_request(url, method="GET", headers={}, data=None):
    """Make an HTTP request to the API."""
    if data is not None:
        if method == "GET":
            # append as query parameters
            params = urllib.parse.urlencode(data)
            url = f"{url}?{params}"
            data = None
        else:
            if isinstance(data, dict):
                data = urllib.parse.urlencode(data).encode()
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            elif isinstance(data, str):
                data = data.encode()
                headers["Content-Type"] = "text/plain"
    req = urllib.request.Request(url, method=method, headers=headers, data=data)

    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode()
            return {
                "status": response.status,
                "content": content,
                "json": lambda: json.loads(content) if content else {},
            }
    except urllib.error.HTTPError as e:
        content = e.read().decode()
        return {
            "status": e.code,
            "content": content,
            "json": lambda: json.loads(content) if content else {},
        }
    except Exception as e:
        print(f"Error making request: {e}")
        return {
            "status": 500,
            "content": str(e),
            "json": lambda: {},
        }