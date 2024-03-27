import json
import hashlib
import os

secrets = {
    "secret-test": "secret-value",
    "another-secret": "another-value"
}

HMAC_SECRET = os.getenv('HMAC_SECRET', '123456')
SECRETS_JSON = os.getenv('ALLSECRETS', json.dumps(secrets))


def hmac_hash_secrets(secrets_json: str, hmac_secret: str) -> str:
    """
    This function takes a JSON string and an HMAC secret (from environment),
    hashes each value using HMAC-SHA256 with the secret,
    and returns the modified JSON string.
    """
    try:
        secrets_dict = json.loads(secrets_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")

    if not hmac_secret:
        raise ValueError("Missing HMAC_SECRET environment variable")

    for key, value in secrets_dict.items():
        hashed_value = hashlib.sha256((str(value).encode() + hmac_secret.encode()).strip()).hexdigest()
        secrets_dict[key] = hashed_value

    return json.dumps(secrets_dict)


def main():
    secrets_hmac_values = hmac_hash_secrets(SECRETS_JSON, HMAC_SECRET)
    print(secrets_hmac_values)


if __name__ == '__main__':
    main()
