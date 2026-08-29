import requests
import json
import csv
import time

# ============== CONFIG ==============
URL = "https://candidateapi.jobvision.ir/api/v1/JobPost/List"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": " Bearer Token x) ",
    "clientid": " x) ",
    "content-type": "application/json",
    "origin": "https://jobvision.ir",
    "referer": "https://jobvision.ir/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "web-app-version": "19.0.121",
}
PAGE_SIZE = 30
DELAY_BETWEEN_PAGES = 3 

# ============== FETCH ALL PAGES ==============
all_jobs = []
current_page = 1
total_pages = None

while True:
    payload = {
        "pageSize": PAGE_SIZE,
        "requestedPage": current_page,
        "sortBy": 1,                
        "searchId": None
    }

    print(f"Fetching page {current_page}...")
    try:
        resp = requests.post(URL, headers=HEADERS, json=payload, timeout=20)
        resp.raise_for_status()
        page_data = resp.json()
    except Exception as e:
        print(f"Error on page {current_page}: {e}")
        break

    inner = page_data.get("data", {})
    jobs_on_page = inner.get("jobPosts", [])

    if total_pages is None:
        job_count = inner.get("jobPostCount", 0)
        total_pages = (job_count + PAGE_SIZE - 1) // PAGE_SIZE
        print(f"Total jobs: {job_count}, Total pages: {total_pages}")

    all_jobs.extend(jobs_on_page)
    print(f"  Collected {len(jobs_on_page)} jobs. Total so far: {len(all_jobs)}")

    # Stop if no more jobs
    if len(jobs_on_page) == 0:
        print("No more jobs, stopping.")
        break
    if current_page >= total_pages:
        print("Reached last page.")
        break

    current_page += 1
    time.sleep(DELAY_BETWEEN_PAGES)

# ============== SAVE TO JSON (optional) ==============
with open("jobvision_all_jobs.json", "w", encoding="utf-8") as jf:
    json.dump(all_jobs, jf, ensure_ascii=False, indent=2)
print(f"JSON saved with {len(all_jobs)} jobs.")

# ============== SAVE TO CSV ==============
csv_file = "jobvision_all_jobs.csv"
with open(csv_file, "w", encoding="utf-8-sig", newline="") as cf:
    writer = csv.writer(cf)
    writer.writerow([
        "id",
        "title",
        "company_name",
        "location",
        "work_type",
        "seniority_level",
        "salary",
        "industry",
        "activation_time",
        "url"
    ])

    for job in all_jobs:
        jid = job.get("id", "")
        title = job.get("title", "")
        company = (job.get("company") or {}).get("nameFa", "")
        location = (job.get("location") or {}).get("titleFa", "")
        work_type = job.get("workType", "")
        seniority = job.get("seniorityLevel", "")
        salary = job.get("salary", "")  # may be a dict; convert if needed
        industry = (job.get("industry") or {}).get("titleFa", "")
        activation = job.get("activationTime", "")
        url = f"https://jobvision.ir/job/{jid}" if jid else ""

        # format e salary 
        if isinstance(salary, dict):
            salary = f"{salary.get('from','')}-{salary.get('to','')} {salary.get('unit','')}"

        writer.writerow([jid, title, company, location, work_type, seniority, salary, industry, activation, url])

print(f"CSV saved to {csv_file} with {len(all_jobs)} rows.")