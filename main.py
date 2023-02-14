import sys

from api.jira_steps import create_test_ticket, check_test_ticket_exist
from reports_parser import get_tests, convert_report_to_ticket, combine_parametrized_tickets

"""
Path to the folder with test results should be passed as a first command line argument
"""

list_of_tests = get_tests(sys.argv[1])
# list_of_new_tests = [test for test in list_of_tests if not check_test_ticket_exist(test.get('name'))]
tickets = convert_report_to_ticket(list_of_tests, 'smoke')
combined_tickets = combine_parametrized_tickets(tickets)
for ticket in combined_tickets:
    create_test_ticket(ticket)
# new_summaries = [
#
# ]
# new_tickets = []
# for new in new_summaries:
#     new_tickets.append([x for x in combined_tickets if new.strip() in x.summary][0])
# list_of_new_tests = [test for test in new_tickets if not check_test_ticket_exist(test.summary)]
# for ticket in list_of_new_tests:
#     create_test_ticket(ticket)
