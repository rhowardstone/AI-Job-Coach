#!/usr/bin/env python3
"""
Job Search Script - Bulk search across multiple job boards

Uses JobSpy library to search Indeed, LinkedIn, Glassdoor, Google, ZipRecruiter

Usage:
    python job_search.py "software engineer" --location "San Francisco, CA" --min-salary 150000
    python job_search.py "ML engineer" --remote --hours 72
    python job_search.py --config ../profile.json  # Use profile for search terms
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from jobspy import scrape_jobs
    import pandas as pd
except ImportError:
    print("Required packages not installed. Run:")
    print("  pip install python-jobspy pandas")
    sys.exit(1)


def load_profile(profile_path: str) -> dict:
    """Load user profile for search parameters."""
    with open(profile_path) as f:
        return json.load(f)


def search_jobs(
    search_term: str,
    location: str = None,
    remote: bool = False,
    min_salary: int = None,
    hours_old: int = 72,
    results_per_site: int = 25,
    sites: list = None,
) -> pd.DataFrame:
    """
    Search for jobs across multiple boards.

    Returns DataFrame with columns:
    - site, title, company, location, job_url, description
    - date_posted, job_type, salary_min, salary_max, salary_currency
    """
    if sites is None:
        sites = ["indeed", "linkedin", "glassdoor", "google", "zip_recruiter"]

    print(f"Searching for '{search_term}'...")
    if location:
        print(f"  Location: {location}")
    if remote:
        print(f"  Remote: Yes")
    if min_salary:
        print(f"  Min salary: ${min_salary:,}")
    print(f"  Sites: {', '.join(sites)}")
    print(f"  Posted within: {hours_old} hours")
    print()

    try:
        jobs = scrape_jobs(
            site_name=sites,
            search_term=search_term,
            location=location or "",
            is_remote=remote,
            results_wanted=results_per_site,
            hours_old=hours_old,
            country_indeed='USA',
            enforce_annual_salary=True,  # Normalize all salaries to annual
        )
    except Exception as e:
        print(f"Error during search: {e}")
        return pd.DataFrame()

    # Filter by minimum salary if specified
    if min_salary and 'min_amount' in jobs.columns:
        before = len(jobs)
        jobs = jobs[
            (jobs['min_amount'].isna()) |  # Keep jobs without salary info
            (jobs['min_amount'] >= min_salary)
        ]
        after = len(jobs)
        if before != after:
            print(f"Filtered {before - after} jobs below ${min_salary:,} salary")

    return jobs


def format_results(jobs: pd.DataFrame, verbose: bool = False) -> str:
    """Format job results for display."""
    if jobs.empty:
        return "No jobs found matching criteria."

    lines = [f"Found {len(jobs)} jobs:\n"]
    lines.append("=" * 80)

    for idx, job in jobs.iterrows():
        title = job.get('title', 'Unknown Title')
        company = job.get('company', 'Unknown Company')
        location = job.get('location', '')
        url = job.get('job_url', '')
        site = job.get('site', '')

        # Format salary if available
        salary_str = ""
        min_sal = job.get('min_amount')
        max_sal = job.get('max_amount')
        if pd.notna(min_sal) or pd.notna(max_sal):
            if pd.notna(min_sal) and pd.notna(max_sal):
                salary_str = f"${int(min_sal):,} - ${int(max_sal):,}"
            elif pd.notna(min_sal):
                salary_str = f"${int(min_sal):,}+"
            else:
                salary_str = f"Up to ${int(max_sal):,}"

        lines.append(f"\n[{site.upper()}] {title}")
        lines.append(f"  Company: {company}")
        if location:
            lines.append(f"  Location: {location}")
        if salary_str:
            lines.append(f"  Salary: {salary_str}")
        lines.append(f"  URL: {url}")

        if verbose and job.get('description'):
            desc = str(job['description'])[:300] + "..." if len(str(job.get('description', ''))) > 300 else job.get('description', '')
            lines.append(f"  Description: {desc}")

        lines.append("-" * 40)

    return "\n".join(lines)


def save_results(jobs: pd.DataFrame, output_path: str):
    """Save results to CSV and JSON."""
    if jobs.empty:
        print("No results to save.")
        return

    # Save CSV
    csv_path = output_path.replace('.json', '.csv')
    jobs.to_csv(csv_path, index=False)
    print(f"Saved CSV: {csv_path}")

    # Save JSON (more detailed)
    json_path = output_path if output_path.endswith('.json') else output_path + '.json'
    jobs.to_json(json_path, orient='records', indent=2)
    print(f"Saved JSON: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Search for jobs across multiple boards")
    parser.add_argument("search_term", nargs="?", help="Job title or keywords to search")
    parser.add_argument("--location", "-l", help="Location to search (city, state)")
    parser.add_argument("--remote", "-r", action="store_true", help="Search for remote jobs only")
    parser.add_argument("--min-salary", "-s", type=int, help="Minimum salary filter")
    parser.add_argument("--hours", type=int, default=72, help="Jobs posted within N hours (default: 72)")
    parser.add_argument("--results", "-n", type=int, default=25, help="Results per site (default: 25)")
    parser.add_argument("--sites", nargs="+", help="Sites to search (indeed, linkedin, glassdoor, google, zip_recruiter)")
    parser.add_argument("--config", "-c", help="Path to profile.json for search parameters")
    parser.add_argument("--output", "-o", help="Output file path (saves CSV and JSON)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show job descriptions")

    args = parser.parse_args()

    # Load from config if provided
    search_term = args.search_term
    location = args.location
    min_salary = args.min_salary

    if args.config:
        profile = load_profile(args.config)
        job_search = profile.get('job_search', {})
        if not search_term and job_search.get('target_titles'):
            search_term = " OR ".join(job_search['target_titles'])
        if not location and job_search.get('preferred_locations'):
            location = job_search['preferred_locations'][0]
        if not min_salary:
            min_salary = job_search.get('min_salary')

    if not search_term:
        parser.error("search_term is required (or provide --config with target_titles)")

    # Run search
    jobs = search_jobs(
        search_term=search_term,
        location=location,
        remote=args.remote,
        min_salary=min_salary,
        hours_old=args.hours,
        results_per_site=args.results,
        sites=args.sites,
    )

    # Display results
    print(format_results(jobs, verbose=args.verbose))

    # Save if output specified
    if args.output:
        save_results(jobs, args.output)
    elif not jobs.empty:
        # Default output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_output = f"job_search_{timestamp}.json"
        save_results(jobs, default_output)


if __name__ == "__main__":
    main()
