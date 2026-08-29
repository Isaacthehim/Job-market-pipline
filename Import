import json
import pyodbc

# ===== TANZIMAT =====
JSON_FILE = r"C:\Users\***"
SERVER = 'DESKTOP-PNBJ451'
DATABASE = 'Job_EN'   # ya Jobs_EN

CONN_STR = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

conn = pyodbc.connect(CONN_STR)
cursor = conn.cursor()

# ===== KHAANDAN JSON =====
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    jobs_list = json.load(f)

# ===== INSERT UNIQUE COMPANIES =====
companies_seen = set()
companies_inserted = 0
for job in jobs_list:
    comp = job.get('company')
    if not comp:
        continue
    cid = comp['id']
    if cid not in companies_seen:
        companies_seen.add(cid)
        name_en = comp.get('nameEn')
        if name_en == '':
            name_en = None
        cursor.execute("""
            INSERT INTO Company (CompanyID, Name, Is_Employer_Responsive, Famous, Is_Governmental_Company, Company_Score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cid,
            name_en,
            comp.get('isEmployerResponsive'),
            comp.get('isFamous'),
            comp.get('isGovernmentalCompany'),
            comp.get('companyScore')
        ))
        companies_inserted += 1
conn.commit()
print(f'{companies_inserted} unique companies inserted into Company.')

# ===== INSERT JOB POSTS =====
batch_size = 200
job_count = 0

for job in jobs_list:
    loc = job.get('location') or {}
    country = loc.get('country') or {}
    province = loc.get('province') or {}
    city = loc.get('city') or {}
    region = loc.get('region') or {}

    props = job.get('properties', {})
    gen = job.get('gender') or {}
    ind = job.get('industry') or {}
    wt = job.get('workType') or {}
    sl = job.get('seniorityLevel') or {}
    sal = job.get('salary') or {}
    first = job.get('firstActivationTime') or {}
    act = job.get('activationTime') or {}
    exp = job.get('expireTime') or {}

    title_val = job.get('title')
    company_id = job['company']['id'] if job.get('company') else None
    job_id = job['id']

    cursor.execute("""
        INSERT INTO JobPost (
            JobID, Title, Score, CompanyID,
            Country, Province, City, Neighborhood, CitySize, CitySizeGroupID,
            Is_Internship, Is_Remote, Is_Urgent, RequiredExperienceYears,
            Suitable_For_Disabled, Salary_Can_Be_Shown,
            Gender, Industry, WorkType, Seniority_Level,
            Salary_Text, Min_Salary, Max_Salary,
            FirstActivation_Text, FirstActivation_Date,
            Activation_Text, Activation_Date,
            Expire_Text, Expire_Date
        ) OUTPUT INSERTED.PostID
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        job_id,
        title_val,
        job.get('score'),
        company_id,
        country.get('titleEn'),
        province.get('titleEn'),
        city.get('titleEn'),
        region.get('titleEn'),
        city.get('citySize'),
        city.get('citySizeGroupId'),
        props.get('isInternship'),
        props.get('isRemote'),
        props.get('isUrgent'),
        props.get('requiredRelatedExperienceYears'),
        props.get('suitableForDisabled'),
        props.get('salaryCanBeShown'),
        gen.get('titleEn'),
        ind.get('titleEn'),
        wt.get('titleEn'),
        sl.get('titleEn'),
        sal.get('titleEn'),
        sal.get('min'),
        sal.get('max'),
        first.get('beautifyEn'),
        first.get('date'),
        act.get('beautifyEn'),
        act.get('date'),
        exp.get('beautifyEn'),
        exp.get('date')
    ))

    new_post_id = cursor.fetchone()[0]

    for b in job.get('benefits', []):
        benefit_en = b.get('titleEn')
        if benefit_en and benefit_en != '':
            cursor.execute("INSERT INTO Benefits (PostID, Benefit) VALUES (?, ?)", (new_post_id, benefit_en))

    for cat in job.get('jobCategories', []):
        cat_en = cat.get('titleEn')
        if cat_en and cat_en != '':
            cursor.execute("INSERT INTO Job_Category (PostID, Category) VALUES (?, ?)", (new_post_id, cat_en))

    job_count += 1
    if job_count % batch_size == 0:
        conn.commit()
        print(f'{job_count} jobs inserted...')

conn.commit()
cursor.close()
conn.close()
print(f'=== Done! Total jobs imported into {DATABASE}: {job_count} ===')