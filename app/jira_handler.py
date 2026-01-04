from atlassian import Jira
import logging
import os

logger = logging.getLogger(__name__)

class JiraHandler:
    def __init__(self):
        self.url = os.getenv('JIRA_URL')
        self.username = os.getenv('JIRA_USERNAME')
        self.password = os.getenv('JIRA_PASSWORD')  # or API token
        self.project_key = os.getenv('JIRA_PROJECT_KEY')
        if not all([self.url, self.username, self.password, self.project_key]):
            raise ValueError("Jira credentials not fully set")
        self.jira = Jira(url=self.url, username=self.username, password=self.password)

    def create_issue(self, summary, description):
        """Create a Jira issue with the given summary and description."""
        try:
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
            }
            issue = self.jira.create_issue(fields=issue_dict)
            logger.info(f"Created Jira issue: {issue['key']}")
            return issue
        except Exception as e:
            logger.error(f"Failed to create Jira issue: {e}")
            return None