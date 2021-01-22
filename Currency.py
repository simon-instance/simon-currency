import time
import random
import hashlib

class Block:
    def __init__(self, is_genesis = False, prev_hash = None, hash = None, proof = None):
        self.is_genesis = is_genesis
        self.prev_hash = prev_hash
        self.date_time = time.time()
        self.hash = hash
        self.proof = proof
    
    def proof_of_work(self, node_signature) -> bool:
        nonse = 1
        while True:
            nonse += random.randint(0, 15)
            resolvable = hashlib.sha512(f"{node_signature}{self.date_time}{nonse}".encode()).hexdigest()
            
            calc = str(round(nonse / (nonse*random.randint(2, 30000) - (nonse/2)) * 10000000))

            if resolvable.startswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}") and resolvable.endswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}"):
                self.hash = resolvable
                self.proof = 0
                return True
        return False

class BlockChain:
    def __init__(self, node_signature):
        self.node_signature = node_signature
        self.mining_rewards = 30
        self.chain = [self.add_genesis_block()]
        self.transactions = []

    def add_genesis_block(self) -> Block:
        block = Block(is_genesis=True)

        if block.proof_of_work(self.node_signature):
            return block

        raise Exception("Failed to validate proof of work")

    @property
    def last_block(self):
        self.chain[-1]