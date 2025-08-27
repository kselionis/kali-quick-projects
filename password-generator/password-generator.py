#!/usr/bin/env python3
import argparse, secrets, string, sys

AMBIGUOUS = "O0Il1|{}[]()<>`'\"\\/"

def build_charset(include_lower, include_upper, include_digits, include_symbols, no_ambiguous):
    charset = ""
    if include_lower: charset += string.ascii_lowercase
    if include_upper: charset += string.ascii_uppercase
    if include_digits: charset += string.digits
    if include_symbols: charset += "!@#$%^&*_-+=:;.,?"
    if no_ambiguous:
        charset = "".join(ch for ch in charset if ch not in AMBIGUOUS)
    return charset

def main():
    ap = argparse.ArgumentParser(description="Strong password generator")
    ap.add_argument("--length", "-l", type=int, default=16)
    ap.add_argument("--count", "-c", type=int, default=1)
    ap.add_argument("--no-lower", action="store_true")
    ap.add_argument("--no-upper", action="store_true")
    ap.add_argument("--no-digits", action="store_true")
    ap.add_argument("--no-symbols", action="store_true")
    ap.add_argument("--no-ambiguous", action="store_true")
    args = ap.parse_args()

    charset = build_charset(not args.no_lower, not args.no_upper, not args.no_digits, not args.no_symbols, args.no_ambiguous)
    if not charset:
        print("Error: empty charset.", file=sys.stderr); sys.exit(2)
    if args.length <= 0 or args.count <= 0:
        print("Error: positive length/count required.", file=sys.stderr); sys.exit(2)

    for _ in range(args.count):
        print("".join(secrets.choice(charset) for _ in range(args.length)))

if __name__ == "__main__":
    main()
