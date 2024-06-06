from set_credential import set_credential
from google.cloud import bigquery

def save_result(input_text, output_text, status, time):
    credentials = set_credential()
    client = bigquery.Client(credentials=credentials)
    
    query = """
        INSERT INTO `llama_llm`.llama_llm_result (QUESTION, ANSWER, USER_FEEDBACK, `BQ_CREATED_DATE`, `BQ_UPDATED_DATE`)
        VALUES (@input_text, @output_text, @status, @time1, @time2)
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("input_text", "STRING", input_text),
            bigquery.ScalarQueryParameter("output_text", "STRING", output_text),
            bigquery.ScalarQueryParameter("status", "STRING", status),
            bigquery.ScalarQueryParameter("time1", "STRING", time),
            bigquery.ScalarQueryParameter("time2", "STRING", time),
        ]
    )
    
    try:
        print("Inserting")
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Waits for the query to finish
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error: {e}")

    return 'ok'
