import csv
import json
from collections import OrderedDict, Counter
from glob import glob

from api.jira_steps import get_project_id
from entities import Ticket


def get_tests(folder_path: str) -> list:
    report = []
    for f_name in glob(f'{folder_path}/*.json'):
        with open(f_name) as f:
            test = json.load(f)
            report.append(test) if isinstance(test, dict) else None
    return report


def write_to_csv(entries):
    with open('result.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for entry in entries:
            writer.writerow([entry.replace('\t', ''), entries[entry], len(entries[entry])])


def get_list_of_grouped_issues():
    results = {}
    list_of_tests = get_tests('results')
    for test in list_of_tests:
        trace = test.get('statusTrace').split('\n')
        reason = trace[-2] if len(trace[-2]) > 15 else trace[-3]
        try:
            results[reason].append(test.get('name'))
        except KeyError:
            results[reason] = [test.get('name')]
    return OrderedDict(reversed(sorted(results.items(), key=lambda x: len(x[1]))))


def convert_report_to_ticket(tests: list, package) -> list:
    tickets = []
    project_id = get_project_id()
    for test in tests:
        package_prefix = f'com.lenovo.qa.api.core.{package}'
        is_in_package = [x for x in test.get('labels') if
                         x.get('name') == 'package' and package_prefix in x.get('value')]
        if is_in_package and 'CLEANUP_SPEC' not in test.get('name'):
            links = [link.get('name') for link in test.get('links')]
            steps = '\n'.join([step.get('name') for step in test.get('testStage').get('steps')]) if test.get(
                'testStage') else None
            suite = is_in_package[0].get('value').replace(f'{package_prefix}.', '')
            params = ', '.join([f'{x.get("name")}: {x.get("value")}' for x in test.get('parameters')]) if test.get('parameters') else None
            tickets.append(
                Ticket(summary=test.get('name'), link=links, project=project_id, description=steps, suite=suite,
                       params=params))
    return tickets


def combine_parametrized_tickets(tickets):
    def _filter_by_summary(summary_):
        return [ticket for ticket in tickets if ticket.summary == summary_]

    combined_tickets = []
    count_summary = Counter([x.summary for x in tickets])
    for summary in count_summary:
        if count_summary[summary] == 1:
            combined_tickets.append(*_filter_by_summary(summary))
        else:
            filtered_tickets = _filter_by_summary(summary)
            total_params = '\n'.join(
                [ticket.params for ticket in filtered_tickets]) if filtered_tickets[0].params else None
            filtered_tickets[0].params = total_params
            combined_tickets.append(filtered_tickets[0])
    return combined_tickets


if __name__ == '__main__':
    write_to_csv(get_list_of_grouped_issues())
