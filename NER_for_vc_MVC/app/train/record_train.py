# record the training data into bigquery table
# 1. create table (try)
# 2. insert data
import uuid   
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from app.credentials.set_credential import set_credential

def get_training_info():
    credentials = set_credential()
    client = bigquery.Client(credentials=credentials)
    create_table('intern-project-415606', 'NER_web', 'training_record')
    query = """
        SELECT *
        FROM `intern-project-415606.NER_web.training_record`
    """
    query_job = client.query(query)
    result = query_job.result()
    training_info = [dict(row) for row in result]
    for training_record in training_info:
        if training_record['Job Ended Time'] == training_record['Job Created Time']:
            training_record['Job Ended Time'] = 'In Progress'
    #sort by job created time
    train_info = sorted(training_info, key=lambda x: x['Job Created Time'], reverse=True)
    train_html = pd.DataFrame(train_info).to_html(index=False)
    train_html = train_html[train_html.find('\n'):train_html.rfind('\n')]

    return train_info, train_html

def create_table(project_id, dataset_id, table_id_write):
    credentials = set_credential()
    bigquery_client = bigquery.Client(credentials=credentials)
    schema = [
        bigquery.SchemaField("UUID", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Username", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Dataset Description", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Job Created Time", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("Job Ended Time", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("Job Duration", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Model Path", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Result Path", "STRING", mode="REQUIRED")
    ]
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id_write}", schema=schema)
    try:
        table = bigquery_client.create_table(table)
    except Exception as e:
        print(f"Table {project_id}.{dataset_id}.{table_id_write} already exists.")

def create_uuid():
    return str(uuid.uuid1().hex)

def add_record_begin(dataset_name, dataset_size):
    # Authenticate using service account credentials
    credentials = set_credential()
    create_table('intern-project-415606', 'NER_web', 'training_record')
    client = bigquery.Client(credentials=credentials)
    job_uuid, start_time = create_uuid(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    query = f"""
        INSERT INTO `intern-project-415606.NER_web`.training_record (UUID, Username, Status, `Dataset Description`, `Job Created Time`, `Job Ended Time`, `Job Duration`, `Model Path`, `Result Path`)
        VALUES ('{job_uuid}', 'admin', 'In Progress', '{dataset_name} - {dataset_size}', '{start_time}', '{start_time}', 0, '-', '-')
    """
    try:
        client.query(query)
    except Exception as e:
        print(f"Error: {e}")

    return job_uuid

def add_record_done(job_uuid, model_path, result_path):
    credentials = set_credential()
    client = bigquery.Client(credentials=credentials)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = f"""
        UPDATE `intern-project-415606.NER_web`.training_record
        SET `Status` = 'Completed', `Job Ended Time` = '{end_time}', `Job Duration` = TIMESTAMP_DIFF(TIMESTAMP('{end_time}'), TIMESTAMP(`Job Created Time`), SECOND), `Model Path` = '{model_path}', `Result Path` = '{result_path}'
        WHERE UUID = '{job_uuid}'
    """
    try:
        client.query(query)
    except Exception as e:
        print(f"Error: {e}")
