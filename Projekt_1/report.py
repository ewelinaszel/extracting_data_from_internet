import json

from Projekt_1.job_info_model import JobInfoModel
def count_unique_skills(job_offers):
    result = {}
    for offer in job_offers:
        for skill in offer["skills"]:
            if skill in result:
                result[skill] += 1
            else:
                result[skill] = 1
    return result


def get_offers_by_seniority_and_position(job_offers, seniority, position):
    return [job_offer for job_offer in job_offers if
            seniority == job_offer["seniority"] and position.lower() in job_offer["position"].lower()]


def get_job_summary(job_offers: []):
    if not job_offers:
        return {"number_of_offers": 0,
                "min_salary": None,
                "max_salary": None,
                "mean_salary": None}
    return {
        "number_of_offers": len(job_offers),
        "min_salary": min([job["min_salary"] for job in job_offers]),
        "max_salary": max([job["max_salary"] for job in job_offers]),
        "mean_salary": sum([job["min_salary"] for job in job_offers] + [job["max_salary"] for job in job_offers]) / (
                    2 * len(job_offers))
    }

def get_basic_job_summary(job_offers):
    seniorities = ['junior', 'mid/regular', 'senior']
    positions = ['Data Engineer', 'Data Analyst', 'Data Scientist', 'Data Architect']
    seniorities_positions = [(seniority, position) for seniority in seniorities for position in positions]
    job_offers_by_seniority_and_position = {sp: get_offers_by_seniority_and_position(job_offers, sp[0], sp[1]) for sp in
                                            seniorities_positions}
    job_summaries_by_seniority_and_position = {key[0][0].upper() + key[0][1:] + ' ' + key[1]: get_job_summary(value) for
                                               key, value in job_offers_by_seniority_and_position.items()}
    return job_summaries_by_seniority_and_position


def main():
    with open('pracuj_jobs.json', 'r') as file:
        job_offers = json.load(file)
    with open('just_join_jobs.json', 'r') as file:
        job_offers += json.load(file)
    dict_of_counted_skills = count_unique_skills(job_offers)
    get_basic_job_summary(job_offers)
    report = {
        "skills_counts": dict_of_counted_skills,
        "basic_job_summary": get_basic_job_summary(job_offers)
    }
    with open('report.json', 'w') as plik:
        json.dump(report, plik, indent=4)


if __name__ == "__main__":
    main()
