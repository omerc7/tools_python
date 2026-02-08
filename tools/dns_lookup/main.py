import argparse
import json
import socket


RECORD_TYPES = {
    "A": socket.AF_INET,
    "AAAA": socket.AF_INET6,
}


def resolve_basic(domain):
    """Resolve A and AAAA records using socket.getaddrinfo."""
    results = {}
    for rtype, family in RECORD_TYPES.items():
        try:
            infos = socket.getaddrinfo(domain, None, family, socket.SOCK_STREAM)
            results[rtype] = sorted(set(addr[4][0] for addr in infos))
        except socket.gaierror:
            results[rtype] = []
    return results


def resolve_mx(domain):
    """Resolve MX records using dns.resolver."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        return [{"priority": r.preference, "host": str(r.exchange).rstrip(".")} for r in answers]
    except Exception:
        return []


def resolve_ns(domain):
    """Resolve NS records using dns.resolver."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "NS")
        return [str(r.target).rstrip(".") for r in answers]
    except Exception:
        return []


def resolve_cname(domain):
    """Resolve CNAME records using dns.resolver."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "CNAME")
        return [str(r.target).rstrip(".") for r in answers]
    except Exception:
        return []


def resolve_txt(domain):
    """Resolve TXT records using dns.resolver."""
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "TXT")
        return [str(r) for r in answers]
    except Exception:
        return []


def dns_lookup(domain):
    basic = resolve_basic(domain)
    mx = resolve_mx(domain)
    ns = resolve_ns(domain)
    cname = resolve_cname(domain)
    txt = resolve_txt(domain)

    result = {
        "domain": domain,
        "A": basic.get("A", []),
        "AAAA": basic.get("AAAA", []),
        "MX": mx,
        "NS": ns,
        "CNAME": cname,
        "TXT": txt,
    }

    print(f"DNS Lookup Results for: {domain}")
    print("=" * 40)
    for rtype in ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]:
        records = result[rtype]
        if records:
            print(f"\n{rtype} Records:")
            for r in records:
                if isinstance(r, dict):
                    print(f"  {r['priority']} {r['host']}")
                else:
                    print(f"  {r}")
        else:
            print(f"\n{rtype} Records: (none)")

    print("\n" + "=" * 40)
    print("\nJSON Output:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform DNS lookup for a domain")
    parser.add_argument("domain", help="Domain name to look up")
    args = parser.parse_args()
    dns_lookup(args.domain)
