import json
import matplotlib.pyplot as plt

def draw_top_10_skills_histogram(report_data):
    top_ten_items = list(sorted(report_data['skills_counts'].items(), key=lambda item: item[1], reverse=True))[:10]

    plt.figure(figsize=(10, 6))
    plt.bar([i[0] for i in top_ten_items], [i[1] for i in top_ten_items], color='#87ceeb')
    plt.xticks(rotation=45)
    plt.title('Popularne języki i technologie w ofertach pracy "Data"')
    plt.ylabel('Liczba')
    plt.xlabel('Języki/Technologie')


def draw_salary_summary_per_job(report_data):
    report_data_list = [report_data['basic_job_summary'][position] for position in report_data['basic_job_summary'].keys()] 

    mean_salaries = [job_summary['mean_salary'] for job_summary in report_data_list]
    min_salaries = [job_summary['min_salary'] for job_summary in report_data_list]
    max_salaries = [job_summary['max_salary'] for job_summary in report_data_list]

    plt.figure(figsize=(10, 6))

    # linie pionowe
    legend_for_lines_inserted = False
    for i in range(len(report_data_list)):
        if min_salaries[i] and max_salaries[i]:
            plt.vlines(i + 1, ymin=min_salaries[i], ymax=max_salaries[i], color='blue', linestyle='-', linewidth=1.5, zorder=2, label=(None if legend_for_lines_inserted else "Przedział min-max"))
            legend_for_lines_inserted = True
    
    # linie poziome
    plt.scatter(range(1, len(report_data_list) + 1), mean_salaries, marker='o', color='red', zorder=1, label="Średnia")
    plt.xticks(range(1, len(report_data_list) + 1), report_data['basic_job_summary'].keys(), rotation=90)

    plt.title('Przedziały wynagrodzenia dla rożnych stanowisk pracy')
    plt.ylabel('Wynagrodzenie (w PLN)')
    plt.xlabel('Stanowiska pracy')
    plt.legend()
    plt.tight_layout()


def main():
    with open('report.json', 'r') as file:
        report_data = json.load(file)
    draw_top_10_skills_histogram(report_data)
    plt.savefig('plots/top_10_skills_histogram.png')
    draw_salary_summary_per_job(report_data)
    plt.savefig('plots/summary_per_job.png')

if __name__ == "__main__":
    main()
