# %%
from hashlib import sha256
import json
import time

class Block:

    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty = 2
        
    def create_genesis_block(self):
        genesis_block = Block(
            index = 0, 
            transactions = [], 
            timestamp = time.time(), 
            previous_hash = "0"*64)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def print_block(self, n):
        if len(self.chain) < n:
            return ''
        else:
            block = self.chain[n]
            return ' Index: {}\nTransactions: {}\nTimestamp: {}\nPreviousHash: {}\n'.format(
                block.index, block.transactions, block.timestamp, block.previous_hash
            )
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while (computed_hash.startswith('0' * self.difficulty) == False):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        condition1 = block_hash.startswith('0'*self.difficulty)
        condition2 = block_hash == block.compute_hash()
        return (condition1 and condition2)

    def new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(
            index = last_block.index + 1,
            transactions = self.unconfirmed_transactions,
            timestamp = time.time(),
            previous_hash = last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
