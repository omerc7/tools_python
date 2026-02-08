import argparse
import json
import ssl
import socket
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests


def get_ssl_expiry(hostname, port=443):
    """Get SSL certificate expiry date for a hostname."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, port))
            cert = s.getpeercert()
            expiry_str = cert["notAfter"]
            expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            days_left = (expiry_date - datetime.now(timezone.utc)).days
            return {
                "expiry_date": expiry_date.isoformat(),
                "days_remaining": days_left,
                "issuer": dict(x[0] for x in cert.get("issuer", [])),
                "subject": dict(x[0] for x in cert.get("subject", [])),
            }
    except Exception as e:
        return {"error": str(e)}


def check_url_health(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    result = {
        "url": url,
        "hostname": parsed.hostname,
    }

    # HTTP check
    try:
        start = time.time()
        resp = requests.get(url, timeout=15, allow_redirects=True)
        elapsed_ms = round((time.time() - start) * 1000)

        redirect_chain = []
        if resp.history:
            for r in resp.history:
                redirect_chain.append({
                    "url": r.url,
                    "status_code": r.status_code,
                })

        result["status_code"] = resp.status_code
        result["response_time_ms"] = elapsed_ms
        result["final_url"] = resp.url
        result["redirect_chain"] = redirect_chain
        result["content_type"] = resp.headers.get("Content-Type", "")
        result["server"] = resp.headers.get("Server", "")
        result["healthy"] = 200 <= resp.status_code < 400
    except requests.exceptions.ConnectionError:
        result["healthy"] = False
        result["error"] = "Connection failed"
    except requests.exceptions.Timeout:
        result["healthy"] = False
        result["error"] = "Request timed out"
    except requests.exceptions.RequestException as e:
        result["healthy"] = False
        result["error"] = str(e)

    # SSL check
    if parsed.scheme == "https":
        result["ssl"] = get_ssl_expiry(parsed.hostname)

    # Print results
    healthy_str = "HEALTHY" if result.get("healthy") else "UNHEALTHY"
    print(f"URL Health Check: {url}")
    print("=" * 50)
    print(f"  Status:          {healthy_str}")

    if "status_code" in result:
        print(f"  Status Code:     {result['status_code']}")
        print(f"  Response Time:   {result['response_time_ms']} ms")
        print(f"  Content-Type:    {result.get('content_type', 'N/A')}")
        print(f"  Server:          {result.get('server', 'N/A')}")
    if "error" in result:
        print(f"  Error:           {result['error']}")
    if result.get("redirect_chain"):
        print(f"  Redirects:       {len(result['redirect_chain'])} hop(s)")
        for i, hop in enumerate(result["redirect_chain"], 1):
            print(f"    {i}. [{hop['status_code']}] {hop['url']}")
        print(f"  Final URL:       {result['final_url']}")

    ssl_info = result.get("ssl")
    if ssl_info and "error" not in ssl_info:
        print(f"\n  SSL Certificate:")
        print(f"    Expires:       {ssl_info['expiry_date']}")
        print(f"    Days Left:     {ssl_info['days_remaining']}")
        issuer_cn = ssl_info.get("issuer", {}).get("organizationName", "N/A")
        print(f"    Issuer:        {issuer_cn}")
    elif ssl_info and "error" in ssl_info:
        print(f"\n  SSL Error:       {ssl_info['error']}")

    print("=" * 50)
    print("\nJSON Output:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check health of a URL endpoint")
    parser.add_argument("url", help="URL to check (e.g. https://example.com)")
    args = parser.parse_args()
    check_url_health(args.url)
