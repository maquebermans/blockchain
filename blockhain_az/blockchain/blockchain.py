#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 23:17:58 2022

@author: mukarom.alisyaban
@file : blockchain.py
@description : 
 - building blockchain
 - mining blockchain
"""
# Libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Building Blockchain
class Blockchain:
    def __init__(self):
        # init chain list
        self.chain = []
        
        # init genesis block
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        # init dictionary key that will hold blockchain metadata
        block = {'index': len(self.chain),
                 'timestamp': datetime.datetime.now(),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        # append the block onto the chain
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        # get the last block of the chain
        return self.chain[-1]
        
    def proof_of_work(self, proof, previous_proof):
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
        