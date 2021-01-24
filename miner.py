import time
import random
import hashlib
import requests
import json

from multiprocessing import Pipe, Process

from api_conf import NETWORK_NODES, NODE_API_URL, MINER_ADDRESS

class Block:
    def __init__(self, node, proof, is_genesis = False, prev_hash = None, hash = None):
        self.is_genesis = is_genesis
        self.prev_hash = prev_hash
        self.date_time = time.time()
        self.hash = hash
        self.proof = proof
        self.node = node

    def proof_of_work(self, node_signature, chain, last_block: Block) -> bool:
        mining_result = [False] 

        # If our blockchain isn't the longest anymore, change it and restart mining...
        while not mining_result[0]:
            mining_result = self.start_mining(node_signature, chain)

            # Reward miner if the mining result is not false
            # Else update the blockchain

            self.node.blockchain = mining_result[1]
            LIVE_CHAIN_IN.send(self.node.blockchain)

        PENDING_NODE_TRANSACTIONS = requests.get(url = NODE_API_URL + '/transactions', params = {'update':MINER_ADDRESS}).content
        PENDING_NODE_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)

        return mining_result[]

    def start_mining(self, node_signature, chain) -> str:
        new_proof = chain[-1].proof + 1

        proof_hash = None

        start_time = time.time()

        while (proof_hash == None):
            new_proof += random.randint(0, 15)
            resolvable = hashlib.sha512(f"{node_signature}{self.date_time}{new_proof}".encode('utf-8')).hexdigest()
            
            calc = str(round(new_proof / (new_proof*random.randint(2, 30000) - (new_proof/2)) * 10000000))

            # Every minute check for unsynced possibly mined blocks from other nodes
            if (time.time() - start_time) % 60 == 0:
                # If a genesis block has been mined (start of a blockchain), cancel this mining process and start over
                found_new_blockchain, new_blockchain = self.node.consensus(chain)
                
                if found_new_blockchain:
                    return False, new_blockchain

            if resolvable.startswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}") and resolvable.endswith(f"{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}{calc[random.randint(0, 2)]}"):
                self.hash = resolvable
                self.proof = 0
                # Hash has been found by the computer
                proof_hash = resolvable
        
        return new_proof, blockchain


class BlockChain:
    def __init__(self, node_signature):
        self.node_signature = node_signature
        self.mining_rewards = 30
        self.chain = [self.add_genesis_block()]
        self.transactions = []
        self.node = Node(self.chain)

    def add_genesis_block(self) -> Block:
        block = Block(node=self.node, is_genesis=True, proof=1)

        # block = block.mine(self.chain, )

        raise Exception("Failed to validate proof of work")

    @property
    def last_block(self):
        self.chain[-1]


class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def get_network_chains(self):
        network_chains = []

        for node in NETWORK_NODES:
            # Chain requested from node API
            chain = requests.get(f'{node}/all-blocks').content
            chain = json.loads(chain)
            network_chains.append(chain)

        return network_chains

    def consensus(self, blockchain):
        network_chains = self.get_network_chains()

        # Keep longest chain our chain for now...
        self.blockchain = blockchain
        longest_chain = self.blockchain
        # Start looking for other longer chains in other nodes on the network
        for chain in network_chains:
            # When the length of our chain is not the largest, change the largest chain to the remote network chain received from an API
            if len(blockchain) < len(chain):
                lonegst_chain = chain

        # If the current node has the longest blockchain of all, return a 'keep mining' signal
        # Else we want to change the longest chain to the new longest chain, found in another node. Now we return a 'restart mining' signal
        if longest_chain == self.blockchain:
            return False, None
        else:
            self.blockchain = longest_chain
            return True, self.blockchain