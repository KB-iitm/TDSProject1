from tasks.Task_A1 import install_uv, run_datagen
from tasks.Task_A2 import format_with_prettier
from tasks.Task_A3 import count_wednesdays
from tasks.Task_A4 import sort_contacts
from tasks.Task_A4 import extract_sort_keys
from tasks.Task_A5 import extract_recent_logs
from tasks.Task_A6 import generate_md_index
from tasks.Task_A7 import extract_email_sender
from tasks.Task_A8 import extract_credit_card_number
from tasks.Task_A9 import find_most_similar_comments
from tasks.Task_A10 import calculate_gold_ticket_sales
from tasks.Task_B3 import fetch_api_data, extract_api_data
from tasks.Task_B4 import clone_and_commit, extract_clone_and_commit
from tasks.Task_B5 import run_sql_query, extract_sql_query
from tasks.Task_B6 import scrape_website, extract_scrape
from tasks.Task_B7 import process_image, extract_image_params
from tasks.Task_B8 import transcribe_audio, extract_audio_params
from tasks.Task_B9 import convert_md_to_html, extract_md_to_html
from tasks. Task_B10 import filter_csv, extract_filter_csv
# Import other tasks as needed...

TASK_MAP = {
    "A1": [install_uv, run_datagen],
    "A2": format_with_prettier,
    "A3": count_wednesdays,
    "A4": sort_contacts,
    "A5": extract_recent_logs,
    "A6": generate_md_index,
    "A7": extract_email_sender,
    "A8": extract_credit_card_number,
    "A9": find_most_similar_comments,
    "A10": calculate_gold_ticket_sales,
    "B3": fetch_api_data,
    "B4": clone_and_commit,
    "B5": run_sql_query,
    "B6": scrape_website,
    "B7": process_image,
    "B8": transcribe_audio,
    "B9": convert_md_to_html,
    "B10": filter_csv
    # Add mappings for other tasks
}

def execute_task(task_code, user_inputs=None):
    """
    Execute the given task and return its result.
    """
    try:
        # Find the module dynamically
        module_name = f"tasks.Task_{task_code}"
        module = __import__(module_name, fromlist=[""])
        
        # Get the function (assuming task function name matches task_code)
        func_name = task_code.lower()  
        task_function = getattr(module, func_name, None)

        if task_function is None or not callable(task_function):
            raise HTTPException(status_code=400, detail=f"Task {task_code} function not found in {module_name}")

        # Get function parameters
        func_params = inspect.signature(task_function).parameters
        required_params = [p for p in func_params if func_params[p].default == inspect.Parameter.empty]

        # Ensure all required parameters are provided
        missing_params = [param for param in required_params if param not in user_inputs]
        if missing_params:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required parameters for {task_code}: {missing_params}"
            )

        # Execute the function and return its output
        result = task_function(**user_inputs)
        return {"success": True, "result": result}

    except Exception as e:
        return {"error": f"Failed to execute {task_code}: {str(e)}"}
# Example: execute_task("A3", "dates.txt", "output.txt")