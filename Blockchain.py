# @Author MAYANK YADAV

from Block import Block
'''
Remember block structure :
    (previous_hash, data)
where 
    data is a dictionary contaning product_id, order_id, product_name
'''
class Blockchain():
    def __init__(self):
            block_0 = self.create_genesis_block()
            self.chain = [block_0]
   
    def create_genesis_block(self):
        data = {
        'product_id': 0,
        'order_id' : 0,
        'product_name' : ''
        }
        genesis_block = Block('0', data)
        return genesis_block

    def create_new_block(self):
        '''
        this will be called only for a new order
        '''
        previous_block = self.chain[-1]
        is_input_valid = False
        while(is_input_valid is False):
            try:
                product_id = int(input("Enter Product ID : "))
                try:
                    order_id = int(input("Enter Order ID : "))
                    try:
                        product_name = input("Enter Product Name : ")
                        is_input_valid = True
                    except Exception as name_error:
                        print("Some Error Occured!, Please Retry.")
                except Exception as order_id_error:
                    print("Order ID Needs to be an integer!, Please Retry.")
            except Exception as product_id_error:
                print("Product ID Needs to be an integer!, Please Retry.")

        data = {'product_id' : product_id, 'order_id' : order_id, 'product_name' : product_name}
        new_block = Block(previous_block.hash, data)
        return new_block