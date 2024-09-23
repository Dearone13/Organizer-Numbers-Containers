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

        #Save all messages from others clients
        def receiveMessage(self, name,txt):
            #self.messages[name]=txt
            self.messages["message"+str(len(self.messages)+1)]={name:txt}
            return 0
        
        #obtain received messages (it is to client use only)
        def getReceivedMessages(self):
            return self.messages

        #Update clients list from index (it is to index server only)
        def updateClientsList(self, clientsList):
            self.clientsList=clientsList
            return 0

        #obtain clients list (it is to client use only)    
        def getClientsList(self):
            return self.clientsList
    #----------------------------------------------------------------------------
    server.register_instance(ServerClient())

    # Run the server's main loop
    server.serve_forever()