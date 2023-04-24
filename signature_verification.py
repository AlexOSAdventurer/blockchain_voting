from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import traceback
import base64

#Public-key is an RSA public-key string
#Msg is a String
#Signature is a base64 encoded string
def verify_signature(public_key, msg, signature):
	public_key = RSA.import_key(public_key)
	hash = SHA256.new(msg.encode())
	verifier = pkcs1_15.new(public_key)
	try:
		signature = base64.b64decode(signature.encode())
		verifier.verify(hash, signature)
		return True
	except Exception as e:
		print(e)
		traceback.print_exc()
		return False
