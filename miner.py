import time
import random
import hashlib
import requests
import json

from miner_conf import NETWORK_NODES

class Block:
    def __init__(self, is_genesis = False, prev_hash = None, hash = None, proof = None):
        self.is_genesis = is_genesis
        self.prev_hash = prev_hash
        self.date_time = time.time()
        self.hash = hash
        self.proof = proof

    def proof_of_work(self, node_signature, chain, last_block: Block) -> bool:
        current_proof = last_block.proof
        proof = self.start_mining(node_signature, chain)
        print(f"{proof}")
        return proof

    def start_mining(self, node_signature, chain) -> str:
        nonse = 1
        proof_hash = None

        start_time = time.time()

        while (proof_hash == None):
            nonse += random.randint(0, 15)
            resolvable = hashlib.sha512(f"{node_signature}{self.date_time}{nonse}".encode('utf-8')).hexdigest()
            
            calc = str(round(nonse / (nonse*random.randint(2, 30000) - (nonse/2)) * 10000000))

            # Every minute check for unsynced possibly mined blocks from other nodes
            if (time.time() - start_time) % 60 == 0:
                # If a genesis block has been mined (start of a blockchain), cancel this mining process and start over
                new_blockchain_mined = Node.consensus(chain)

            if resolvable.startswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}") and resolvable.endswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}"):
                self.hash = resolvable
                self.proof = 0
                # Hash has been found by the computer
                proof_hash = resolvable
        
        return proof_hash


class BlockChain:
    def __init__(self, node_signature):
        self.node_signature = node_signature
        self.mining_rewards = 30
        self.chain = [self.add_genesis_block()]
        self.transactions = []

    def add_genesis_block(self) -> Block:
        block = Block(is_genesis=True)

        if block.proof_of_work(self.node_signature, self.chain, self.last_block):
            return block

        raise Exception("Failed to validate proof of work")

    @property
    def last_block(self):
        self.chain[-1]


class Node:
    @staticmethod
    def get_network_chains():
        network_chains = []

        for node in NETWORK_NODES:
            # Chain requested from node API
            chain = requests.get(f'{node}/all-blocks').content
            chain = json.loads(chain)
            network_chains.append(chain)

        return network_chains

    @staticmethod
    def consensus(blockchain):
        network_chains = Node.get_network_chains()

        # Keep longest chain our chain for now...
        longest_chain = blockchain
        for chain in network_chains:
            # When length of our chain is not the largest, change the largest chain to the remote network chain received from an API
            if len(blockchain) < len(chain):
                lonegst_chain = chain