import requests

response = requests.get(
    "https://accounitum1.atlassian.net/rest/api/2/search?'jql'=teamable/example@gmail.com:<api-token>/Accept: application/json")

my_projects = response.json()

print(my_projects)

for project in my_projects:
    print(
        f"Project Name: {project['key']}\nProject summary: {project['summary']}\n")
