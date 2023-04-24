import sys
from Crypto.Signature import pss, pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from flask import Flask, jsonify, request
import traceback
import base64

app = Flask(__name__)

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

elections = {}
voters = {}

def get_user(username):
	if username in voters:
		return voters[username]

def get_user_list():
	return list(voters.values())

def set_user(username, public_key):
	voters[username] = {"username": username, "public_key": public_key}

@app.route('/add_user', methods=['GET'])
def add_user():
	username = request.args.get("username")
	public_key = request.args.get("public_key")
	response = (get_user(username) is None)
	if (response):
		set_user(username, public_key)
	result = {"username": username, "public_key": public_key, "response": response}
	return jsonify(result);

@app.route('/get_users', methods=['GET'])
def get_users():
	return jsonify(get_user_list());

def set_election(name, prompt, user, signature):
	elections[name] = {"name": name, "prompt": prompt, "user": user, "signature": signature, "yays": [], "nays": []}

def get_election(name, preserve_votes=False):
	if name in elections:
		result = elections[name].copy()
		if (not preserve_votes):
			result["yays"] = len(result["yays"])
			result["nays"] = len(result["nays"])
		return result

def get_election_list():
	result = []
	for k in elections:
		result.append(get_election(k))
	return result

@app.route('/get_elections', methods=['GET'])
def get_elections():
	return jsonify(get_election_list())

@app.route('/add_election', methods=['GET'])
def add_election():
	name = request.args.get("name")
	prompt = request.args.get("prompt")
	username = request.args.get("username")
	signature = request.args.get("signature")
	response = verify_signature(default_public_key, name + prompt + username, signature) and (get_election(name) is None)
	if (response):
		set_election(name, prompt, username, signature)
	result = {"name": request.args.get("name"), "prompt": prompt, "username": username, "signature": signature, "response": response}
	if (response):
		pass
	return jsonify(result);

def valid_vote(name, username, vote):
	election = get_election(name, preserve_votes=True)
	return (username not in election["yays"]) and (username not in election["nays"])

def increment_election(name, username, vote):
	elections[name][vote].append(username)

@app.route('/add_vote', methods=['GET'])
def add_vote():
	name = request.args.get("name")
	username = request.args.get("username")
	vote = request.args.get("vote")
	signature = request.args.get("signature")
	response = verify_signature(default_public_key, name + username + vote, signature) and valid_vote(name, username, vote)
	if (response):
		increment_election(name, username, vote)
	result = {"name": name, "username": username, "vote": vote, "signature": signature, "response": response}
	return jsonify(result);

if __name__ == '__main__':
	app.config['data_folder'] = sys.argv[1]
	port = sys.argv[2]
	app.run(debug=True, host="0.0.0.0", port=port)
