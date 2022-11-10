import json, hmac, hashlib, requests

def get_digest(key, data):
  secret = bytes(key.encode('utf8'))
  data = json.dumps(dict(data), separators=(',', ':')).encode('utf8')
  hash = hmac.new(key=secret, digestmod=hashlib.sha512)
  hash.update(data)
  digest = hash.hexdigest()
  return digest