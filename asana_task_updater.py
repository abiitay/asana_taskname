import requests
import os

# Get the Asana API Token from environment variable
ASANA_ACCESS_TOKEN = os.getenv("ASANA_ACCESS_TOKEN")
PROJECT_GID = "your_project_gid"  # Replace with your actual Project GID
HEADER = {"Authorization": f"Bearer {ASANA_ACCESS_TOKEN}"}

def get_tasks_from_project(project_gid):
    """Fetch all tasks in the project."""
    url = f"https://app.asana.com/api/1.0/projects/{project_gid}/tasks"
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()
    return response.json()["data"]

def get_task_details(task_gid):
    """Fetch task details including custom fields."""
    url = f"https://app.asana.com/api/1.0/tasks/{task_gid}"
    response = requests.get(url, headers=HEADER)
    response.raise_for_status()
    return response.json()["data"]

def update_task_name(task_gid, new_name):
    """Update the task name."""
    url = f"https://app.asana.com/api/1.0/tasks/{task_gid}"
    data = {"name": new_name}
    response = requests.put(url, headers=HEADER, json=data)
    response.raise_for_status()
    print(f"Task {task_gid} renamed to '{new_name}'")

def main():
    # Step 1: Fetch all tasks in the project
    tasks = get_tasks_from_project(PROJECT_GID)
    
    for task in tasks:
        task_gid = task["gid"]
        
        # Step 2: Fetch task details
        task_details = get_task_details(task_gid)
        custom_fields = task_details.get("custom_fields", [])
        
        # Step 3: Extract relevant data (e.g., Client & Site)
        client_and_site = ""
        for field in custom_fields:
            if field["name"] == "Client & Site":  # Adjust to match your form field name
                client_and_site = field.get("text_value", "")  # Assuming it's a text field

        # Step 4: Create the new task name based on "Client & Site"
        if client_and_site:
            new_name = f"{client_and_site} Update"
            update_task_name(task_gid, new_name)

if __name__ == "__main__":
    main()
