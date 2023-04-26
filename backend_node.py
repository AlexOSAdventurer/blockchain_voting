import sys
from flask import Flask, jsonify, request
from signature_verification import verify_signature
from backend_utils import Backend

app = Flask(__name__)
internal_state = None

@app.route('/add_user', methods=['GET'])
def add_user():
	username = request.args.get("username")
	public_key = request.args.get("public_key")
	response = (internal_state.get_user(username) is None)
	if (response):
		internal_state.set_user(username, public_key)
	result = {"username": username, "public_key": public_key, "response": response}
	return jsonify(result);

@app.route('/get_users', methods=['GET'])
def get_users():
	return jsonify(internal_state.get_user_list());

@app.route('/get_elections', methods=['GET'])
def get_elections():
	return jsonify(internal_state.get_election_list())

@app.route('/add_election', methods=['GET'])
def add_election():
	name = request.args.get("name")
	prompt = request.args.get("prompt")
	username = request.args.get("username")
	signature = request.args.get("signature")
	response = verify_signature(internal_state.get_public_key(username), name + prompt + username, signature) and (internal_state.get_election(name) is None)
	if (response):
		internal_state.set_election(name, prompt, username, signature)
	result = {"name": request.args.get("name"), "prompt": prompt, "username": username, "signature": signature, "response": response}
	return jsonify(result);

@app.route('/add_vote', methods=['GET'])
def add_vote():
	name = request.args.get("name")
	username = request.args.get("username")
	vote = request.args.get("vote")
	signature = request.args.get("signature")
	response = verify_signature(internal_state.get_public_key(username), name + username + vote, signature) and internal_state.valid_vote(name, username, vote)
	if (response):
		internal_state.increment_election(name, username, vote, signature)
	result = {"name": name, "username": username, "vote": vote, "signature": signature, "response": response}
	return jsonify(result);

if __name__ == '__main__':
	app.config['data_folder'] = sys.argv[1]
	internal_state = Backend(app.config['data_folder'])
	port = sys.argv[2]
	app.run(debug=False, host="0.0.0.0", port=port)
