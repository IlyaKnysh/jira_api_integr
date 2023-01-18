from api.jira_api import create_ticket_builder, get_issue_type_id, get_ticket_builder, get_project_info
from constants import PROJECT_NAME
from entities import Ticket

test_issue_type_id = None
project_id = None


def get_test_issue_type_id() -> str:
    return get_issue_type_id().json().get('testcaseIssueTypeId')


def check_test_ticket_exist(summary: str) -> list:
    tickets = get_ticket_builder.summary(summary).project(PROJECT_NAME).issue_type('Test').execute().json().get(
        'issues')
    return [ticket for ticket in tickets if summary in ticket.get('fields').get('summary')]


def create_test_ticket(ticket: Ticket) -> None:
    global test_issue_type_id
    if not test_issue_type_id:
        test_issue_type_id = get_test_issue_type_id()
    if isinstance(ticket.link, str):
        ticket.link = [ticket.link]
    query_builder = create_ticket_builder.issue_type(test_issue_type_id).summary(
        f'{ticket.suite}: {ticket.summary}').project(ticket.project)
    # for link in ticket.link:
    #     query_builder.link(link)
    if ticket.params:
        ticket.description = f'Params: \n{ticket.params}\n\n{ticket.description}'
    if ticket.description:
        query_builder.description(ticket.description)
    query_builder.label('apiAutomated').label('SmokeAPI_UDS')
    query_builder.execute()


def get_project_id():
    return get_project_info().json().get('id')
    # return 14700


if __name__ == '__main__':
    test_ticket = Ticket('test_summary', 'LCP-22016', 14700, 'test_decription')
    create_test_ticket(test_ticket)
