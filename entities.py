from __future__ import annotations


class Ticket:
    def __init__(self, summary: str = None, link: str | list = None, project: int = None, description: str = None,
                 suite: str = None, params: str = None):
        self.summary = summary
        self.link = link
        self.project = project
        self.description = description
        self.suite = suite
        self.params = params

    def __repr__(self):
        return f'SUMMARY: {self.summary}, LINK: {self.link}'
