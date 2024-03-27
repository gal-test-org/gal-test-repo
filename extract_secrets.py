import json
import hashlib
import os

HMAC_SECRET = os.getenv('HMAC_SECRET')
SECRETS_JSON = os.getenv('ALLSECRETS')


def hmac_hash_secrets(secrets_json:str, hmac_secret:str):
  """
  This function takes a JSON string and an HMAC secret (from environment), 
  hashes each value using HMAC-SHA256 with the secret, 
  and returns the modified JSON string.
  """
  try:
    secrets_dict = json.loads(secrets_json)
  except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON input: {e}")

  hmac_secret = os.environ.get("HMAC_SECRET")
  if not hmac_secret:
    raise ValueError("Missing HMAC_SECRET environment variable")

  for key, value in secrets_dict.items():
    hashed_value = hashlib.sha256((str(value).encode() + hmac_secret.encode()).strip()).hexdigest()
    secrets_dict[key] = hashed_value

  return json.dumps(secrets_dict)

def main():
  hmac_hash_secrets(HMAC_SECRET, SECRETS_JSON)

if __name__ == '__main__':
  main()