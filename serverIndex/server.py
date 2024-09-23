from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import numpy as np
import random
import socket

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
# Create server
hostIP=str(socket.gethostbyname(socket.gethostname()))
#List of 55 numbers to use
listNumbers = np.array([i for i in range(11)] * 5)
#shuffle 55 numbers in random order
random.shuffle(listNumbers)
#divide th list in five parts
parts = np.array_split(listNumbers, 5) 
with SimpleXMLRPCServer((hostIP, 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class Index:
        def __init__(self)->None:
            self.registeredList={} #clients ips and names
            
         

        #Register a client
        def register(self, ip, name):
            self.registeredList[name]=ip
            #Send clients IP to all clients
            self.sendRegisteredClientsList()
            return self.registeredList

        #Send registered clients list to all clients
        def sendRegisteredClientsList(self):
            print("Clients List:")
            print(self.registeredList)
            cpRegisteredList=self.registeredList
            for key in self.registeredList:
                IPClient = self.registeredList.get(key)
                sc = xmlrpc.client.ServerProxy('http://'+IPClient+':8000')
                sc.updateClientsList(cpRegisteredList)
                
        def sendNumbersatRegisteredClients():
            for i in parts:
                return i
                      
    server.register_instance(Index())

    # Run the server's main loop
    print("Server Index actived in: "+hostIP)
    server.serve_forever()