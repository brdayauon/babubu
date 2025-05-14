import requests
import time
import json
import hashlib
import hmac # Keep for completeness if you still want to see other hash outputs

# --- Data obtained from your successful POST .../preview call for spuId = 2156 ---
# This is the JSON structure you provided.

current_t = int(time.time()) # This is 'n' from the JavaScript, used for X-Sign and payload's 't'

preview_json_from_user = {
    "code": "OK",
    "data": {
        "set_no": "10001394100585",
        "count": 6,
        "box_list": [
            {"box_info": {"position": 1, "state": 1, "box_no": "fleKkhM6uWkscZiVyLNX5g==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False},
            {"box_info": {"position": 2, "state": 1, "box_no": "3I+0MxtDp6p34GRcV/expA==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False},
            {"box_info": {"position": 3, "state": 1, "box_no": "Og7prCn7hXPEAVz7bCujJA==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False},
            {"box_info": {"position": 4, "state": 1, "box_no": "z+Vqovu48nEz6KDrrif7+A==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False},
            {"box_info": {"position": 5, "state": 1, "box_no": "I3kxae4VwbEAZe23ctegwQ==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False},
            {"box_info": {"position": 6, "state": 1, "box_no": "/7tFpU1b/gymuV/PhNtrIQ==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False}
        ],
        "width": 3,
        "height": 2,
        "price": 2799,
        "currency": "USD",
        "spu_id": 2156,
        "spu_ext_id": 195,
        "sku_id": 3336
    },
    "message": "success",
    "now": 1746962620, # Timestamp from when preview data was fetched
    "ret": 1
}
# --- End of data from /preview ---

# Extract the actual data part from the preview response
preview_data = preview_json_from_user.get("data", {})

# --- Configuration for POST addBoxListToCart ---
api_url_post_add_to_cart = "https://prod-global-api.popmart.com/shop/v1/box/boxCart/addBoxListToCart"

# Prepare the list of boxes to add to the cart
items_to_add_to_cart = []
if preview_data and "box_list" in preview_data:
    for box_item in preview_data["box_list"]:
        box_info = box_item.get("box_info", {})
        if box_info.get("state") == 1: # Only add if state is 1 (available)
            items_to_add_to_cart.append({
                "spu_ext_id": preview_data.get("spu_ext_id"),
                "spu_id": preview_data.get("spu_id"),
                "sku_id": preview_data.get("sku_id"),
                "set_no": preview_data.get("set_no"),
                "box_id": box_info.get("box_no"),
                "position": box_info.get("position")
            })

if items_to_add_to_cart:
    client_key_value = "nw3b089qrgw9m7b7i" # This is the ClientKey from the JavaScript

    # --- Correct X-Sign Calculation (Matches JavaScript's s() logic) ---
    string_to_hash_for_xsign = str(current_t) + "," + client_key_value
    x_sign_hash = hashlib.md5(string_to_hash_for_xsign.encode('utf-8')).hexdigest() # This is the MD5 hash
    x_sign_header_value = f"{x_sign_hash},{current_t}" # This is the "hash,timestamp" format for the X-Sign header
    # --- End of X-Sign Calculation ---

    # --- Testing Section ---
    print("--- HASH TESTING SECTION (using sMock and tMock) ---")

    sMock = "c4a731a86f6b9a6fc3deb56d44d056f0" # This is the expected MD5 hash for tMock and client_key_value
    tMock = "1746999031" # Example timestamp for mock testing

    # TRY WITH beginning and NO KEYVAL: 
    stringToHashForXSignMock = "{}W_ak^moHpMla" + str(tMock)  #+ "," + client_key_value
    x_sign_hash_mock = hashlib.md5(stringToHashForXSignMock.encode('utf-8')).hexdigest() # This is the MD5 hash
    print(x_sign_hash_mock + " sMock: " + sMock)

    print("--- END OF HASH TESTING SECTION ---\n")
    # --- End of Testing Section ---

    add_to_cart_payload = {
        "box_list": items_to_add_to_cart,
        "s": x_sign_hash, # This is the MD5 hash component of the X-Sign.
                          # Ensure this is the correct value expected by the API for the payload's 's' field.
        "t": current_t    # Using the current timestamp for the payload's 't' field
    }

    jwt_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6Im5hdXMiLCJ0eXAiOiJKV1QifQ.eyJnaWQiOiIyOTg3MDI0Iiwibmlja25hbWUiOiJicmRheWF1b24iLCJhdmF0YXIiOiIiLCJ2aXBMZXZlbCI6MCwicm9sZSI6IlVzZXIiLCJhcHBJRCI6MSwiYXBwQ29kZSI6MCwicHJvdmlkZXJUeXBlIjoiZ29vZ2xlIiwibG9naW5BdCI6MTc0MzQ3Njk1OSwic2hvd0lEIjoiODAwNjQ5OTE1OTAwNTM3Njg3NzM4NiIsInByb2plY3RJZCI6Im5hdXMiLCJwcm92aWRlcklEIjoiYnJkYXlhdW9uQGdtYWlsLmNvbSIsInByb3ZpZGVyIjoiIn0.DGpBN1WbiJeZk97JkMdHIcQw6DguxSQe3uFYUanmmi4" # Replace with your actual valid JWT token

    headers_for_add_to_cart_post = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd', # Modern browsers might send 'br, zstd', ensure your requests library handles or you adjust if issues arise
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {jwt_token}',
        'clientkey': client_key_value,
        'content-type': 'application/json',
        'country': 'US',
        'did': 'a1iBd7l0-a365-A54t-941P-3Wu4dWC7422U', # Ensure this is a valid or expected device ID
        'grey-secret': 'null', # If the actual value is string "null" or None (which requests might omit)
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
        # 'td-session-key': 'iWPUL1746959093zzZztm88px0', # These TD-Session headers are highly likely to be dynamic
        # 'td-session-path': '/shop/v1/box/boxCart/addBoxListToCart', # and tied to a specific session or pre-flight request.
        # 'td-session-query': '', # Hardcoding them might lead to errors.
        # 'td-session-sign': 'w3b14e37058b24b79a81a7489683217edetAIWTjB2JudyoaapgogaigEoDNsPEEfymi9091036e644860368dc8fa4503183be24e129408e015669f991a6c3b9b96617540000929bb11f6d1b3b11c2e0a5c49ebe4312a',
        'tz': 'America/Los_Angeles', # Ensure this matches the timezone context if critical
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-client-country': 'US',
        'x-client-namespace': 'america',
        'x-device-os-type': 'web',
        'x-project-id': 'naus',
        'x-sign': x_sign_header_value
    }

    print(f"Current Timestamp (current_t for X-Sign and payload): {current_t}")
    print(f"String to hash for X-Sign: {string_to_hash_for_xsign}")
    print(f"X-Sign Hash component (MD5): {x_sign_hash}")
    print(f"Full X-Sign Header Value: {x_sign_header_value}")

    print(f"\nRequesting POST to URL: {api_url_post_add_to_cart}")
    print(f"With Payload: {json.dumps(add_to_cart_payload, indent=2)}")
    # print(f"With Headers: {json.dumps(headers_for_add_to_cart_post, indent=2)}") # Uncomment for full header debugging

    try:
        response = requests.post(api_url_post_add_to_cart, headers=headers_for_add_to_cart_post, json=add_to_cart_payload, timeout=15)
        print(f"\nStatus Code: {response.status_code}")
        try:
            data = response.json()
            print("\nResponse JSON from addBoxListToCart:")
            print(json.dumps(data, indent=2))
        except json.JSONDecodeError:
            print("\nCould not parse JSON response from addBoxListToCart.")
            print(f"Response Text (first 500 chars): {response.text[:500] if response.text else '[No Response Text]'}")

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred during the request: {e}")

else:
    print("Could not prepare items to add to cart, preview data might be missing 'box_list' or it's empty.")