import requests

def get_crop_details(crop_name):
    # Set your Trefle API token
    api_token = '1KtuHrdM4t_pI7PI9N6P_kEqWGchL7a5XGUvEkWHZg4'

    # API endpoint for plant search
    endpoint = f"https://trefle.io/api/v1/plants/search?token={api_token}&q={crop_name}"

    try:
        # Send GET request to the API
        response = requests.get(endpoint)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract crop details from the response
            if data['data']:
                crop = data['data'][0]  # Assuming the first result is the desired crop
                crop_name = crop['common_name']
                family = crop['family']
                scientific_name = crop['scientific_name']
                # Extract any other desired details from the crop object

                # Return the crop details
                return {
                    'Crop Name': crop_name,
                    'Family': family,
                    'Scientific Name': scientific_name
                    # Add more fields as needed
                }
            else:
                return {'error': 'Crop not found'}
        else:
            return {'error': 'Request failed'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Example usage
crop_name = 'coffee'  # Replace with your desired crop name
crop_details = get_crop_details(crop_name)
print(crop_details)
