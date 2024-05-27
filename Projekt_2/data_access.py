import sqlite3
from job_info_model import JobInfoModel

def connect_to_db():
    connection = sqlite3.connect('offers.db')
    cursor = connection.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Company" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Name"	TEXT,
        PRIMARY KEY("ID" AUTOINCREMENT)
    )
''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Position" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Name"	TEXT,
        PRIMARY KEY("ID" AUTOINCREMENT)
    );
''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS "Skills" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"Name"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
         ''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Currency" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Name"	TEXT,
        PRIMARY KEY("ID" AUTOINCREMENT)
    );
''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "Source" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Name"	TEXT,
        PRIMARY KEY("ID" AUTOINCREMENT)
    );
''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS "Category" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Name"	TEXT,
        PRIMARY KEY("ID" AUTOINCREMENT)
    );
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Offers" (
        "ID"	INTEGER NOT NULL UNIQUE,
        "Position_ID"	INTEGER,
        "Company_ID"	INTEGER,
        "Category_ID"	INTEGER,
        "Currency_ID"	INTEGER,
        "Source_ID"	INTEGER,
        "Link"  TEXT,
        "Skills_IDs"    TEXT,
        "Seniority"	INTEGER,
        "Min_salary"	INTEGER,
        "Max_salary"	INTEGER,
        "Job_summary"	TEXT,
        "Address"	TEXT,
        FOREIGN KEY("Company_ID") REFERENCES "Company"("ID"),
        FOREIGN KEY("Category_ID") REFERENCES "Category"("ID"),
        FOREIGN KEY("Position_ID") REFERENCES "Position"("ID"),
        PRIMARY KEY("ID" AUTOINCREMENT),
        FOREIGN KEY("Currency_ID") REFERENCES "Currency"("ID"),
        FOREIGN KEY("Source_ID") REFERENCES "Source"("ID")
    );
''')
    connection.commit()
    return connection


def get_id(where_value, table_name, connection):
    cursor = connection.cursor()

    cursor.execute(f"SELECT ID FROM {table_name} WHERE Name = ?", (where_value,))
    position_id = cursor.fetchone()

    if position_id is None:
        cursor.execute(f"INSERT INTO {table_name} (Name) VALUES (?)", (where_value,))
        connection.commit()
        position_id = cursor.lastrowid
    else:
        position_id = position_id[0]
    return position_id


def get_skills_list(skills, connection):
    skills_ids = []
    for skill in skills:
        skill_id = get_id(skill, "Skills", connection)
        skills_ids.append(skill_id)
    return skills_ids


def save_offer_in_db(connection, offer):
    cursor = connection.cursor()
    position_id = get_id(offer.position, 'Position', connection)
    company_id = get_id(offer.company, 'Company', connection)
    category_id = get_id(offer.category, 'Category', connection)
    source_id = get_id(offer.source, 'Source', connection)
    currency_id = get_id(offer.currency, 'Currency', connection)
    skills_ids = get_skills_list(offer.skills, connection)
    skills_ids = ",".join([str(i) for i in skills_ids])
    cursor.execute("insert into Offers (Position_ID, Company_ID, Category_ID, Currency_ID, Source_ID, Link, "
                   "Skills_IDs, Seniority, Min_salary, Max_salary, Job_summary, Address)"
                   " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (position_id, company_id, category_id, currency_id, source_id, offer.link, skills_ids,
                    offer.seniority,
                    offer.min_salary, offer.max_salary, offer.description, offer.address))
    connection.commit()


def fetch_skills_by_ids(connection, skills_ids):
    cursor = connection.cursor()
    query = f"SELECT ID, Name FROM Skills WHERE ID IN ({','.join(skills_ids)})"
    cursor.execute(query)
    return {row[0] : row[1] for row in cursor.fetchall()}

def get_all_offers_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("""SELECT o.ID,
                       s.Name,
                       o.Link,
                       p.Name,
                       com.Name,
                       o.Min_salary,
                       o.Max_salary,
                       cur.Name,
                       o.Skills_IDs,
                       cat.Name,
                       o.Seniority,
                       o.Job_summary,
                       o.Address
                FROM Offers o
                JOIN Source s ON o.Source_ID = s.ID
                JOIN Position p ON o.Position_ID = p.ID
                JOIN Company com ON o.Company_ID = com.ID
                JOIN Currency cur ON o.Currency_ID = cur.ID
                JOIN Category cat on o.Category_ID = cat.ID""")
    job_offers = [JobInfoModel(dbDto[0], dbDto[1], dbDto[2], dbDto[3], dbDto[4], dbDto[5], dbDto[6], dbDto[7], dbDto[8], dbDto[9], dbDto[10], dbDto[11], dbDto[12]) for dbDto in cursor.fetchall()]
    skills_ids = []
    for job_info in job_offers:
        if job_info.skills:
            skills_ids += job_info.skills.split(',')
    skills_ids = set(skills_ids)
    skills_names_by_id = fetch_skills_by_ids(connection, skills_ids)

    for job_info in job_offers:
        if job_info.skills:
            job_info.skills = [skills_names_by_id[int(skill_id)] for skill_id in job_info.skills.split(',')]
        else:
            job_info.skills = []
    return job_offers