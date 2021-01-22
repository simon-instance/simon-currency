import time

class Block:
    def __init__(self, is_genesis = False, prev_hash = None):
        self.isGenesis = is_genesis
        self.prev_hash = prev_hash
        self.date_time = time.time()

class BlockChain:
    def __init__(self, node_signature):
        self.node_signature = node_signature
        self.mining_rewards = 30
        self.chain = [self.add_genesis_block()]
        self.transactions = []

    def add_genesis_block(self) -> Block:
        return Block(is_genesis=True)
