# @Author MAYANK YADAV
import hashlib
import time

class Block:

    def __init__(self, previous_hash, data):
        '''
        data is a dictionary contaning product_id, order_id, product_name
        '''
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f'{self.timestamp}{self.previous_hash}{self.data}'.encode()
        return hashlib.sha256(block_string).hexdigest()