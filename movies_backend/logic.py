import hashlib
import json
import base64


def dict_to_token(data):
    data_str = json.dumps(data, sort_keys=True)
    hashed_data = hashlib.sha256(data_str.encode()).hexdigest()
    token = base64.b64encode(hashed_data.encode()).decode()

    return token


def token_to_dict(token):
    decoded_hash = base64.b64decode(token).decode()
    print(decoded_hash)
    token_dict = json.loads(decoded_hash)
    print(token_dict)

    return token_dict
