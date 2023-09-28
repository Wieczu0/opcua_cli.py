from opcua import Client
import argparse
import sys
import time


#definicja dla argparse
parser = argparse.ArgumentParser()

#definicja argumentów
parser.add_argument('server_UA_TCP', type=str, help="Enter server addres. Example: opc.tcp://localhost:53530/OPCUA/SimulationServer")
parser.add_argument("-n","--nodeid", type=str, help="Enter NodeID of the object you want to print. Examples: for PS('ns=3;i=1002') for cmd(ns=3;i=1002)", nargs='+')
parser.add_argument("-l","--loop",action="store_true" ,help="Make program work in a loop. Works only with -n parameter")
parser.add_argument("-f","--file", help="Load NodeID from txt file. Enter Address")
parser.add_argument("-s","--send", help="send Value to an object. 'NodeID,value'",nargs=2)
parser.add_argument("-S","--sub",help="subscribe to a node. 'NodeID")

#pobranie argumentów
args = parser.parse_args()


#wczytanie NodeID z pliku
if args.file:
    try:
        with open(args.file, 'r') as txt:
            args.nodeid=txt.read().splitlines()
    except FileNotFoundError:
        print(f"File '{args.file}' not found.")
    except Exception:
        print("an error occured")


#printowanie wskazanego obiektu funkcja
def print_object(args):
    try:
        if len(args.nodeid)>1:
            #dla więcej niż jednego obiektu
            value_list=[]
            for i in range(len(args.nodeid)):
                node = client.get_node(str(args.nodeid[i]))
                value_list.append(node.get_value())
            print(args.nodeid)
            print(value_list)
        else:
            #dla jednego obiektu
            node = client.get_node(str(args.nodeid[0]))
            print(str(args.nodeid[0]))
            print(node.get_value())
    except:
        print("object reading error")
        client.disconnect()
        sys.exit()


#funkcja dla subskrypcji
class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print(f"New data change event at {node}, to {val}")

#łączenie z serweren
try:
    server_endpoint= args.server_UA_TCP
    client= Client(server_endpoint)
    client.connect()
except:
    print("server connection error")
    sys.exit() 



#printowanie wskazanego obiektu wywołanie
if args.nodeid:
    if args.loop:
        try:
            while True:
                print_object(args)
                print(" ")
                time.sleep(1)
        except KeyboardInterrupt:
            client.disconnect()
            sys.exit()
    else:
        print_object(args)


#wysyłanie obiektu do serwera
if args.send:
    try:
        node = client.get_node(args.send[0])
        node.set_value(args.send[1])
        print("value sent")
    except:
        print("Value Sending error, check if the node exist, or is it writable")
        client.disconnect()
        sys.exit()


#subskrypcja (nie dotykać)
if args.sub:
    try:
        #przypisanie funkcji do zmiennej
        handler=SubHandler()
        #tworzenie suba
        subscription = client.create_subscription(1000,handler)
        #obiekt monitorowany
        node_to_monitor = client.get_node(args.sub)
        monitored_item = subscription.subscribe_data_change(node_to_monitor)
        while True:
            pass
    except KeyboardInterrupt:
        client.disconnect()
        sys.exit()
    except:
        print("subscription error")
        client.disconnect()
        sys.exit()

#rozłącz
client.disconnect()