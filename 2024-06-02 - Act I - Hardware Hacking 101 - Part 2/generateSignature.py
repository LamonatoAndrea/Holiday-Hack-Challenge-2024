import hmac
import hashlib
secret_key = b"9ed1515819dec61fd361d5fdabb57f41ecce1a5fe1fe263b98c0d6943b9b232e"
access_uuid = b"1c06018b6-5e80-4395-ab71-ae5124560189"
signature = hmac.new(secret_key, access_uuid, hashlib.sha256).hexdigest()
print("signature = {0}".format(signature))