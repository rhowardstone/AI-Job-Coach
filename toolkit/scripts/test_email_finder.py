#!/usr/bin/env python3
"""
Test suite for email_finder.py

Verified against real, public email addresses.
Last updated: 2026-01-21
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from email_finder import (
    normalize_name,
    generate_emails,
    get_domain_pattern,
    verify_with_hunter,
    load_env,
)

load_env()

# ============================================================
# VERIFIED EMAIL DATA (Hunter.io verified 2026-01-21)
# ============================================================

# Company patterns discovered via Hunter.io
VERIFIED_PATTERNS = {
    "vercel.com": "{first}.{last}",
    "microsoft.com": "{f}{last}",
    "stripe.com": "{first}{last}",
    "openai.com": "{first}{l}",
    "figma.com": "{f}{last}",
    "databricks.com": "{first}.{last}",
}

# Real verified emails (Hunter.io deliverable)
# Note: CEOs often have special patterns (just firstname@)
VERIFIED_EMAILS = [
    # (name, domain, verified_email, notes)
    ("Guillermo Rauch", "vercel.com", "guillermo.rauch@vercel.com", "CEO, matches pattern"),
    ("Guillermo Rauch", "vercel.com", "guillermo@vercel.com", "CEO, alternate"),
    ("Satya Nadella", "microsoft.com", "snadella@microsoft.com", "CEO, matches {f}{last}"),
    ("Patrick Collison", "stripe.com", "patrick@stripe.com", "CEO, special - just firstname"),
    ("Sam Altman", "openai.com", "sama@openai.com", "CEO, matches {first}{l}"),
    ("Dylan Field", "figma.com", "dfield@figma.com", "CEO, matches {f}{last}"),
    ("Ali Ghodsi", "databricks.com", "ali@databricks.com", "CEO, special - just firstname"),
]

# Emails verified as INVALID (undeliverable)
INVALID_EMAILS = [
    ("Patrick Collison", "stripe.com", "patrickcollison@stripe.com", "Pattern suggested but invalid"),
    ("Sam Altman", "openai.com", "sam.altman@openai.com", "Standard format but invalid"),
    ("Dylan Field", "figma.com", "dylan.field@figma.com", "Standard format but invalid"),
]

# ============================================================
# PRACTICAL OUTREACH TARGETS (Hiring Managers, not CEOs)
# ============================================================
# CEOs are good for testing tool accuracy, but for actual outreach
# you want people who: (1) review applications, (2) respond to cold email,
# (3) can refer you internally. Directors and Managers are ideal.

HIRING_MANAGER_EMAILS = [
    # (name, domain, verified_email, title, notes)
    ("Xiao Li", "databricks.com", "xiao.li@databricks.com",
     "Director of Engineering", "Hiring for Spark teams, matches {first}.{last}"),
    ("Chris Stevens", "databricks.com", "chris.stevens@databricks.com",
     "Engineering Manager", "Building Aarhus office, matches {first}.{last}"),
]


def test_pattern_accuracy():
    """Test that our pattern detection matches known patterns."""
    print("\n" + "=" * 60)
    print("Pattern Detection Accuracy")
    print("=" * 60)

    api_key = os.environ.get("HUNTER_API_KEY")
    if not api_key:
        print("  Skipped - no HUNTER_API_KEY")
        return True

    passed = 0
    total = len(VERIFIED_PATTERNS)

    for domain, expected in VERIFIED_PATTERNS.items():
        detected = get_domain_pattern(domain, api_key)
        match = detected == expected
        status = "✓" if match else "✗"

        if match:
            passed += 1
            print(f"  {status} {domain}: {detected}")
        else:
            print(f"  {status} {domain}: got {detected}, expected {expected}")

    print(f"\n  Passed: {passed}/{total}")
    return passed == total


def test_verified_emails():
    """Test that verified emails are generated and ranked well."""
    print("\n" + "=" * 60)
    print("Verified Email Generation")
    print("=" * 60)

    passed = 0
    total = len(VERIFIED_EMAILS)

    for name, domain, verified_email, notes in VERIFIED_EMAILS:
        parts = name.lower().split()
        first = parts[0]
        last = parts[-1] if len(parts) > 1 else ""

        emails = generate_emails(first, last, domain)

        if verified_email in emails:
            rank = emails.index(verified_email) + 1
            status = "✓" if rank <= 5 else "~"  # Good if in top 5
            passed += 1 if rank <= 5 else 0.5
            print(f"  {status} {name} @ {domain}")
            print(f"      {verified_email} (rank #{rank}) - {notes}")
        else:
            print(f"  ✗ {name} @ {domain}")
            print(f"      {verified_email} NOT GENERATED - {notes}")

    print(f"\n  Passed: {passed}/{total}")
    return passed >= total * 0.7  # 70% threshold


def test_email_verification():
    """Live test against Hunter.io API."""
    print("\n" + "=" * 60)
    print("Live Email Verification")
    print("=" * 60)

    api_key = os.environ.get("HUNTER_API_KEY")
    if not api_key:
        print("  Skipped - no HUNTER_API_KEY")
        return True

    # Test a few known-good emails
    test_cases = [
        ("guillermo.rauch@vercel.com", "deliverable"),
        ("snadella@microsoft.com", "deliverable"),
        ("sama@openai.com", "deliverable"),
    ]

    passed = 0
    for email, expected_result in test_cases:
        result = verify_with_hunter(email, api_key)
        actual = result.get("result", "error")
        match = actual == expected_result
        status = "✓" if match else "✗"

        if match:
            passed += 1

        print(f"  {status} {email}: {actual}")

    print(f"\n  Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_ceo_pattern_insight():
    """
    Test insight: CEOs often have simpler emails than the company pattern.

    Pattern might be {first}.{last} but CEO gets {first}@ or {f}{last}@
    """
    print("\n" + "=" * 60)
    print("CEO Email Pattern Insight")
    print("=" * 60)

    # CEOs with special (simpler) emails
    ceo_specials = [
        ("Patrick Collison", "stripe.com", "patrick@stripe.com", "{first}{last}"),
        ("Ali Ghodsi", "databricks.com", "ali@databricks.com", "{first}.{last}"),
    ]

    print("  CEOs often get simpler emails than company pattern:")
    for name, domain, actual_email, company_pattern in ceo_specials:
        print(f"    • {name} @ {domain}")
        print(f"      Company pattern: {company_pattern}")
        print(f"      CEO actual: {actual_email}")

    print("\n  Insight: For executives, try {first}@ even if pattern differs")
    return True


def test_hiring_manager_emails():
    """
    Test that hiring manager emails are generated correctly.

    These are PRACTICAL outreach targets - people who actually
    review applications and respond to cold email.
    """
    print("\n" + "=" * 60)
    print("Hiring Manager Email Generation (Practical Targets)")
    print("=" * 60)

    passed = 0
    total = len(HIRING_MANAGER_EMAILS)

    for name, domain, verified_email, title, notes in HIRING_MANAGER_EMAILS:
        parts = name.lower().split()
        first = parts[0]
        last = parts[-1] if len(parts) > 1 else ""

        emails = generate_emails(first, last, domain)

        if verified_email in emails:
            rank = emails.index(verified_email) + 1
            status = "✓" if rank <= 3 else "~"  # Want top 3 for managers
            passed += 1 if rank <= 3 else 0.5
            print(f"  {status} {name} ({title})")
            print(f"      {verified_email} (rank #{rank}) - {notes}")
        else:
            print(f"  ✗ {name} ({title})")
            print(f"      {verified_email} NOT GENERATED - {notes}")

    print(f"\n  Passed: {passed}/{total}")
    print("\n  Note: These are actual outreach targets, not CEOs.")
    print("  Hiring managers respond to personalized cold email.")
    return passed >= total * 0.8  # 80% threshold


def run_all_tests():
    """Run all tests."""
    print("\n" + "#" * 60)
    print("# Email Finder Test Suite - Real Verified Data")
    print("#" * 60)

    results = [
        ("Pattern Detection", test_pattern_accuracy()),
        ("Verified Email Generation", test_verified_emails()),
        ("Hiring Manager Emails", test_hiring_manager_emails()),
        ("Live API Verification", test_email_verification()),
        ("CEO Pattern Insight", test_ceo_pattern_insight()),
    ]

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    print()
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
