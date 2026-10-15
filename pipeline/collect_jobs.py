import json
import os
import requests

# Companies to collect from (their Greenhouse board names)
COMPANIES = ["stripe", "affirm"]

# If a job's location contains any of these words, we treat it as Canadian
CANADA_WORDS = [
    "canada", "toronto", "vancouver", "montreal", "ottawa",
    "waterloo", "calgary", "edmonton", "windsor",
]


def fetch_jobs(company):
    """Ask Greenhouse for all of a company's jobs, with descriptions."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # stop with an error if the request failed
    return response.json()["jobs"]


def is_in_canada(location):
    """Return True if the location mentions a Canadian place."""
    location = location.lower()
    return any(word in location for word in CANADA_WORDS)


def clean_job(job, company):
    """Turn a messy job record into our own neat format."""
    return {
        "id": f"{company}-{job['id']}",
        "company": job.get("company_name") or company,
        "title": job.get("title", "").strip(),
        "location": job.get("location", {}).get("name", "").strip(),
        "url": job.get("absolute_url", ""),
        "updated_at": job.get("updated_at", ""),
        "description_html": job.get("content", ""),
    }


def main():
    all_jobs = []

    for company in COMPANIES:
        print(f"Fetching jobs from {company}...")
        try:
            jobs = fetch_jobs(company)
        except requests.RequestException as error:
            print(f"  Could not fetch {company}: {error}")
            continue  # skip this company, keep going with the rest

        canada_jobs = []
        for job in jobs:
            location = job.get("location", {}).get("name", "")
            if is_in_canada(location):
                canada_jobs.append(clean_job(job, company))

        print(f"  {len(jobs)} total jobs, {len(canada_jobs)} in Canada")
        all_jobs.extend(canada_jobs)

    # Save everything to a file
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.json", "w", encoding="utf-8") as file:
        json.dump(all_jobs, file, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(all_jobs)} Canadian jobs to data/jobs.json")


if __name__ == "__main__":
    main()