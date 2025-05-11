import requests
import time
import json
import hashlib


# --- Configuration ---
api_url_base = "https://prod-global-api.popmart.com/shop/v1/box/box_set/preview"

current_t = int(time.time())


# --- Provided Payload ---
# This is the exact data you want to send in the POST request body
post_payload = {
    "set_no": "10001732500585",
            #    010010001356100585 
            # https://www.popmart.com/us/pop-now/set/195-10001356100585
    "s": "9d964f54b5eeac49aa3cf872d4a9eb75",
    "t": current_t  # Using the specific timestamp from your payload
}

# Note: The 'spu_id' from your original GET request parameters is not in this payload.
# Verify if 'spuId' is needed for this POST request or if 'set_no' replaces it.

# Since 's' and 't' are in the post_payload, query_params_for_post should likely be empty or None
# unless the API specifically requires other parameters in the URL for this POST endpoint.
query_params_for_post = None # Or an empty dictionary {}

jwt_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6Im5hdXMiLCJ0eXAiOiJKV1QifQ.eyJnaWQiOiIyOTg3MDI0Iiwibmlja25hbWUiOiJicmRheWF1b24iLCJhdmF0YXIiOiIiLCJ2aXBMZXZlbCI6MCwicm9sZSI6IlVzZXIiLCJhcHBJRCI6MSwiYXBwQ29kZSI6MCwicHJvdmlkZXJUeXBlIjoiZ29vZ2xlIiwibG9naW5BdCI6MTc0MzQ3Njk1OSwic2hvd0lEIjoiODAwNjQ5OTE1OTAwNTM3Njg3NzM4NiIsInByb2plY3RJZCI6Im5hdXMiLCJwcm92aWRlcklEIjoiYnJkYXlhdW9uQGdtYWlsLmNvbSIsInByb3ZpZGVyIjoiIn0.DGpBN1WbiJeZk97JkMdHIcQw6DguxSQe3uFYUanmmi4" # Your JWT token
client_key_value = "nw3b089qrgw9m7b7i" # Your client key

string_to_hash_for_xsign = str(current_t) + "," + client_key_value # This is 'o'
x_sign_hash = hashlib.md5(string_to_hash_for_xsign.encode('utf-8')).hexdigest()
x_sign_header_value = f"{x_sign_hash},{current_t}"

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {jwt_token}',
    'clientkey': client_key_value,
    'country': 'US',
    'did': 'a1iBd7l0-a365-A54t-941P-3Wu4dWC7422U',
    'grey-secret': 'null',
    'language': 'en',
    'origin': 'https://www.popmart.com',
    'priority': 'u=1, i',
    'referer': 'https://www.popmart.com/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'td-session-key': 'uWPU5174695562300IduTyCvP4', # Ensure this is current/valid
    'td-session-path': '/shop/v1/box/box_set/preview', # CRITICAL: This should match the path of the POST request for td-session-sign
    'td-session-query': '', # CRITICAL: If query_params_for_post is used, this needs to be the query string for td-session-sign
    'td-session-sign': 'w3348bc24ce2afddaf0a630fc80f713dd5Tq714JfluUDYOAAPGOGAIG2OegS922FYMIf0510324973eacc6c9c749110a1e3c4c7b3fda5ce744ee88a6b2a5aae7a84803c00001e1ba49f99869eb58b5cc242c0f237d15', # CRITICAL: This signature is tied to td-session-path and td-session-query
    'tz': 'America/Los_Angeles',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-client-country': 'US',
    'x-client-namespace': 'america',
    'x-device-os-type': 'web',
    'x-project-id': 'naus',
    # CRITICAL 'x-sign': The x-sign header string.
    # Example: 'c3190b48e4c1fe7fb920215f163a91b1,1746955624'
    # The first part is the hash, the second part is the timestamp.
    # This timestamp for x-sign (e.g., 1746955624 in your original headers for the GET)
    # MUST align with how the API expects it, especially if 't' is also in the payload.
    # If your x-sign was generated with timestamp 1746959257 (from your payload), it would be:
    # 'YOUR_GENERATED_HASH_FOR_POST_PAYLOAD,1746959257'
    'x-sign': x_sign_header_value, # Replace with the actual, correctly generated x-sign for this POST request
    # 'Content-Type' will be set to 'application/json' automatically by requests when using the `json` parameter.
}


# --- Update x-sign header based on payload's timestamp ---
# It's crucial that the timestamp in the x-sign header matches the 't' in your payload IF the API expects this consistency.
# If the 't' in x-sign MUST be int(time.time()), and 't' in payload is fixed, this could be an issue.
# Assuming the x-sign uses the 't' from the payload for this specific request:
payload_timestamp = post_payload['t']
# You would need to generate the hash part of x-sign using this payload_timestamp and other required elements.
# For this example, let's assume you have a function or method to get the hash:
# x_sign_hash = generate_x_sign_hash(post_payload, payload_timestamp, ...) # This is a placeholder for your actual signing logic
# headers['x-sign'] = f"{x_sign_hash},{payload_timestamp}"
# For now, ensure headers['x-sign'] is the correct one you have that corresponds to this payload.

print(f"Requesting URL (POST): {api_url_base}")
if query_params_for_post:
    print(f"With URL Query Params: {query_params_for_post}")
print(f"With JSON Payload: {json.dumps(post_payload, indent=2)}")
# print(f"With Headers: {json.dumps(headers, indent=2)}") # Uncomment to verify headers before sending


try:
    response = requests.post(api_url_base, params=query_params_for_post, json=post_payload, headers=headers, timeout=15)

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("\nResponse Text (first 500 chars):")
    print(response.text[:500] if response.text else "[No Response Text]")

    if response.status_code == 200 or response.status_code == 201: # Common success codes for POST
        try:
            data = response.json()
            print("\nSuccessfully parsed JSON:")
            print(json.dumps(data, indent=2))
        except requests.exceptions.JSONDecodeError as json_e:
            print(f"\nFailed to decode JSON: {json_e}")
    elif response.status_code == 400:
        print("\nReceived 400 Bad Request. The request payload might be malformed, missing required fields, or signatures are incorrect.")
        try:
            error_data = response.json()
            print("Error details from API:")
            print(json.dumps(error_data, indent=2))
        except requests.exceptions.JSONDecodeError:
            pass # No JSON in error response
    elif response.status_code == 401:
        print("\nReceived 401 Unauthorized. JWT or Clientkey might be wrong.")
    elif response.status_code == 403:
        print("\nReceived 403 Forbidden. Authenticated but not authorized, or signature issues (x-sign, td-session-sign).")
    elif response.status_code == 503:
        print("\nReceived a 503 Service Unavailable.")
    else:
        print(f"\nReceived unexpected status code: {response.status_code}")


except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the request: {e}")