import json


def create_headers(access_token):
    headers = dict()
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers


def signin(client, credentials):
    response = client.post("/users/signin", json=credentials)
    json_response = response.get_json()

    return response, json_response


def signup(client, credentials):
    response = client.post("/users/signup", json=credentials)
    json_response = response.get_json()

    return response, json_response


