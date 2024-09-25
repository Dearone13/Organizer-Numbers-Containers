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


with SimpleXMLRPCServer((hostIP, 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class Index:
        def __init__(self)->None:
            self.registeredList={} #clients ips and names
            self.serverActive = 0  #count how many servers are on
            self.listNumbers = []
            self.parts = []
            
        #Register a client
        def register(self, ip, name):
            self.registeredList[name]=ip
            #Send clients IP to all clients
            self.serverActive += 1 #For every server active add 1
            #List of n*11 numbers to use counting th numbers of servers on
            self.listNumbers =  np.array([i for i in range(11)] * self.serverActive)
            #shuffle n*11 numbers in random order
            random.shuffle(self.listNumbers)
            #divide th list in five parts
            self.parts = np.array_split(self.listNumbers, 5)
             
            self.sendRegisteredClientsList()
            self.sendNumbersatRegisteredClients()
            return self.registeredList

        #Send registered clients list to all clients
        def sendRegisteredClientsList(self):
            print("Clients List: " +str(self.serverActive))
            print(self.registeredList)
            cpRegisteredList=self.listNumbers
            for key in self.registeredList:
                IPClient = self.registeredList.get(key)
                sc = xmlrpc.client.ServerProxy('http://'+IPClient+':8000')
                sc.updateClientsList(cpRegisteredList)
                
        def sendNumbersatRegisteredClients(self):
            index = 0 #Define a index for acces to parts
            for key in self.registeredList: 
                cpNumberList = self.parts[index] #create a copy of  every numbers of parts
                IPClient = self.registeredList.get(key) #Bring serverClients ip
                sc = xmlrpc.client.ServerProxy('http://'+IPClient+':8000')  #Activate serverClient
                sc.updateReceivedNumbers(cpNumberList.list()) #Index give  list of 11 numbers
                index += 1 #Increment index
                if index >= len(self.parts): #When index is queal to lenght of part
                    break #should stop the for and not iterate more because all the numbers
                      
    server.register_instance(Index())

    # Run the server's main loop
    print("Server Index actived in: "+hostIP)
    server.serve_forever()