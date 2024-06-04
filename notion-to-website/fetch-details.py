import requests
import os
import yaml
import json

# Replace these with your actual Notion API key and database ID
NOTION_API_KEY = 'secret_pMjSYaN7ecvYyFpulLLsaWBLrQHlFrvPbVlhfaIqkg1'
DATABASE_ID = '79a626a8176d4aca8922faa551ddbfa8'
MARKDOWN_FILE = 'content/project/allprojects.md'

def get_notion_database_content():
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28'  # Use the latest Notion API version
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        database_content = response.json()
        # Save the response to a JSON file
        with open('database_content.json', 'w') as json_file:
            json.dump(database_content, json_file, indent=4)
        return database_content
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



def extract_project_details(database_content):
    projects = {}
    
    for result in database_content.get('results', []):
        properties = result.get('properties', {})

        # Extracting the project name
        try:
            project_name = properties['Project Name']['title'][0]['plain_text']
        except (KeyError, IndexError):
            project_name = "Unnamed Project"

        # Extracting other project details safely
        date_start = ""
        if properties.get('Dates') and properties['Dates'].get('date'):
            date_start = properties['Dates']['date'].get('start', "")

        description = ""
        if properties.get('Description') and properties['Description'].get('rich_text'):
            description = properties['Description']['rich_text'][0].get('plain_text', "")

        project_id = ""
        if properties.get('Project ID') and properties['Project ID'].get('rich_text'):
            project_id = properties['Project ID']['rich_text'][0].get('plain_text', "")

        short_description = ""
        if properties.get('Short Description') and properties['Short Description'].get('rich_text'):
            short_description = properties['Short Description']['rich_text'][0].get('plain_text', "")

        title = ""
        if properties.get('Title') and properties['Title'].get('title'):
            title = properties['Title']['title'][0].get('plain_text', "")

        goal = ""
        if properties.get('Goal') and properties['Goal'].get('rich_text'):
            goal = properties['Goal']['rich_text'][0].get('plain_text', "")

        projects[project_name] = {
            "date": date_start,
            "description": description,
            "external_link": result.get('url', ""),
            "image": properties.get('Image', {}).get('url', ""),
            "project_id": project_id,
            "short_description": short_description,
            "title": title,
            "participants": [
                {
                    "name": participant.get('name', ''),
                    "is_member": participant.get('is_member', False),
                    "id": participant.get('id', '')
                } for participant in properties.get('Assigned To', {}).get('people', [])
            ],
            "goal": goal
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

#Update all markdown files -- This code is correct
def update_all_markdown_files(directory, project_details):
    # Ensure the content directory exists
    os.makedirs(directory, exist_ok=True)

    for project_name, details in project_details.items():
        filename = f"{details['project_id']}.md"
        filepath = os.path.join(directory, filename)

        print(filename)
        print(filepath)

        # Create front matter in YAML format
        front_matter = {
            'title': details['title'],
            'date': details['date'],
            'description': details['description'],
            'external_link': details['external_link'],
            'image': details['image'],
            'project_id': details['project_id'],
            'short_description': details['short_description'],
            'goal': details['goal'],
            'participants': [{'name': p['name'], 'is_member': p['is_member']} for p in details['participants']]
        }

        # Write to markdown file
        with open(filepath, 'w') as file:
            file.write('---\n')
            yaml.dump(front_matter, file, default_flow_style=False)
            file.write('---\n\n')

            # Additional content can be added here if necessary
            file.write(f"# {project_name}\n\n")
            file.write(f"{details['description']}\n\n")

        print(f"Updated {filepath} with project details.")

def update_markdown_file(markdown_file, project_details):
    with open(markdown_file, 'w') as file:
        for project_name, details in project_details.items():
            file.write(f"# {project_name}\n\n")
            file.write(f"**Title:** {details['title']}\n\n")
            file.write(f"**Date:** {details['date']}\n\n")
            file.write(f"**Description:** {details['description']}\n\n")
            file.write(f"**External Link:** {details['external_link']}\n\n")
            file.write(f"**Image:** {details['image']}\n\n")
            file.write(f"**Project ID:** {details['project_id']}\n\n")
            file.write(f"**Short Description:** {details['short_description']}\n\n")
            file.write(f"**Goal:** {details['goal']}\n\n")
            file.write(f"**Participants:**\n")
            for participant in details['participants']:
                file.write(f"- {participant['name']} (Member: {participant['is_member']})\n")
            file.write("\n---\n\n")

    # print(f"Updated {markdown_file} with project details.")


if __name__ == "__main__":
    notion_data = get_notion_database_content()
    
    if notion_data:
        project_names = extract_project_names(notion_data)
        project_details = extract_project_details(notion_data)
        
        print("Project Names:", project_names)
        print("Project Details:", project_details)

        update_markdown_file(MARKDOWN_FILE, project_details)
        update_all_markdown_files('/Users/ananya/Documents/aiea-lab.github.io/content/project/', project_details)
    
