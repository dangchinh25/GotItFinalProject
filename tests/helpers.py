import json


def create_headers(access_token=None):
    headers = {'Content-Type': 'application/json'}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers


def signin(client, credentials):
    response = client.post("/users/signin", headers=create_headers(), data=json.dumps(credentials))
    json_response = response.get_json()

    return response, json_response


def signup(client, credentials):
    response = client.post("/users/signup", headers=create_headers(), data=json.dumps(credentials))
    json_response = response.get_json()

    return response, json_response


def create_category(client, credentials, category_name):
    _, signin_response = signin(client, credentials)
    access_token = signin_response["access_token"]

    response = client.post("/categories", headers=create_headers(access_token), data=json.dumps({"name": category_name}))
    json_response = response.get_json()

    return response, json_response


def put_item(client, credentials, item_id, data):
    _, signin_response = signin(client, credentials)
    access_token = signin_response["access_token"]

    response = client.put(f"/items/{item_id}", headers=create_headers(access_token), data=json.dumps(data))
    json_response = response.get_json()

    return response, json_response


def delete_item(client, credentials, item_id):
    _, signin_response = signin(client, credentials)
    access_token = signin_response["access_token"]

    response = client.delete(f"/items/{item_id}", headers=create_headers(access_token))

    return response


def create_item(client, credentials, category_id,data):
    _, signin_response = signin(client, credentials)
    access_token = signin_response["access_token"]

    response = client.post(f"/categories/{category_id}/items", headers=create_headers(access_token), data=json.dumps(data))
    json_response = response.get_json()

    return response, json_response