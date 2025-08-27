#!/usr/bin/env python3
"""
scanner.py - minimal concurrent TCP port scanner

Usage:
  python3 scanner.py --host example.com --common
  python3 scanner.py --host 127.0.0.1 --ports 1-1024,8080-8090
"""
import argparse, socket, concurrent.futures, sys

COMMON_PORTS = [21,22,23,25,53,80,110,139,143,443,445,3306,3389,8080,8443]

def scan_port(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except Exception:
        return port, False

def parse_ports(spec):
    ports = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk: 
            continue
        if "-" in chunk:
            start, end = chunk.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(chunk))
    return sorted(p for p in ports if 1 <= p <= 65535)

def main():
    ap = argparse.ArgumentParser(description="Tiny TCP port scanner (educational). Scan only with permission.")
    ap.add_argument("--host", required=True, help="Target hostname or IP")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--ports", help="List/ranges: e.g. 1-1024,8080,8443")
    group.add_argument("--common", action="store_true", help="Scan common ports")
    ap.add_argument("--timeout", type=float, default=1.0, help="Timeout seconds per port (default 1.0)")
    ap.add_argument("--workers", type=int, default=200, help="Thread pool size")
    args = ap.parse_args()

    ports = COMMON_PORTS if args.common else parse_ports(args.ports)
    if not ports:
        print("No valid ports provided.", file=sys.stderr); sys.exit(2)

    print(f"Scanning {args.host} on {len(ports)} ports...")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(scan_port, args.host, p, args.timeout) for p in ports]
        for fut in concurrent.futures.as_completed(futures):
            port, is_open = fut.result()
            if is_open:
                open_ports.append(port)
                print(f"[+] {port}/tcp open")

    if open_ports:
        print("Open ports:", ", ".join(map(str, sorted(open_ports))))
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
