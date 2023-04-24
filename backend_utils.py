class Backend:
	def __init__(self, root_folder):
		self.root_folder = root_folder
		print(f"Storing persistent data for backend in {self.root_folder}")
		self.elections = {}
		self.voters = {}

	def get_public_key(self, username):
		user = self.get_user(username)
		if user is not None:
			return user["public_key"]
		return None

	def get_user(self, username):
		if username in self.voters:
			return self.voters[username]

	def get_user_list(self):
		return list(self.voters.values())

	def set_user(self, username, public_key):
		self.voters[username] = {"username": username, "public_key": public_key}

	def set_election(self, name, prompt, user, signature):
		self.elections[name] = {"name": name, "prompt": prompt, "user": user, "signature": signature, "yays": [], "nays": []}

	def get_election(self, name, preserve_votes=False):
		if name in self.elections:
			result = self.elections[name].copy()
			if (not preserve_votes):
				result["yays"] = len(result["yays"])
				result["nays"] = len(result["nays"])
			return result

	def get_election_list(self):
		result = []
		for k in self.elections:
			result.append(self.get_election(k))
		return result

	def valid_vote(self, name, username, vote):
		election = self.get_election(name, preserve_votes=True)
		return (username not in election["yays"]) and (username not in election["nays"])

	def increment_election(self, name, username, vote):
		self.elections[name][vote].append(username)
