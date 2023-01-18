from __future__ import annotations

import requests as requests
from requests import Response

from api.base_api import BaseApi
from constants import BASE_URL, AUTH, PROJECT_NAME

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AUTH}'
}


class GetTicketBuilder(BaseApi):

    def __init__(self):
        BaseApi.session = requests.Session() if not BaseApi.session else BaseApi.session
        self.query = []
        self.headers = HEADERS
        self.base_link = f'{BASE_URL}/rest/api/2/search'

    def summary(self, summary: str) -> GetTicketBuilder:
        self.query.append(f'text~"{summary}"')
        return self

    def assignee(self, assignee: str) -> GetTicketBuilder:
        self.query.append(f'assignee in ({assignee})')
        return self

    def issue_type(self, type_: str) -> GetTicketBuilder:
        self.query.append(f'issuetype={type_}')
        return self

    def project(self, project: str) -> GetTicketBuilder:
        self.query.append(f'project={project}')
        return self

    def execute(self) -> Response:
        params = {'jql': ' AND '.join(self.query)}
        return self.get(self.base_link, params=params, headers=self.headers)


class CreateTicketBuilder(BaseApi):
    def __init__(self):
        BaseApi.session = requests.Session() if not BaseApi.session else BaseApi.session
        self.headers = HEADERS
        self.base_link = f'{BASE_URL}/rest/api/2/issue'
        self.payload = {}
        self.links = []
        self.labels = []

    def project(self, project_id: int) -> CreateTicketBuilder:
        self.payload['project'] = {'id': project_id}
        return self

    def summary(self, summary: str) -> CreateTicketBuilder:
        self.payload['summary'] = summary
        return self

    def issue_type(self, issuetype_id: int) -> CreateTicketBuilder:
        self.payload['issuetype'] = {'id': issuetype_id}
        return self

    def description(self, description: str) -> CreateTicketBuilder:
        self.payload['description'] = description
        return self

    def link(self, link: str) -> CreateTicketBuilder:
        self.links.append({
            "add": {
                "type": {
                    "name": "Testing",
                    "inward": "is tested by",
                    "outward": "tests"
                },
                "outwardIssue": {
                    "key": link
                }
            }
        })
        return self

    def label(self, label):
        self.labels.append({
            "add": label
        })
        return self

    def execute(self) -> Response:
        json_payload = {'fields': self.payload, 'update': {'issuelinks': self.links, 'labels': self.labels}}
        return self.post(self.base_link, json=json_payload, headers=self.headers)


def get_issue_type_id() -> Response:
    BaseApi.session = requests.Session() if not BaseApi.session else BaseApi.session
    return BaseApi().get(f'{BASE_URL}/rest/zapi/latest/util/zephyrTestIssueType', headers=HEADERS)


def get_project_info() -> Response:
    BaseApi.session = requests.Session() if not BaseApi.session else BaseApi.session
    return BaseApi().get(f'{BASE_URL}/rest/api/latest/project/{PROJECT_NAME}', headers=HEADERS)


def add_label(issue_id, label="automated"):
    BaseApi.session = requests.Session() if not BaseApi.session else BaseApi.session
    payload = {"update": {"labels": [{"add": label}]}}
    return BaseApi().put(f'{BASE_URL}/rest/api/2/issue/{issue_id}', json=payload, headers=HEADERS)


get_ticket_builder = GetTicketBuilder()
create_ticket_builder = CreateTicketBuilder()

if __name__ == "__main__":
    get_project_info()
