import requests
import subprocess

def comparison(input_data):
    try:
        # Obtain the identity token using gcloud
        result = subprocess.run('gcloud auth print-identity-token', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode != 0:
            raise Exception(f"Error obtaining identity token: {result.stderr.decode('utf-8')}")
        
        identity_token = result.stdout.decode('utf-8').strip()

        # URL to which the POST request will be sent
        url = "https://us-central1-intern-project-415606.cloudfunctions.net/comparison"

        # Headers including the Authorization token
        headers = {
            "Authorization": f"bearer {identity_token}",
            "Content-Type": "application/json"
        }

        # Send the POST request
        response = requests.post(url, json=input_data, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        # Decode the JSON response to make it readable
        decoded_response = response.json()
        print(decoded_response)
        #print(decoded_response)
        return decoded_response

    except Exception as e:
        print(f"An error occurred: {e}")

# Data to be sent in the POST request
data = {
    "person": {
        "name": "Nguyễn Thị M",
        "gender": "Male",
        "birthdate": "1980-03-27",
        "company_name": "ABC Company",
        "province_name": "Hà Nội",
        "district_name": "Hoàn Kiếm",
        "full_address": "123 ABC Street, Hoàn Kiếm, Hà Nội"
    }
}

#comparison(data)
