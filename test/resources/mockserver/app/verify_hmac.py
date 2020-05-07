import hmac, hashlib, json, time, base64, urllib
import codecs


SHARED_SECRET = 'sup3rs3cr3t!!'

# TODO: this doesn't work, auth fails with veracode generated auth string
def verifyAuthorization(signing_data, authorization, api_key_secret):
    # parse authorization
    # VERACODE-HMAC-SHA-256 id=3ddaeeb10ca690df3fee5e3bd1c329fa,ts=1588878918722,nonce=a8d7fdb5aa22fc3fdb688fbb6807c2b4,sig=055490fe1aba6c309205ef5322b37a77a9de0646a318de23699e69ce4c5cb9d4

    sig = authorization[authorization.index('sig='):]

    return verifySignature(signing_data, sig, api_key_secret)


def verifySignature(string_to_verify, signature, shared_secret):
	return ct_compare(
        hmac.new(
            codecs.encode(shared_secret), 
		    codecs.encode(string_to_verify), 
            hashlib.sha512).digest(), 
        signature)


def verifyTime(decoded_json):
	j = json.loads(decoded_json)

	if int(time.time()) - int(j['timestamp']) > 30:
		raise Exception('Timestamp too far in the past')

	return j


def ct_compare(a, b):
	"""
	** From Django source **

	Run a constant time comparison against two strings

	Returns true if a and b are equal.

	a and b must both be the same length, or False is 
	returned immediately
	"""
	if len(a) != len(b):
		return False

	result = 0
	for ch_a, ch_b in zip(a, b):
		result |= ord(ch_a) ^ ord(ch_b)
	return result == 0


if __name__ == '__main__':
	url = '[QUERYSTRING]'
	query = urlparse.parse_qs(urlparse.urlparse(url).query)
	decoded_signature = base64.urlsafe_b64decode(query['signature'][0])
	decoded_json = base64.urlsafe_b64decode(query['data'][0])

	if verifySignature(decoded_json, decoded_signature, SHARED_SECRET) is True:
		print('Valid signature')

		# Verify timestamp
		payload = verifyTime(decoded_json)
		print('Timestamp verified')
		print(payload)

	else:
		print('Invalid signature')