#!/usr/bin/env python3
"""
md5_cracker.py — εκπαιδευτικό demo dictionary attack για MD5.
Χρήση μόνο σε hashes που σου ανήκουν ή έχεις ρητή άδεια να δοκιμάσεις.

Usage:
  python3 md5_cracker.py --hash <md5hex> --wordlist /path/to/wordlist.txt
"""
import argparse, hashlib, sys

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser(description="MD5 dictionary cracker (demo)")
    ap.add_argument("--hash", required=True, help="MD5 hash (32-hex)")
    ap.add_argument("--wordlist", required=True, help="Path σε wordlist (π.χ. rockyou.txt)")
    ap.add_argument("--progress", type=int, default=100000, help="Εμφάνιση προόδου κάθε Ν λέξεις (default 100000)")
    args = ap.parse_args()

    target = args.hash.strip().lower()
    if len(target) != 32 or any(c not in "0123456789abcdef" for c in target):
        print("Λάθος μορφή MD5 (πρέπει να είναι 32-hex).", file=sys.stderr); sys.exit(2)

    try:
        with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for i, word in enumerate(f, 1):
                cand = word.rstrip("\r\n")
                if md5_hex(cand) == target:
                    print(f"[+] Βρέθηκε: '{cand}'")
                    return
                if args.progress and i % args.progress == 0:
                    print(f"[i] Ελέγχθηκαν {i} λέξεις...", file=sys.stderr)
    except FileNotFoundError:
        print("Δεν βρέθηκε το wordlist.", file=sys.stderr); sys.exit(2)
    print("[-] Δεν βρέθηκε αντιστοιχία.")

if __name__ == "__main__":
    main()
