import sys
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/add_vote', methods=['GET'])
def add_vote():
	result = {"name": request.args.get("name"), "username": request.args.get("username"), "vote": request.args.get("vote"), "signature": request.args.get("signature"), "response": True}
	return jsonify(result);

@app.route('/add_election', methods=['GET'])
def add_election():
	result = {"name": request.args.get("name"), "prompt": request.args.get("prompt"), "username": request.args.get("username"), "signature": request.args.get("signature"), "response": True}
	return jsonify(result);

@app.route('/add_user', methods=['GET'])
def add_user():
	result = {"username": request.args.get("username"), "public_key": request.args.get("public_key"), "response": True}
	return jsonify(result);

@app.route('/get_users', methods=['GET'])
def get_users():
	user1 = {"name": "abad", "public_key": "asdfasdf"};
	user2 = {"name": "abd", "public_key": "adsfasdg"};
	user3 = {"name": "ab3rd", "public_key": "dhjkhh"};
	user4 = {"name": "aba3", "public_key": "dsgjilgr"};
	return jsonify([user1, user2, user3, user4]);

@app.route('/get_elections', methods=['GET'])
def get_elections():
	election1 = {"name": "Penn", "prompt": "Going in!", "user": "abad", "yays": 10, "nays": 2};
	election2 = {"name": "Nebraska", "prompt": "Going in 2!", "user": "abd", "yays": 5, "nays": 2};
	election3 = {"name": "Yugo", "prompt": "Going in 3!", "user": "aba3", "yays": 3, "nays": 9};
	election4 = {"name": "Tenn", "prompt": "Going in 4!", "user": "ab3rd", "yays": 27, "nays": 4};
	return jsonify([election1, election2, election3, election4])

if __name__ == '__main__':
	app.config['data_folder'] = sys.argv[1]
	port = sys.argv[2]
	app.run(debug=True, host="0.0.0.0", port=port)
