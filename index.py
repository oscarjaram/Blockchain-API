from blockchain import Block, Blockchain
from flask import Flask, request
import requests
import time
import json

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_transaction', methods = ['POST'])
def new_transaction():
    tx_data = request.get_json()
    require_fields = ['author', 'content']
    for field in require_fields:
        if not tx_data.get(field):
            return 'Datos de transaccion invalidos', 404
    
    tx_data['timestamp'] = time.time()
    blockchain.new_transaction(tx_data)
    return "Exito", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({
        'length': len(chain_data),
        'chain': chain_data
    })

@app.route('/mine', methods = ['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return 'Nothing to mine'
    return 'Block#{} is mined'.format(result)

@app.route('/pending_transaction', methods=['POST'])
def get_pending_transaction():
    return json.dumps(blockchain.nconfirmed_transactions)

app.run(port=8000)