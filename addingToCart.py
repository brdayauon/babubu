import requests
import time
import json
import time
import hashlib

# --- Data obtained from your successful POST .../preview call for spuId = 2156 ---
# This is the JSON structure you provided.

current_t = int(time.time()) # This is 'n' from the JavaScript

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
            {"box_info": {"position": 5, "state": 1, "box_no": "I3kxae4VwbEAZe23ctegwQ==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False}, # Corrected structure assuming item 5 was similar
            {"box_info": {"position": 6, "state": 1, "box_no": "/7tFpU1b/gymuV/PhNtrIQ==", "is_locked_by_me": False, "is_shaken": False}, "tips": [], "in_shopping_cart": False}  # Corrected structure assuming item 6 was similar
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
        # Optionally, you might want to check if box_info["state"] == 1 (available)
        if box_info.get("state") == 1: # Only add if state is 1 (available)
            items_to_add_to_cart.append({
                "spu_ext_id": preview_data.get("spu_ext_id"),
                "spu_id": preview_data.get("spu_id"),
                "sku_id": preview_data.get("sku_id"),
                "set_no": preview_data.get("set_no"),
                "box_id": box_info.get("box_no"),      # This is the specific ID for each box instance
                "position": box_info.get("position")
            })

if items_to_add_to_cart:
    # Construct the full payload for addBoxListToCart
    # These 's' and 't' values are from your captured addBoxListToCart POST request's payload
    # The 't' (1746959270) is now over an hour old from current time (Sun, 11 May 2025 ~11:37 GMT).
    # This might be too old for the server to accept.
    add_to_cart_payload = {
        "box_list": items_to_add_to_cart,
        "s": "f78e97c34517740354984288b9b3b89b",
        "t": current_t  # This 't' should ideally be current and match the timestamp in x-sign
    }

    # Headers for THIS SPECIFIC addBoxListToCart POST request (from your capture)
    jwt_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6Im5hdXMiLCJ0eXAiOiJKV1QifQ.eyJnaWQiOiIyOTg3MDI0Iiwibmlja25hbWUiOiJicmRheWF1b24iLCJhdmF0YXIiOiIiLCJ2aXBMZXZlbCI6MCwicm9sZSI6IlVzZXIiLCJhcHBJRCI6MSwiYXBwQ29kZSI6MCwicHJvdmlkZXJUeXBlIjoiZ29vZ2xlIiwibG9naW5BdCI6MTc0MzQ3Njk1OSwic2hvd0lEIjoiODAwNjQ5OTE1OTAwNTM3Njg3NzM4NiIsInByb2plY3RJZCI6Im5hdXMiLCJwcm92aWRlcklEIjoiYnJkYXlhdW9uQGdtYWlsLmNvbSIsInByb3ZpZGVyIjoiIn0.DGpBN1WbiJeZk97JkMdHIcQw6DguxSQe3uFYUanmmi4"
    client_key_value = "nw3b089qrgw9m7b7i"

    string_to_hash_for_xsign = str(current_t) + "," + client_key_value # This is 'o'
    x_sign_hash = hashlib.md5(string_to_hash_for_xsign.encode('utf-8')).hexdigest()
    x_sign_header_value = f"{x_sign_hash},{current_t}"

    headers_for_add_to_cart_post = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {jwt_token}',
        'clientkey': client_key_value,
        'content-type': 'application/json',
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
        'td-session-key': 'iWPUL1746959093zzZztm88px0',
        'td-session-path': '/shop/v1/box/boxCart/addBoxListToCart',
        'td-session-query': '',
        'td-session-sign': 'w3b14e37058b24b79a81a7489683217edetAIWTjB2JudyoaapgogaigEoDNsPEEfymi9091036e644860368dc8fa4503183be24e129408e015669f991a6c3b9b96617540000929bb11f6d1b3b11c2e0a5c49ebe4312a',
        'tz': 'America/Los_Angeles',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-client-country': 'US',
        'x-client-namespace': 'america',
        'x-device-os-type': 'web',
        'x-project-id': 'naus',
        # This x-sign (and its timestamp) also corresponds to the captured addBoxListToCart POST.
        # It's now over an hour old.
        'x-sign': x_sign_header_value
    }
    # e90086d7e016bc18b37af56243f8f356,1746962969

    print(f"Requesting POST to URL: {api_url_post_add_to_cart}")
    print(f"With Payload: {json.dumps(add_to_cart_payload, indent=2)}")
    # print(f"With Headers: {json.dumps(headers_for_add_to_cart_post, indent=2)}")

    try:
        response = requests.post(api_url_post_add_to_cart, headers=headers_for_add_to_cart_post, json=add_to_cart_payload, timeout=15)
        print(f"\nStatus Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\nSuccessfully parsed JSON response from addBoxListToCart:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Response Text (first 500 chars): {response.text[:500] if response.text else '[No Response Text]'}")
            print(f"Full Response Text: {response.text}")


    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred during the request: {e}")

else:
    print("Could not prepare items to add to cart, preview data might be missing 'box_list' or it's empty.")