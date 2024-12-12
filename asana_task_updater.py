import requests

# Replace with your Asana Personal Access Token
ASANA_ACCESS_TOKEN = "2/1208756554701895/1208967186635071:e31a47a948983d8332cd856a5bd0112a"
PROJECT_GID = "1208964551030260"  # Replace with your project GID
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
    
    print(f"Fetched {len(tasks)} tasks.")

    for task in tasks:
        task_gid = task["gid"]
        
        # Step 2: Fetch task details
        task_details = get_task_details(task_gid)
        custom_fields = task_details.get("custom_fields", [])
        
        # Step 3: Log the structure of custom fields
        print(f"Task {task_gid} has the following custom fields:")
        for field in custom_fields:
            print(field)  # Log each custom field to inspect the structure
        
        # Step 4: Extract relevant data (e.g., Client & Site, Update Type)
        client_and_site = ""
        update_type = ""
        
        for field in custom_fields:
            if field["name"] == "Client & Site":
                # Check for 'enum_value' (single select field)
                if "enum_value" in field:
                    client_and_site = field["enum_value"].get("name", "")
                else:
                    print(f"Unexpected format for 'Client & Site' in task {task_gid}")
            elif field["name"] == "Update Type":
                # Check for 'text_value' (text field)
                if "text_value" in field:
                    update_type = field["text_value"]
                else:
                    print(f"Update Type field is missing 'text_value' in task {task_gid}")
        
        # Step 5: Create the new task name using Client & Site + Update Type
        if client_and_site and update_type:
            new_name = f"{client_and_site} + {update_type}"
            print(f"Renaming task {task_gid} to: '{new_name}'")  # Print the renaming action
            update_task_name(task_gid, new_name)
        else:
            print(f"Missing data for task {task_gid}, skipping rename.")
   
if __name__ == "__main__":
    main()
