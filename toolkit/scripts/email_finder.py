#!/usr/bin/env python3
"""
Email Pattern Finder

Given a name and company domain, generates likely email addresses
and optionally verifies them via Hunter.io API.

Usage:
    python email_finder.py "John Smith" company.com
    python email_finder.py "Jane Doe" anthropic.com --verify
    python email_finder.py --domain stripe.com --pattern  # Just show pattern
"""

import argparse
import os
import re
import json
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Required: pip install requests")
    sys.exit(1)


def load_env():
    """Load environment variables from .env file if it exists."""
    env_paths = [
        Path(__file__).parent.parent / ".env",  # toolkit/.env
        Path(__file__).parent / ".env",          # scripts/.env
        Path.cwd() / ".env",                     # current directory
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())
            break


# Load .env on import
load_env()


# Common email patterns (ordered by frequency)
PATTERNS = [
    "{first}.{last}",      # john.smith@
    "{first}{last}",       # johnsmith@
    "{first}",             # john@
    "{f}{last}",           # jsmith@
    "{first}{l}",          # johns@ (OpenAI pattern)
    "{first}_{last}",      # john_smith@
    "{last}.{first}",      # smith.john@
    "{f}.{last}",          # j.smith@
    "{first}.{l}",         # john.s@
    "{last}",              # smith@
    "{first}-{last}",      # john-smith@
]


def normalize_name(name: str) -> tuple[str, str]:
    """Extract first and last name, handle edge cases."""
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0].lower(), ""
    # Handle "Dr. John Smith" or "John Smith Jr."
    # Take first non-title and last non-suffix
    titles = {"dr", "mr", "ms", "mrs", "prof"}
    suffixes = {"jr", "sr", "ii", "iii", "iv", "phd", "md"}

    clean_parts = [p for p in parts if p.lower().rstrip(".") not in titles
                   and p.lower().rstrip(".") not in suffixes]

    if len(clean_parts) >= 2:
        return clean_parts[0].lower(), clean_parts[-1].lower()
    elif len(clean_parts) == 1:
        return clean_parts[0].lower(), ""
    else:
        return parts[0].lower(), parts[-1].lower()


def generate_emails(first: str, last: str, domain: str) -> list[str]:
    """Generate all likely email permutations."""
    if not first:
        return []

    emails = []
    f = first[0]  # First initial
    l = last[0] if last else ""  # Last initial

    for pattern in PATTERNS:
        try:
            email = pattern.format(
                first=first,
                last=last,
                f=f,
                l=l
            )
            # Skip patterns that need last name if we don't have one
            if not last and "{last}" in pattern:
                continue
            emails.append(f"{email}@{domain}")
        except (KeyError, IndexError):
            continue

    return emails


def verify_with_hunter(email: str, api_key: str) -> dict:
    """Verify email using Hunter.io API."""
    url = "https://api.hunter.io/v2/email-verifier"
    params = {"email": email, "api_key": api_key}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_domain_pattern(domain: str, api_key: str) -> Optional[str]:
    """Get email pattern for a domain using Hunter.io."""
    url = "https://api.hunter.io/v2/domain-search"
    params = {"domain": domain, "api_key": api_key}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", {})
        return data.get("pattern")
    except requests.exceptions.RequestException as e:
        return None


def format_output(name: str, domain: str, emails: list[str],
                  verified: dict = None, pattern: str = None) -> str:
    """Format results for display."""
    lines = [
        f"\n{'='*60}",
        f"Email Finder Results",
        f"{'='*60}",
        f"Name: {name}",
        f"Domain: {domain}",
    ]

    if pattern:
        lines.append(f"Known Pattern: {pattern}")

    lines.append(f"\nLikely Email Addresses (in order of probability):")
    lines.append("-" * 40)

    for i, email in enumerate(emails[:10], 1):
        status = ""
        if verified and email in verified:
            v = verified[email]
            if v.get("error"):
                status = f" [Error: {v['error']}]"
            elif v.get("result") == "deliverable":
                status = " ✓ VERIFIED"
            elif v.get("result") == "undeliverable":
                status = " ✗ Invalid"
            else:
                status = f" [{v.get('result', 'unknown')}]"

        lines.append(f"  {i}. {email}{status}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find email addresses for a person at a company")
    parser.add_argument("name", nargs="?", help="Person's full name (e.g., 'John Smith')")
    parser.add_argument("domain", nargs="?", help="Company domain (e.g., 'company.com')")
    parser.add_argument("--verify", "-v", action="store_true",
                        help="Verify emails with Hunter.io (requires HUNTER_API_KEY env var)")
    parser.add_argument("--pattern", "-p", action="store_true",
                        help="Look up domain's email pattern only (domain as first positional arg)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    # Get Hunter.io API key if needed
    api_key = os.environ.get("HUNTER_API_KEY")

    # For --pattern, use 'name' arg as domain if domain not provided
    if args.pattern and args.name and not args.domain:
        args.domain = args.name
        args.name = None

    if args.pattern and args.domain:
        if not api_key:
            print("Error: HUNTER_API_KEY environment variable required for --pattern")
            print("Get a free key at https://hunter.io/")
            sys.exit(1)

        pattern = get_domain_pattern(args.domain, api_key)
        if pattern:
            print(f"Email pattern for {args.domain}: {pattern}")
        else:
            print(f"Could not determine pattern for {args.domain}")
        return

    if not args.name or not args.domain:
        parser.error("name and domain are required")

    # Generate emails
    first, last = normalize_name(args.name)
    emails = generate_emails(first, last, args.domain)

    # Get pattern if API key available
    pattern = None
    if api_key:
        pattern = get_domain_pattern(args.domain, api_key)

        # If we know the pattern, prioritize that format
        if pattern:
            pattern_email = pattern.format(
                first=first, last=last, f=first[0], l=last[0] if last else ""
            ) + f"@{args.domain}"
            if pattern_email in emails:
                emails.remove(pattern_email)
            emails.insert(0, pattern_email)

    # Verify if requested
    verified = {}
    if args.verify:
        if not api_key:
            print("Error: HUNTER_API_KEY environment variable required for --verify")
            print("Get a free key at https://hunter.io/")
            sys.exit(1)

        print("Verifying emails (this may take a moment)...")
        # Only verify top 3 to conserve API calls
        for email in emails[:3]:
            verified[email] = verify_with_hunter(email, api_key)

    # Output
    if args.json:
        result = {
            "name": args.name,
            "domain": args.domain,
            "pattern": pattern,
            "emails": emails[:10],
            "verified": verified if verified else None
        }
        print(json.dumps(result, indent=2))
    else:
        print(format_output(args.name, args.domain, emails, verified, pattern))

        if not api_key:
            print("Tip: Set HUNTER_API_KEY for pattern detection and verification")
            print("     Get a free key at https://hunter.io/")


if __name__ == "__main__":
    main()
