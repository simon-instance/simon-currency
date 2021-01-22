#!/usr/bin/python3.9

from Currency import Block, BlockChain

if __name__ == "__main__":
    blockchain = BlockChain("iadbuhpfdfpaiubh")
    print(blockchain.chain[0].hash)