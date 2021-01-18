import json


def signin(client, credentials):
    response = client.post("/users/signin", headers={'Content-Type': 'application/json'}, data=json.dumps(credentials))
    json_response = response.get_json()

    return response, json_response