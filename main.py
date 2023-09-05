from api.jira_steps import create_test_ticket
from constants import LABELS_LIST, PACKAGE_NAME, REPORTS_PATH
from reports_parser import get_tests, convert_report_to_ticket, combine_parametrized_tickets

"""
Path to the folder with test results should be passed as a first command line argument
"""

list_of_tests = get_tests(REPORTS_PATH)
tickets = convert_report_to_ticket(list_of_tests, PACKAGE_NAME)
combined_tickets = combine_parametrized_tickets(tickets)
for ticket in combined_tickets:
    create_test_ticket(ticket, labels=LABELS_LIST)
