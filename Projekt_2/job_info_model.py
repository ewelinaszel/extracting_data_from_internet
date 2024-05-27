class JobInfoModel:
    def __init__(self, id, source, link, position, company, min_salary, max_salary, currency, skills, category,
                 seniority, description, address):
        self.id = id
        self.source = source
        self.link = link
        self.position = position
        self.company = company
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.currency = currency
        self.skills = skills
        self.category = category
        self.seniority = seniority
        self.description = description
        self.address = address

