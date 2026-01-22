#!/usr/bin/env python3
"""
Greenhouse Job Board API Search

Directly query company job boards hosted on Greenhouse.
No authentication required for public job listings.

Usage:
    python greenhouse_search.py anthropic --keyword "engineer"
    python greenhouse_search.py stripe openai databricks --min-salary 200000
    python greenhouse_search.py --companies-file target_companies.txt
"""

import argparse
import json
import re
import sys
from typing import Optional
from urllib.parse import urljoin
import requests

# Known company board tokens (add more as discovered)
KNOWN_BOARDS = {
    # AI/ML
    "anthropic": "anthropic",
    "openai": "openai",
    "deepmind": "deepmind",
    "cohere": "cohere",
    "huggingface": "huggingface",
    "scale": "scaleai",
    "runway": "runwayml",
    "stability": "stability",
    "midjourney": "midjourney",
    "replicate": "replicate",

    # Big Tech
    "stripe": "stripe",
    "databricks": "databricks",
    "figma": "figma",
    "notion": "notion",
    "airtable": "airtable",
    "linear": "linear",
    "vercel": "vercel",
    "supabase": "supabase",
    "planetscale": "planetscale",

    # Biotech/Science
    "insitro": "insitro",
    "recursion": "recursionpharma",
    "tempus": "tempus",
    "grail": "grail",
    "color": "color",
    "benchling": "benchling",

    # CZ Initiative / Biohub
    "chanzuckerberg": "chanzuckerberginitiative",
    "czi": "chanzuckerberginitiative",
    "biohub": "biohub",
    "czbiohub": "biohub",
}


def get_board_token(company: str) -> str:
    """Get Greenhouse board token for a company."""
    company_lower = company.lower().replace(" ", "").replace("-", "")
    return KNOWN_BOARDS.get(company_lower, company_lower)


def fetch_greenhouse_jobs(board_token: str, content: bool = True) -> dict:
    """
    Fetch all jobs from a Greenhouse job board.

    Args:
        board_token: Company's Greenhouse board identifier
        content: Include full job descriptions

    Returns:
        Dict with 'jobs' list and metadata
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    params = {"content": "true"} if content else {}

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": f"Board '{board_token}' not found", "jobs": []}
        raise
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "jobs": []}


def extract_salary_from_description(description: str) -> tuple[Optional[int], Optional[int]]:
    """
    Extract salary range from job description text.

    Returns (min_salary, max_salary) or (None, None) if not found.
    """
    if not description:
        return None, None

    # Common patterns: "$150,000 - $200,000", "$150k-200k", "150,000 to 200,000"
    patterns = [
        r'\$?([\d,]+)k?\s*[-–to]+\s*\$?([\d,]+)k?(?:\s*(?:USD|usd|per year|annually|/yr|/year))?',
        r'salary[:\s]+\$?([\d,]+)k?\s*[-–to]+\s*\$?([\d,]+)k?',
        r'compensation[:\s]+\$?([\d,]+)k?\s*[-–to]+\s*\$?([\d,]+)k?',
    ]

    for pattern in patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            min_str = match.group(1).replace(",", "")
            max_str = match.group(2).replace(",", "")

            min_val = int(min_str)
            max_val = int(max_str)

            # Handle "k" notation (150 -> 150000)
            if min_val < 1000:
                min_val *= 1000
            if max_val < 1000:
                max_val *= 1000

            return min_val, max_val

    return None, None


def filter_jobs(
    jobs: list,
    keyword: str = None,
    min_salary: int = None,
    location: str = None,
    department: str = None,
) -> list:
    """Filter jobs by various criteria."""
    filtered = []

    for job in jobs:
        # Keyword filter (title or description)
        if keyword:
            keyword_lower = keyword.lower()
            title = job.get("title", "").lower()
            description = job.get("content", "").lower() if job.get("content") else ""
            if keyword_lower not in title and keyword_lower not in description:
                continue

        # Location filter
        if location:
            job_location = job.get("location", {}).get("name", "").lower()
            if location.lower() not in job_location:
                continue

        # Department filter
        if department:
            job_depts = [d.get("name", "").lower() for d in job.get("departments", [])]
            if not any(department.lower() in d for d in job_depts):
                continue

        # Salary filter (extract from description)
        if min_salary:
            description = job.get("content", "")
            min_sal, max_sal = extract_salary_from_description(description)
            if min_sal and min_sal < min_salary:
                continue
            # If no salary info found, include the job (don't filter out)

        filtered.append(job)

    return filtered


def format_job(job: dict, company: str, verbose: bool = False) -> str:
    """Format a single job for display."""
    lines = []

    title = job.get("title", "Unknown")
    location = job.get("location", {}).get("name", "Unknown Location")
    url = job.get("absolute_url", "")
    departments = [d.get("name") for d in job.get("departments", [])]

    lines.append(f"\n[GREENHOUSE] {title}")
    lines.append(f"  Company: {company}")
    lines.append(f"  Location: {location}")
    if departments:
        lines.append(f"  Department: {', '.join(departments)}")

    # Try to extract salary
    description = job.get("content", "")
    min_sal, max_sal = extract_salary_from_description(description)
    if min_sal and max_sal:
        lines.append(f"  Salary: ${min_sal:,} - ${max_sal:,}")

    lines.append(f"  URL: {url}")

    if verbose and description:
        # Strip HTML and truncate
        clean_desc = re.sub(r'<[^>]+>', ' ', description)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        if len(clean_desc) > 300:
            clean_desc = clean_desc[:300] + "..."
        lines.append(f"  Description: {clean_desc}")

    lines.append("-" * 40)
    return "\n".join(lines)


def search_companies(
    companies: list[str],
    keyword: str = None,
    min_salary: int = None,
    location: str = None,
    verbose: bool = False,
) -> tuple[list, list]:
    """
    Search multiple companies for matching jobs.

    Returns (all_jobs, output_lines)
    """
    all_jobs = []
    output_lines = []

    for company in companies:
        board_token = get_board_token(company)
        output_lines.append(f"\nSearching {company} (board: {board_token})...")

        data = fetch_greenhouse_jobs(board_token)

        if data.get("error"):
            output_lines.append(f"  Error: {data['error']}")
            continue

        jobs = data.get("jobs", [])
        output_lines.append(f"  Found {len(jobs)} total jobs")

        # Apply filters
        filtered = filter_jobs(jobs, keyword=keyword, min_salary=min_salary, location=location)

        if keyword or min_salary or location:
            output_lines.append(f"  {len(filtered)} jobs match filters")

        for job in filtered:
            job["_company"] = company  # Tag with company name
            all_jobs.append(job)
            output_lines.append(format_job(job, company, verbose=verbose))

    return all_jobs, output_lines


def main():
    parser = argparse.ArgumentParser(description="Search Greenhouse job boards directly")
    parser.add_argument("companies", nargs="*", help="Company names or board tokens to search")
    parser.add_argument("--companies-file", "-f", help="File with company names (one per line)")
    parser.add_argument("--keyword", "-k", help="Keyword to filter by (searches title and description)")
    parser.add_argument("--min-salary", "-s", type=int, help="Minimum salary filter")
    parser.add_argument("--location", "-l", help="Location filter")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show descriptions")
    parser.add_argument("--list-known", action="store_true", help="List known company board tokens")

    args = parser.parse_args()

    if args.list_known:
        print("Known Greenhouse board tokens:")
        for name, token in sorted(KNOWN_BOARDS.items()):
            print(f"  {name}: {token}")
        return

    # Gather company list
    companies = list(args.companies) if args.companies else []

    if args.companies_file:
        with open(args.companies_file) as f:
            companies.extend(line.strip() for line in f if line.strip())

    if not companies:
        parser.error("Provide company names or --companies-file")

    # Search
    all_jobs, output_lines = search_companies(
        companies,
        keyword=args.keyword,
        min_salary=args.min_salary,
        location=args.location,
        verbose=args.verbose,
    )

    # Print output
    print("\n".join(output_lines))
    print(f"\n{'=' * 80}")
    print(f"Total: {len(all_jobs)} matching jobs across {len(companies)} companies")

    # Save if requested
    if args.output and all_jobs:
        with open(args.output, 'w') as f:
            json.dump(all_jobs, f, indent=2, default=str)
        print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
