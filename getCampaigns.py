import requests
from google.ads.googleads.client import GoogleAdsClient
from google.auth.transport.requests import Request

def main2(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""

    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    print(dir(stream))

    for batch in stream:
        for row in batch.results:
            print(
                f"Campaign with ID {row.campaign.id} and name "
                f'"{row.campaign.name}" was found.'
            )


def main():
    # Load the Google Ads client library from the google-ads.yaml configuration file
    client = GoogleAdsClient.load_from_storage('google-ads.yaml')

    # Access the OAuth2 credentials from the client
    credentials = client.credentials
    print(credentials)
    print(dir(credentials))
    # Refresh the access token if necessary
    credentials.refresh(Request())

    # Extract the access token
    access_token = credentials.token

    # Specify the customer ID (the 10-digit account number without hyphens)
    customer_id = '6283329745'

    # Define the API endpoint URL for listing campaigns
    url = f'https://googleads.googleapis.com/v17/customers/{customer_id}/campaigns'

    # Set up the headers required for the API call
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Developer-Token': client.developer_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Make the GET request to the API endpoint
    response = requests.get(url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        campaigns = response.json().get('results', [])
        if campaigns:
            for campaign in campaigns:
                print(f"Campaign ID: {campaign['resourceName']}, Name: {campaign['name']}")
        else:
            print("No campaigns found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    client = GoogleAdsClient.load_from_storage('google-ads.yaml')
    customer_id = '7920620082'
    try:
        main2(client, customer_id)
    except Exception as err:
        print(err.failure.errors)
