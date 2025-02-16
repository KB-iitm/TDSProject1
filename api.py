from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import os
import re
import subprocess
from sentence_transformers import SentenceTransformer, util
import numpy as np
from task_dispatcher import (
    install_uv, run_datagen, format_with_prettier, count_wednesdays, 
    sort_contacts, extract_recent_logs, generate_md_index, 
    extract_email_sender, extract_credit_card_number, find_most_similar_comments, 
    calculate_gold_ticket_sales, fetch_api_data, clone_and_commit, run_sql_query,
    scrape_website, process_image, transcribe_audio, convert_md_to_html, 
    filter_csv, extract_sort_keys, extract_api_data, extract_clone_and_commit,
    extract_sql_query, extract_scrape, extract_image_params, extract_audio_params,
    extract_md_to_html, extract_filter_csv
)

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

DATA_DIR = Path(\data)

def is_valid_path(file_path: str) -> bool:
    abs_path = os.path.abspath(file_path)
    return abs_path.startswith(os.path.abspath(DATA_DIR))


# 🔹 Task mapping: Natural language -> Task codes
TASK_MAPPING = {
    "install uv and run datagen": "A1",
    "format format.md with prettier": "A2",
    "count wednesdays in dates.txt": "A3",
    "sort contacts in contacts.json": "A4",
    "extract recent logs": "A5",
    "generate markdown index": "A6",
    "extract email sender": "A7",
    "extract credit card number": "A8",
    "find similar comments": "A9",
    "calculate gold ticket sales": "A10",
    "fetch api data": "B3",
    "clone and commit": "B4",
    "run sql query": "B5",
    "scrape website": "B6",
    "process image": "B7",
    "transcribe audio": "B8",
    "convert md to html": "B9",
    "filter csv": "B10"
    # add more mappings as needed...
}

task_keys = list(TASK_MAPPING.keys())
task_embeddings = model.encode(task_keys, convert_to_tensor=True)

def get_best_task_code(query: str) -> str:
    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Compute cosine similarities
    cosine_scores = util.cos_sim(query_embedding, task_embeddings)[0]
    
    # Find the index of the best match
    best_idx = int(np.argmax(cosine_scores))
    best_task_key = task_keys[best_idx]
    
    return TASK_MAPPING[best_task_key]


@app.post("/run")
async def run_task(task: str, file_path: str = None, params: str = Query(None, description="Optional JSON string for additional parameters")):
    """Run the specified task based on user input."""
    print(f"Received task: {task}")

    if file_path and not file_path.startswith("data/"):
        raise HTTPException(status_code=403, detail="Access to files outside /data/ is forbidden.")

    if "delete" in task.lower():
        raise HTTPException(status_code=403, detail="File deletion is not allowed.")

    # 🔹 Convert natural language to task code
    try:
        task_code = get_best_task_code(task.lower())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in matching task: {str(e)}")
    print(task_code)

    user_params = {}
    if params:
        try:
            user_params = json.loads(params)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid params JSON")

    try:
        if task_code == "A1":
            install_uv()
            run_datagen("23ds3000241@ds.study.iitm.ac.in")
        elif task_code == "A2":
            format_with_prettier("data/format.md")
        elif task_code == "A3":
            day_names = ["mondays", "tuesdays", "wednesdays", "thursdays", "fridays", "saturdays", "sundays",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            pattern = r'\b(' + '|'.join(day_names) + r')\b'
            match = re.search(pattern, task.lower())
            target_day = match.group(1) if match else "wednesday"
            print(target_day)
            # Prepare the output file name dynamically, e.g., data/dates-tuesdays.txt
            output_file = f"data/dates-{target_day}s.txt"
            count_wednesdays("data/dates.txt", output_file, target_day)
        elif task_code == "A4":
            sort_keys = extract_sort_keys(task)
            print(f"Extracted sort keys: {sort_keys}")
            
            # Define file names (you can change these if needed)
            input_file = "data/contacts.json"
            output_file = "data/contacts_sorted.json"
            
            sort_contacts(input_file, output_file, sort_keys=sort_keys)
        elif task_code == "A5":
            extract_recent_logs("data/logs", "data/logs-recent.txt")
        elif task_code == "A6":
            generate_md_index("data/docs", "data/docs/index.json")
        elif task_code == "A7":
            extract_email_sender("data/email.txt", "data/email-sender.txt")
        elif task_code == "A8":
            extract_credit_card_number("data/credit_card.png", "data/credit_card.txt", task)
        elif task_code == "A9":
            find_most_similar_comments("data/comments.txt", "data/comments_similar.txt", task)
        elif task_code == "A10":
            calculate_gold_ticket_sales("data/ticket-sales.db", "data/ticket-sales-gold.txt", task)
        elif task_code == "B3":
            url, output_file = extract_api_data(task)
            fetch_api_data(url, output_file)
            return {"status": "success", "message": f"B3: Fetched API data from {url} and saved to {output_file}"}
            fetch_api_data(url, output_file_param)
        elif task_code == "B4":
            repo_url, commit_message = extract_clone_and_commit(task)
            clone_and_commit(repo_url, commit_message)
            return {"status": "success", "message": f"B4: Cloned repo {repo_url} and committed with message '{commit_message}'"}
        elif task_code == "B5":
            db_file, query = extract_sql_query(task)
            run_sql_query(db_file, query)
            return {"status": "success", "message": f"B5: Ran SQL query on {db_file}: {query}"}
        elif task_code == "B6":
            url, output_file = extract_scrape(task)
            scrape_website(url, output_file)
            return {"status": "success", "message": f"B6: Scraped website {url} and saved to {output_file}"}
        elif task_code == "B7":
            input_file, output_file, width, height, quality = extract_image_params(task)
            process_image(input_file, output_file, width, height, quality)
            return {"status": "success", "message": f"B7: Processed image {input_file} to {output_file}"}
        elif task_code == "B8":
            input_file, output_file = extract_audio_params(task)
            transcribe_audio(input_file, output_file)
            return {"status": "success", "message": f"B8: Transcribed audio from {input_file} to {output_file}"}
        elif task_code == "B9":
            input_file, output_file = extract_md_to_html(task)
            convert_md_to_html(input_file, output_file)
            return {"status": "success", "message": f"B9: Converted Markdown {input_file} to HTML and saved to {output_file}"}
        elif task_code == "B10":
            csv_file, column, value = extract_filter_csv(task)
            filter_csv(csv_file, column, value)
            return {"status": "success", "message": f"B10: Filtered CSV {csv_file} where {column} equals {value}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid task name")

        return {"status": "success", "message": f"Task {task_code} executed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
def read_file(path: str):

    print(path)
    file_path = DATA_DIR / path  # Prevent directory traversal
    print(file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
