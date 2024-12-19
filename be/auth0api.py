import json
import http.client

token_request_conn = http.client.HTTPSConnection("token_request_conn")

token_request_payload = "{\"client_id\":\"YOUR CLIENT ID\",\"client_secret\":\"YOUR CLIENT SECRET\",\"audience\":\"YOUR AUDIENCE\",\"grant_type\":\"client_credentials\"}"

token_request_headers = { 'content-type': "application/json" }

token_request_conn.request("POST", "/oauth/token", token_request_payload, token_request_headers)

res = token_request_conn.getresponse()
data = res.read()
token_decoded = json.loads(data.decode("utf-8"))  # Decode JSON response

access_token = token_decoded["access_token"]

api_conn = http.client.HTTPSConnection("api_conn")
api_headers = {
    'authorization': f"Bearer {access_token}",
}

def delete_user(user_id):
    api_conn.request("DELETE", f"/api/v2/users/{user_id}", headers=api_headers)
    res = api_conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def update_user_password(user_id, new_password):
    payload = json.dumps({
        "password": new_password,
    })
    api_headers1 = {
    'authorization': f"Bearer {access_token}",
    'content-type': "application/json"
    }
    api_conn.request("PATCH", f"/api/v2/users/{user_id}", payload, headers=api_headers1)
    res = api_conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def user_update_email(user_id, new_email):
    payload = json.dumps({
        "email": new_email,
    })
    api_headers1 = {
    'authorization': f"Bearer {access_token}",
    'content-type': "application/json"
    }
    api_conn.request("PATCH", f"/api/v2/users/{user_id}", payload, headers=api_headers1)
    res = api_conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


