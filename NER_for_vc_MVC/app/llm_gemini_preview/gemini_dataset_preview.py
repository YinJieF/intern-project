import re
from time import time
from datetime import datetime
from google.cloud import bigquery
from app.credentials.set_credential import set_credential
#from set_credential import set_credential

# read the (original) data from the bigquery
def read_bq(project_id, dataset_id, table_id, bigquery_client):

    query = f"""
        SELECT *
        FROM {project_id}.{dataset_id}.{table_id}
        ORDER BY extract_id 
        LIMIT 100
    """
    a  = time()
    query_job = bigquery_client.query(query)
    b = time()
    # Convert the result into a Pandas DataFrame
    c = time()
    df = query_job.to_dataframe()
    d = time()
    #df = pandas_gbq.read_gbq(query, credentials=set_credential(), dialect='standard', use_bqstorage_api=True)
    print(f"Time to read the data: {b-a}")
    print(f"Time to convert the data to dataframe: {d-c}")
    return df

# Function to convert various date formats to yyyy-mm-dd    
def convert_to_standard_date(date_str):
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        return date_str
    # Handling Vietnamese format "dd tháng mm năm yyyy"
    viet_date_match = re.match(r'(\d{1,2}) tháng (\d{1,2}) năm (\d{4})', date_str)
    if viet_date_match:
        day = viet_date_match.group(1).zfill(2)
        month = viet_date_match.group(2).zfill(2)
        year = viet_date_match.group(3)
        return f"{year}-{month}-{day}"
    
    # Handling formats like "dd/mm/yyyy" and "dd-mm-yyyy"
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        pass
    
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        pass
    
    # Handling "yyyy-mm" format, assume day as 01
    try:
        return datetime.strptime(date_str, '%Y-%m').strftime('%Y-%m-01')
    except ValueError:
        pass
    
    # Handling "no information" or any other text
    if 'no information' in date_str.lower():
        return 'No information'
    
    # Default return None for unhandled cases
    return None

# Function to convert jail duration to months
def convert_to_months(duration):
    # Define conversion rates
    year_to_month = 12
    month_to_month = 1

    # Dictionary for Vietnamese translations
    vietnamese_to_english = {
        'năm': 'year',
        'tháng': 'month',
        'chung thân': 'life imprisonment',
        'tù chung thân': 'life imprisonment',
        'mười hai': 'twelve',
        'Chín': 'nine',
        'Hai': 'two',
        'Sáu': 'six',
        'bảy': 'seven',
        'Một': 'one',
        '03': 'three',
        '06': 'six',
        '07': 'seven',
        '08': 'eight',
        '09': 'nine'
    }

    # Replace Vietnamese terms with English equivalents
    for viet, eng in vietnamese_to_english.items():
        duration = duration.replace(viet, eng)

    # Handle special cases
    if 'life' in duration.lower():
        return 'Life Imprisonment'
    if 'death' in duration.lower():
        return 'Death Sentence'
    if 'no' in duration.lower() or 'yes' in duration.lower():
        return 'Not Applicable'

    # Extract numbers and units
    numbers = re.findall(r'\d+', duration)
    units = re.findall(r'year|month', duration, re.IGNORECASE)

    # Convert all to months
    total_months = 0
    for number, unit in zip(numbers, units):
        if 'year' in unit.lower():
            total_months += int(number) * year_to_month
        elif 'month' in unit.lower():
            total_months += int(number) * month_to_month

    return total_months

# Function to standardize monetary amounts
def standardize_amount(amount):
    # Check for monthly payments and extract the number of months if present
    monthly_payment_match = re.search(r'(\d+([.,]\d+)*)\s*VND/month\s*for\s*(\d+)\s*months', amount, re.IGNORECASE)
    if monthly_payment_match:
        monthly_payment = monthly_payment_match.group(1).replace('.', '').replace(',', '')
        months = int(monthly_payment_match.group(3))
        return round(float(monthly_payment) * months)  # Return the total payment over the period
    
    # Handle ranges (e.g., "10.000.000-15.000.000")
    range_match = re.search(r'(\d+[.,\d]*)\s*[-đồng tođến]+\s*(\d+[.,\d]*)', amount, re.IGNORECASE)
    if range_match:
        low_amount = range_match.group(1).replace('.', '').replace(',', '')
        high_amount = range_match.group(2).replace('.', '').replace(',', '')
        # Convert to float and take the average of the range
        try:
            low_amount = float(low_amount)
            high_amount = float(high_amount)
            return round((low_amount + high_amount) / 2)
        except ValueError:
            return 0
        
    # Remove non-numeric characters but keep the decimal point and comma
    amount = re.sub(r'[^\d.,]', '', amount)
    # Determine if commas or periods are used as thousand separators or decimal points
    if ',' in amount and '.' in amount:
        if amount.find(',') < amount.find('.'):
            amount = amount.replace(',', '')
        else:
            amount = amount.replace('.', '')
            
    # Replace remaining commas with dots if they are used as decimal separators
    amount = amount.replace('.', ',')
    amount = amount.replace(',', '')
    # Convert to float and round to nearest integer (assuming no cents are needed)
    try:
        standardized_amount = eval(amount)
    except:
        standardized_amount = 0
    return standardized_amount
# Main function to process the DataFrame
def preprocess_dataframe(df):
    # Apply the function to the birthdate column
    df.loc[:,'birthdate'] = df['birthdate'].apply(convert_to_standard_date)
    df.loc[:,'jail_duration'] = df['jail_duration'].apply(convert_to_months)
    df.loc[:,'fine_total'] = df['fine_total'].apply(standardize_amount)
    return df

def load_data(PROJECT_ID, DATASET_ID, TABLE_ID):
    credentials = set_credential()
    bigquery_client = bigquery.Client(credentials=credentials,
                                      project=PROJECT_ID)
    
    df = read_bq(PROJECT_ID, DATASET_ID, TABLE_ID, bigquery_client)
    df = preprocess_dataframe(df) 
    data_html = df.to_html(index=False)
    data_html = data_html[data_html.find('\n'):data_html.rfind('\n')]
    # Convert dataset shape to dictionary
    dataset_shape = {"rows": df.shape[0], "columns": df.shape[1]}
    return data_html, dataset_shape 


# table_id = "criminal_data_gemini"
# project_id = 'intern-project-415606'
# selected_dataset = 'Criminal_Dataset'

# # Load data using provided parameters
# data_html, dataset_shape = load_data(project_id, selected_dataset, table_id)
# print(data_html)
