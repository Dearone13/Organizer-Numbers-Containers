from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
# Create server
hostIP=str(socket.gethostbyname(socket.gethostname()))
print (hostIP)
with SimpleXMLRPCServer((hostIP, 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    
    #----------------------------------------------------------------------------
    class ServerClient:
        def __init__(self):
            self.clientsList={}
            self.messages={}
            self.numbers = []
            self.unique = []
            self.repeatedT = []

        #Save all messages from others clients
        def receiveMessage(self, name,txt):
            #self.messages[name]=txt
            self.messages["message"+str(len(self.messages)+1)]={name:txt}
            return 0
        
        #obtain received messages (it is to client use only)
        def getReceivedMessages(self):
            return self.messages
#----------------------------------------------------------------------------

        #Update clients list from index (it is to index server only)
        def updateClientsList(self, clientsList):
            self.clientsList=clientsList
            return 0

        #obtain clients list (it is to client use only)    
        def getClientsList(self):
            return self.clientsList
    #-------------------------------------------------------------------------------  
        #obtain his 11 numbers from index
        def updateReceivedNumbers(self,numbers):
            self.numbers = numbers
            return 0
        #obtain number list(it is to client use only)
        def getNumbers(self):
            return self.numbers
    #Exchangue unique numbers------------------------------------

        #send repeated form origin cleint to that server client(owner)
        def updateRepeatedCopy(self, repeated):
            self.repeatedT = repeated
            print("Valor de los repeated"+ str(self.repeatedT))
            return self.repeatedT
        #return updated repeated list
        def getRepeatedList(self):
            print("Valor a retornar" +str(self.repeatedT))
            return self.repeatedT
     
    #----------------------------------------------------------------------------
    server.register_instance(ServerClient())

    # Run the server's main loop
    server.serve_forever()