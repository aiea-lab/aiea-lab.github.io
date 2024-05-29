import requests


# Replace these with your actual Notion API key and database ID
NOTION_API_KEY = 'secret_pMjSYaN7ecvYyFpulLLsaWBLrQHlFrvPbVlhfaIqkg1'
DATABASE_ID = '79a626a8176d4aca8922faa551ddbfa8'
MARKDOWN_FILE = '/content/project/allprojects.md'

def get_notion_database_content():
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28'  # Use the latest Notion API version
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch database content. Status code: {response.status_code}")
        print(response.json())
        return None

def extract_project_names(database_content):
    project_names = []
    for result in database_content.get('results', []):
        try:
            title = result['properties']['Project Name']['title'][0]['plain_text']
            project_names.append(title)
        except (KeyError, IndexError) as e:
            print(f"Error extracting project name from entry: {e}")
            continue
    return project_names


def extract_project_details(notion_data):
    projects = {}
    for result in notion_data['results']:
        properties = result['properties']
        project_name = properties['Project Name']['title'][0]['text']['content']

        projects[project_name] = {
            "date": properties.get('Date', {}).get('date', {}).get('start', ""),
            "description": properties.get('Description', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ""),
            "external_link": properties.get('External Link', {}).get('url', ""),
            "image": properties.get('Image', {}).get('url', ""),
            "project_id": properties.get('Project ID', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ""),
            "short_description": properties.get('Short Description', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ""),
            "title": properties.get('Title', {}).get('title', [{}])[0].get('text', {}).get('content', ""),
            "participants": [
                {
                    "name": participant['name'],
                    "is_member": participant.get('is_member', False),
                    "id": participant['id']
                } for participant in properties.get('Participants', {}).get('people', [])
            ],
            "goal": properties.get('Goal', {}).get('rich_text', [{}])[0].get('text', {}).get('content', "")
        }
    return projects

def update_markdown_title(markdown_file, project_name, project_details):
    if project_name not in project_details:
        print(f"Project {project_name} not found.")
        return

    project = project_details[project_name]
    title_line = f'title = "{project["title"]}"\n'

    with open(markdown_file, 'r') as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.startswith('title = '):
            content[i] = title_line
            break

    with open(markdown_file, 'w') as file:
        file.writelines(content)

    print(f"Updated {markdown_file} with title: {project['title']}")

def update_all_markdown_files(directory, project_details):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            project_name = filename.split('.')[0].replace('_', ' ')  # Assuming file name format is "Project_Name.md"
            markdown_file = os.path.join(directory, filename)
            update_markdown_title(markdown_file, project_name, project_details)


if __name__ == "__main__":
    notion_data = get_notion_database_content()
    
    if notion_data:
        project_names = extract_project_names(notion_data)
        project_details = extract_project_details(notion_data)
        
        print("Project Names:", project_names)
        print("Project Details:", project_details)
        
        # directory = "/content/project/allprojects.md"
        # update_all_markdown_files(directory, project_details)
        # directory = DIRECTORY_PATH
        # if os.path.isdir(directory):
        #     update_all_markdown_files(directory, project_details)
        # else:
        #     print(f"The directory {directory} does not exist.")
        # project_name = "XAI Autograder"  # Replace with the correct project name for the file
        # update_markdown_title(MARKDOWN_FILE, project_name, project_details)
