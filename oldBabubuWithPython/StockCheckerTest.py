import requests
import time
import json

# --- Configuration ---
# These values are from the specific successful browser request you provided
# Path: /shop/v1/shop/getSpuTpl?spuId=2156&s=e87674da26e8492a92bfc0db634e1f2b&t=1746955624
# x-sign header: c3190b48e4c1fe7fb920215f163a91b1,1746955624

api_url_base = "https://prod-global-api.popmart.com/shop/v1/box/box_set/preview"
spu_id = "2784"

# Use the exact 's' and 't' that corresponded to the successful header set
# If you run this script later, 't' will be old. For this test, we use the captured 't'.
# For ongoing success, 't' must be current, and 's' and 'x-sign' must be regenerated.
captured_t_param = 1746955624
captured_s_param = "e87674da26e8492a92bfc0db634e1f2b"
current_t = int(time.time())
params = {
    'spuId': spu_id,
    's': captured_s_param,
    't': current_t # Using the captured 't' that matches the captured x-sign
}

jwt_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6Im5hdXMiLCJ0eXAiOiJKV1QifQ.eyJnaWQiOiIyOTg3MDI0Iiwibmlja25hbWUiOiJicmRheWF1b24iLCJhdmF0YXIiOiIiLCJ2aXBMZXZlbCI6MCwicm9sZSI6IlVzZXIiLCJhcHBJRCI6MSwiYXBwQ29kZSI6MCwicHJvdmlkZXJUeXBlIjoiZ29vZ2xlIiwibG9naW5BdCI6MTc0MzQ3Njk1OSwic2hvd0lEIjoiODAwNjQ5OTE1OTAwNTM3Njg3NzM4NiIsInByb2plY3RJZCI6Im5hdXMiLCJwcm92aWRlcklEIjoiYnJkYXlhdW9uQGdtYWlsLmNvbSIsInByb3ZpZGVyIjoiIn0.DGpBN1WbiJeZk97JkMdHIcQw6DguxSQe3uFYUanmmi4"
client_key_value = "nw3b089qrgw9m7b7i"

headers = {
    # Pseudo-headers like :authority:, :method:, :path:, :scheme: are handled by requests
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd', # requests handles this, but can be specified
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {jwt_token}',
    'clientkey': client_key_value,
    'country': 'US',
    'did': 'a1iBd7l0-a365-A54t-941P-3Wu4dWC7422U', # Captured Device ID
    'grey-secret': 'null', # Sending as string 'null' as seen
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
    'td-session-key': 'uWPU5174695562300IduTyCvP4',         # Captured td-session-key
    'td-session-path': '/shop/v1/shop/getSpuTpl',       # Captured td-session-path
    'td-session-query': '',                             # Captured td-session-query (empty)
    'td-session-sign': 'w3348bc24ce2afddaf0a630fc80f713dd5Tq714JfluUDYOAAPGOGAIG2OegS922FYMIf0510324973eacc6c9c749110a1e3c4c7b3fda5ce744ee88a6b2a5aae7a84803c00001e1ba49f99869eb58b5cc242c0f237d15', # Captured td-session-sign
    'tz': 'America/Los_Angeles',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', # Exact User-Agent from capture
    'x-client-country': 'US',
    'x-client-namespace': 'america',
    'x-device-os-type': 'web',
    'x-project-id': 'naus',
    'x-sign': 'c3190b48e4c1fe7fb920215f163a91b1,1746955624' # Captured x-sign (hash,timestamp)
}

print(f"Requesting URL: {api_url_base}")
print(f"With Params: {params}")
# print(f"With Headers: {json.dumps(headers, indent=2)}") # Pretty print headers for verification

try:
    response = requests.get(api_url_base, params=params, headers=headers, timeout=15) # Increased timeout slightly

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("\nResponse Text (first 500 chars):")
    print(response.text[:500] if response.text else "[No Response Text]")

    if response.status_code == 200:
        try:
            data = response.json()
            print("\nSuccessfully parsed JSON:")
            print(json.dumps(data, indent=2))
        except requests.exceptions.JSONDecodeError as json_e:
            print(f"\nFailed to decode JSON: {json_e}")
    # ... (other status code handling from previous script) ...
    elif response.status_code == 401:
        print("\nReceived 401 Unauthorized. JWT or Clientkey might be wrong, or 's'/'t'/'x-sign' issues.")
    elif response.status_code == 403:
        print("\nReceived 403 Forbidden. Authenticated but not authorized, or signature issues.")
    elif response.status_code == 503:
        print("\nReceived a 503 Service Unavailable.")


except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred during the request: {e}")