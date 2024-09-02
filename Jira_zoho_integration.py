import requests
import json
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
JIRA_URL = os.getenv('JIRA_URL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_USER_EMAIL = os.getenv('JIRA_USER_EMAIL')
ZOHO_DESK_URL = os.getenv('ZOHO_DESK_URL')
ZOHO_API_KEY = os.getenv('ZOHO_API_KEY')
DEPARTMENT_ID = os.getenv('DEPARTMENT_ID')
CONTACT_ID = os.getenv('CONTACT_ID')

def create_jira_issue(ticket):
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "fields": {
            "project": {
                "key": "YOUR_PROJECT_KEY"  # Replace with your project key
            },
            "summary": ticket['subject'],
            "description": ticket['description'],
            "issuetype": {
                "name": "Task"  # Change issue type as needed
            }
        }
    }
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
    if response.status_code == 201:
        print(f"Created JIRA issue: {response.json()['key']}")
    else:
        print(f"Failed to create JIRA issue: {response.status_code} - {response.text}")

def get_zoho_tickets():
    url = f"{ZOHO_DESK_URL}/tickets"
    headers = {
        'Authorization': f'Zoho-oauthtoken {ZOHO_API_KEY}',
        'Content-Type': 'application/json'
    }
    params = {
        'status': 'Open',  # Filter by status, e.g., Open tickets
        'limit': 10,  # Number of tickets to fetch
        'sortBy': 'createdTime',  # Sort by creation time
        'sortOrder': 'desc'  # Sort order: descending
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to get Zoho tickets: {response.status_code} - {response.text}")
        return []

def get_jira_issues():
    url = f"{JIRA_URL}/rest/api/3/search"
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)
    headers = {
        'Accept': 'application/json'
    }
    query = {
        'jql': 'project=YOUR_PROJECT_KEY AND status=Open',  # Customize your JQL query
        'maxResults': 10
    }
    response = requests.get(url, headers=headers, auth=auth, params=query)
    if response.status_code == 200:
        return response.json()['issues']
    else:
        print(f"Failed to get JIRA issues: {response.status_code} - {response.text}")
        return []

def main():
    # Fetch Zoho Desk tickets and create corresponding JIRA issues
    zoho_tickets = get_zoho_tickets()
    for ticket in zoho_tickets:
        create_jira_issue(ticket)

    # Optionally, fetch JIRA issues (example usage)
    jira_issues = get_jira_issues()
    for issue in jira_issues:
        print(f"JIRA Issue: {issue['key']} - {issue['fields']['summary']}")

if __name__ == "__main__":
    main()
