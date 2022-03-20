#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 23:17:58 2022

@author: mukarom.alisyaban
@file : blockchain.py
@description : 
 - building blockchain
 - mining blockchain
@term
 - genesis : the first block on the chain
 - proof-of-work : a piece of data that a miner should find in order to create new block
"""
# Libraries
import datetime
import hashlib
import json
from urllib import response
from flask import Flask, jsonify


# Building Blockchain
#================================================================

class Blockchain:
    def __init__(self):
        # init chain list
        self.chain = []
        
        # init genesis block
        self.create_block(proof = 1, previous_hash = '0')
    
    
    def create_block(self, proof, previous_hash):
        # init dictionary key that will hold blockchain metadata
        block = {'index': len(self.chain),
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        # append the block onto the chain
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self):
        # get the last block of the chain
        return self.chain[-1]
        
        
    def proof_of_work(self, previous_proof):
        # init new proof to iterate over (we will start the proof by 1)
        new_proof = 1
        # in order for the iteration to works, we will need to define proof checker
        check_proof = False
        while check_proof is False:
            # define the challange that will be solved by the miner (we will use 4 leading zeros to define the winner, with combination of new proof and previous proof on the formula)
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
    def hash(self, block):
        # we will use json.dumps and encode the block before we hash it
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        # we will iterate from the first chain (the genesis)
        previous_block = chain[0]
        block_index = 1
        
        # we will validate the chain from the first chain until the latest chain 
        while block_index < len(chain):
            # define current block
            block = chain[block_index]
            # check if current block previous_hash has the same hash with previous block hash 
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # check if proof of work has 4 leading zeros
            previous_proof = previous_block['proof']
            proof = block['proof']
            # validate the proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            return True 
            
        
        
    
 # Mining Blockchain
 #================================================================
 
 # Web APP
app = Flask(__name__)
app.config['JSONIFY_PREETYPRINT_REGULAR'] = False
     
# create blockchain object
blockchain = Blockchain()

# create API method
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message': 'Congratulations! You have successfully mine a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Running the flask server
app.run(host='0.0.0.0', port='5000')