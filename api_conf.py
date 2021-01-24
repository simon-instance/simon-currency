from multiprocessing import Pipe

# All nodes in the network, needed for validating proof of work for example
NETWORK_NODES = []

NODE_API_URL = "http://localhost:8080"

MINER_ADDRESS = "daf98ahjfds-34h95bnga-$ndsaofn$xxc"

PENDING_NODE_TRANSACTIONS = []

LIVE_CHAIN_IN, LIVE_CHAIN_OUT = Pipe()