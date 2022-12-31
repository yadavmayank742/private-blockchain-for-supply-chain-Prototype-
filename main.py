# @Author MAYANK YADAV

from geopy.geocoders import Nominatim
from Blockchain import Blockchain
import threading
import time

'''
Remeber to add this line whenever adding a new block : 
    block_tracking_dict[new_block.hash] = {}
'''
supply_chain = Blockchain()
block_tracking_dict=dict()
block_tracking_dict[supply_chain.chain[0].hash]={time.ctime():'Genesis Block Created!'} # genesis block
delivery_status_dictionary=dict()
delivery_status_dictionary[supply_chain.chain[0].hash]=True # genesis block
'''
THIS DICTIONARY WILL HAVE THE FOLLOWING STRUCTURE
    block.hash : {time.time() : location}
'''

def menu():
    print("Choose from avaliable options :")
    print("\t1. Place a new order.")
    print("\t2. Track an order.")
    print("\t3. Mark a product as received.")
    print("\t4. View product location hostory.")
    print("\t5. Exit.")
    print("NOTE: Order ID will be needed for option 2, 3, and 4.")
    try:
        user_input = int(input("Choice [1/2/3/4/5] : "))
        while(user_input not in [1, 2, 3, 4, 5]):
            print("Don't try to be smart, just enter 1, 2, 3, 4, or, 5!")
            user_input = menu()
        return user_input
    except Exception as e:
        print("Enter an integer, ASSHOLE !")
        menu()


def get_location(hash_value):
    cities_list=["Agra", "Gwalior", "Bhopal", "Nagpur"," Adilabad", "Warangal", "Hyderabad", "Gulbarga", "Anantpura", "Bangalore"]
    loc = Nominatim(user_agent="GetLoc")
    for city in cities_list:
        getLoc=loc.geocode(city)
        block_tracking_dict[hash_value][time.ctime()]=[getLoc.latitude, getLoc.longitude, city]
        time.sleep(1)

def main():
    user_input = menu()

    while(user_input in [1, 2, 3, 4, 5]):

        if(user_input == 1): # place a new order
            new_block = supply_chain.create_new_block()
            supply_chain.chain.append(new_block)
            block_tracking_dict[new_block.hash] = {}
            delivery_status_dictionary[new_block.hash] = False
            origin_city = input("Enter Origin City : ")
            origin_city = "Delhi" # fuck your input!
            loc = Nominatim(user_agent="GetLoc")
            getLoc = loc.geocode(origin_city)
            block_tracking_dict[new_block.hash] = {time.ctime():[getLoc.latitude, getLoc.longitude, origin_city]}
            # once this is done, we need to update location after every one second..
            update_location_thread = threading.Thread(target=get_location, args=(new_block.hash,))
            update_location_thread.start()

        elif(user_input == 2): # track an order
            try:
                order_id = int(input("Enter Order ID : "))
                found_block = False
                for block in supply_chain.chain:
                    if(block.data['order_id']==order_id):
                        found_block = True
                        print(f"Found Order ID {order_id}")
                        print(f"These are product details :")
                        for i in block.data:
                            print(f"\t{i.upper()}\t{block.data[i]}")
                        print(f"This is the location hostory :\n\tTime\t\t\tLocation")
                        for _time in block_tracking_dict[block.hash]:
                            print(f"{_time}\t{block_tracking_dict[block.hash][_time]}")
                        if(delivery_status_dictionary[block.hash]):
                            print("Delivery Status : Delivered")
                        else:
                            print("Delivery Status : Not Delivered")
                if(not found_block):
                    print("No Such Order ID!")
            except Exception as err:
                print("Provide a FUCKING INTEGER!")

        elif(user_input == 3): # mark a product as received
            try:
                order_id = int(input("Enter Order ID : "))
                found_block = False
                for block in supply_chain.chain:
                    if(block.data['order_id']==order_id):
                        found_block = True
                        print(f"Found Order ID {order_id}")
                        print(f"These are product details :")
                        for i in block.data:
                            print(f"\t{i.upper()}\t{block.data[i]}")
                        try:
                            delivered = input("Want to mark this product as received [y/n]: ")
                            if(delivered.lower() == 'y'):
                                delivery_status_dictionary[block.hash] = True
                                print(f"Product {block.data['product_name']} marked delivered!")
                            elif(delivered.lower == 'n'):
                                print(f"Product {block.data['product_name']} still not delivered!")
                            else:
                                raise Exception("MoFu!, just give 'y' or 'n'")
                        except Exception as err:
                            print(err)
                if(not found_block):
                    print("No Such Order ID!")
            except Exception as err:
                print(err)

        elif(user_input == 4): # View location history of some order
            '''
            This might look like optin 2 coz this is a prototype
            IRL, tracking is geolocation based and will upadte over time
            This option is for forensics of delivery
            '''
            try:
                order_id = int(input("Enter Order ID : "))
                found_block = False
                for block in supply_chain.chain:
                    if(block.data['order_id']==order_id):
                        found_block = True
                        print(f"Found Order ID {order_id}")
                        print(f"These are product details : ")
                        for i in block.data:
                            print(f"\t{i.upper()}\t{block.data[i]}")
                        print(f"This is the location hostory :\n\tTime\t\t\tLocation")
                        for _time in block_tracking_dict[block.hash]:
                            print(f"{_time}\t{block_tracking_dict[block.hash][_time]}")
                        if(delivery_status_dictionary[block.hash]):
                            print("Delivery Status : Delivered")
                        else:
                            print("Delivery Status : Not Delivered")
                if(not found_block):
                    print("No Such Order ID!")
            except Exception as err:
                print("Provide a FUCKING INTEGER!")

        elif(user_input == 5): # display all blocks and their related shit and exit
            print("Status of all the orders is as follows :")
            if(len(supply_chain.chain)>1):
                for block in supply_chain.chain:
                    print("========================================================")
                    print(f"Product details : ")
                    for i in block.data:
                        print(f"\t{i.upper()}\t{block.data[i]}")
                    print(f"Location hostory :\n\tTime\t\t\tLocation")
                    for _time in block_tracking_dict[block.hash]:
                        print(f"{_time}\t{block_tracking_dict[block.hash][_time]}")
                    if(delivery_status_dictionary[block.hash]):
                        print("Delivery Status : Delivered")
                    else:
                        print("Delivery Status : Not Delivered")
                    print("========================================================")
            else:
                print("NO ORDERS PLACED!")
            break;

        user_input = menu()


if __name__ == '__main__':
    main()