import json
from blockchain import Blockchain

class Backend:
	def __init__(self, root_folder):
		self.root_folder = root_folder
		print(f"Storing persistent data for backend in {self.root_folder}")
		self.blockchain = Blockchain(self.root_folder)

	def get_head_block(self):
		head_hash = self.blockchain.get_longest_chain()
		return self.blockchain.get_block(head_hash)

	def fork_head_block(self):
		head_hash = self.blockchain.get_longest_chain()
		forked_block = self.blockchain.fork_block(head_hash)
		forked_block["state"] = json.loads(forked_block["state"])
		return forked_block

	def commit_forked_block(self, forked_block):
		forked_block["state"] = json.dumps(forked_block["state"])
		forked_block["transition"] = json.dumps(forked_block["transition"])
		self.blockchain.commit_block(forked_block)

	def get_current_state(self):
		data = self.get_head_block()
		parsedData = json.loads(data["state"])
		return parsedData

	def get_user(self, username):
		parsedData = self.get_current_state()
		if username in parsedData["voters"]:
			return parsedData["voters"][username]

	def get_public_key(self, username):
		user = self.get_user(username)
		if user is not None:
			return user["public_key"]
		return None

	def get_user_list(self):
		parsedData = self.get_current_state()
		return list(parsedData["voters"].values())

	def get_election(self, name, preserve_votes=False):
		parsedData = self.get_current_state()
		if name in parsedData["elections"]:
			result = parsedData["elections"][name].copy()
			if (not preserve_votes):
				result["yays"] = len(result["yays"])
				result["nays"] = len(result["nays"])
			return result

	def get_election_list(self):
		parsedData = self.get_current_state()
		result = []
		for k in parsedData["elections"]:
			result.append(self.get_election(k))
		return result

	def valid_vote(self, name, username, vote):
		election = self.get_election(name, preserve_votes=True)
		return (username not in election["yays"]) and (username not in election["nays"])

	def set_user(self, username, public_key):
		forked_block = self.fork_head_block()
		forked_block["state"]["voters"][username] = {"username": username, "public_key": public_key}
		forked_block["transition"] = {"action": "set_user", "username": username, "public_key": public_key}
		self.commit_forked_block(forked_block)

	def set_election(self, name, prompt, username, signature):
		forked_block = self.fork_head_block()
		forked_block["state"]["elections"][name] = {"name": name, "prompt": prompt, "username": username, "signature": signature, "yays": [], "nays": []}
		forked_block["transition"] = {"action": "set_election", "name": name, "prompt": prompt, "username": username, "signature": signature}
		self.commit_forked_block(forked_block)

	def increment_election(self, name, username, vote, signature):
		forked_block = self.fork_head_block()
		forked_block["state"]["elections"][name][vote].append(username)
		forked_block["transition"] = {"action": "increment_election", "name": name, "username": username, "vote": vote, "signature": signature}
		self.commit_forked_block(forked_block)
