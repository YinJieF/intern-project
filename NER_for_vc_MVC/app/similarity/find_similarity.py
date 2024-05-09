import numpy as np
import pandas as pd
from google.cloud import bigquery
from difflib import SequenceMatcher
from scipy.spatial.distance import cosine
from app.credentials.set_credential import set_credential
from app.inference.predict import load_model, lookup

# read the (original) data from the bigquery
def read_bq(project_id, dataset_id, table_id):
    bigquery_client = bigquery.Client(credentials=set_credential())

    query = f"""
        SELECT *
        FROM {project_id}.{dataset_id}.{table_id}
    """
    query_job = bigquery_client.query(query)
    # Convert the result into a Pandas DataFrame
    df = query_job.to_dataframe()

    return df

loaded_model = load_model()
embedding_layer = loaded_model.embedding_layer

def word_embedding(input):
    embedding_vectors = embedding_layer(lookup([input]))

    embedding_vector_list = embedding_vectors.numpy().tolist()[0]
    
    return embedding_vector_list

def find_top_similar(df, input_name, column, n):
    if column == 'String':
        # Compute similarities
        similarities = df['NAME'].apply(lambda x: SequenceMatcher(None, input_name, x).ratio())

        # Get the indices of the top 10 most similar names
        top_10_indices = np.argsort(similarities)[-int(n):][::-1]

        # Retrieve the top 10 most similar rows
        top_10_rows = df.iloc[top_10_indices]

        # Create a new DataFrame with the desired columns
        result = pd.DataFrame({
            'index': top_10_rows.index,
            'JLR_LINK': top_10_rows['JLR_LINK'],
            'NAME': top_10_rows['NAME'],
            'similarity': similarities[top_10_indices]
        })

        # Display the result
        result_html = result.to_html(index=False)
        result_html = result_html[result_html.find('\n'):result_html.rfind('\n')]
        return result_html
    
    elif column == 'Vector':
        # Assuming df is your DataFrame containing the 'VECTOR' column
        df['VECTOR'] = df['VECTOR'].apply(lambda x: eval(x))

        # Check the modified DataFrame
        vector_list = word_embedding(input_name)

        # Compute cosine similarities
        cosine_similarities = [1 - cosine(vector_list, v) for v in df['VECTOR']]

        # Get the indices of the top 10 most similar vectors
        top_10_indices = np.argsort(cosine_similarities)[-int(n):][::-1]

        # Retrieve the top 10 most similar vectors
        top_10_vectors = df.iloc[top_10_indices]
        result = pd.DataFrame({
            'index': top_10_vectors.index,
            'JLR_LINK': top_10_vectors['JLR_LINK'],
            'NAME': top_10_vectors['NAME'],
            'similarity': np.array(cosine_similarities)[top_10_indices]
        })
        
        # Display the result
        result_html = result.to_html(index=False)
        result_html = result_html[result_html.find('\n'):result_html.rfind('\n')]
        return result_html

