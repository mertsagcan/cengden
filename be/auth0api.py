import json
import http.client

token_request_conn = http.client.HTTPSConnection("dev-bgni6r2aiwkt4xgt.us.auth0.com")

token_request_payload = "{\"client_id\":\"GMUL2XNE7KctLcwwRNmsE8Yorj1uv1mB\",\"client_secret\":\"WIWh9Qgs5Bu8P5P9m_hOdF27pnOinSRa1QQ2SMRucmQySsUFh9B25SDmDUNp0pTC\",\"audience\":\"https://dev-bgni6r2aiwkt4xgt.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"

token_request_headers = { 'content-type': "application/json" }

token_request_conn.request("POST", "/oauth/token", token_request_payload, token_request_headers)

res = token_request_conn.getresponse()
data = res.read()
token_decoded = json.loads(data.decode("utf-8"))  # Decode JSON response

access_token = token_decoded["access_token"]

api_conn = http.client.HTTPSConnection("dev-bgni6r2aiwkt4xgt.us.auth0.com")
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


