
import json
import random
from Crypto.Hash import SHA256
import threading

# Blocks have these fields:
# state - JSON string
# transition - JSON string
# prev_hash - hex string
# current_hash - hex string
# nonce - 64-bit integer

commented_out = """def proof_of_work(msg, nonce=None, numberOfZeros=2):
    if nonce is None:
        nonce = random.getrandbits(64)
    while True:
        hash = SHA256.new((msg + str(nonce)).encode()).hexdigest()
        endPiece = hash[(numberOfZeros*-1):]
        totalZeros = 0
        for k in endPiece:
            totalZeros = totalZeros + (1 if k == "0" else 0)
        if (totalZeros == numberOfZeros):
            break
        nonce = nonce + 1
    return nonce"""

class Blockchain:
	def __init__(self, root_folder, start_new=True):
		self.root_folder = root_folder
		print(f"Storing persistent data for blockchain in {self.root_folder}")
		self.access_lock = threading.Lock()
		self.blocks = {}
		#self.rootBlockHashName = "ZGFSb290QmxvY2s=" #daRootBlock
		if (start_new):
			new_block = {}
			new_block["state"] = json.dumps({"elections": {}, "voters": {}})
			new_block["transition"] = json.dumps({"action": "root_block"})
			new_block["prev_hash"] = ""
			self.proof_of_work(new_block, nonce=0)
			new_block["new_hash"] = self.compute_block_hash(new_block)
			self.rootBlockHashName = new_block["new_hash"]
			print(f"Root blockchcain hash is {self.rootBlockHashName}")
			self.base_commit_block(new_block)

	def compute_block_hash(self, block):
		current_string = (block["state"] + block["transition"] + block["prev_hash"] + str(block["nonce"])).encode()
		return SHA256.new(current_string).hexdigest()

	# numberOfZeros is the number of hex zeros - so it's basically multiplied by four for the total number of bits
	# on the server this usually takes about 1 second to run with the default parameters
	def proof_of_work(self, block, nonce=None, numberOfZeros=4):
		if nonce is None:
			nonce = random.getrandbits(64)
		block["nonce"] = nonce
		while True:
			hash = self.compute_block_hash(block)
			endPiece = hash[(numberOfZeros*-1):]
			totalZeros = 0
			for k in endPiece:
				totalZeros = totalZeros + (1 if k == "0" else 0)
			if (totalZeros == numberOfZeros):
				break
			block["nonce"] = block["nonce"] + 1
		print("nonce: ", block["nonce"])

	# Currently have to traverse the entire list to get the children.
	def getBlockChildren(self, chain_head_hash):
		result = []
		for block in self.blocks:
			if (self.blocks[block]["prev_hash"] == chain_head_hash):
				result.append(block)
		return result

	# Currently we have to travel from the root, all the way down to get all chains. Kinda sucks, I know.
	def get_chains(self, hash_root):
		current_chains = [[hash_root]]
		extended = True
		while extended:
			print("Chains: ", current_chains)
			extended = False
			new_chain_list = []
			for chain in current_chains:
				chain_head = chain[-1]
				children = self.getBlockChildren(chain_head)
				for child in children:
					new_chain = chain + [child]
					new_chain_list.append(new_chain)
					extended = True
			if extended:
				current_chains = new_chain_list
		return current_chains

	def get_longest_chain(self):
		self.access_lock.acquire()
		chains = self.get_chains(self.rootBlockHashName)
		current_longest = None
		for chain in chains:
			if ((current_longest is None) or (len(current_longest) < len(chain))):
				current_longest = chain
		self.access_lock.release()
		return current_longest[-1]

	def get_block(self, block_hash):
		self.access_lock.acquire()
		result = self.blocks[block_hash]
		self.access_lock.release()
		return result

	def fork_block(self, block_hash):
		self.access_lock.acquire()
		new_block = self.blocks[block_hash].copy()
		new_block["prev_hash"] = new_block["new_hash"]
		self.access_lock.release()
		return new_block

	def base_commit_block(self, block):
		self.blocks[block["new_hash"]] = block

	def commit_block(self, block):
		print(block)
		self.access_lock.acquire()
		self.proof_of_work(block)
		block["new_hash"] = self.compute_block_hash(block)
		self.base_commit_block(block)
		self.access_lock.release()
