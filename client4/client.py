import xmlrpc.client
import socket
import numpy as np
#----------------------------------------------------------------------------

class Client:
    def __init__(self, name, ipServerIndex):
        # Server index IP
        if(ipServerIndex == ""):
            self.indexIP = '172.17.0.2'  # Misma del ip del indexador
        else:
            self.indexIP = ipServerIndex

        self.clientsList = {}  # clients ips and names
        self.number = []  # list of 11 numbers from index
        self.unique = []  # list of unique numbers
        self.repeated = []  # list of repeated numbers
        self.repeatedT = []  # repeated from every other client except himself
        self.clientIP = str(socket.gethostbyname(socket.gethostname()))
        self.name = name

    # get clients list from serverClient        
    def getClientsList(self):
        s = xmlrpc.client.ServerProxy('http://' + self.clientIP + ':8000')
        self.clientsList = s.getClientsList()

    # Send messages to all client partners
    def sendMessage(self, txt):
        # update clientsList
        self.getClientsList()
        # Send message to all clients
        for key in self.clientsList:
            IPClient = self.clientsList.get(key)
            s = xmlrpc.client.ServerProxy('http://' + str(IPClient) + ':8000')
            s.receiveMessage(self.name, txt)

    # Show all received messages from others clients
    def showReceivedMessages(self):
        s = xmlrpc.client.ServerProxy('http://' + self.clientIP + ':8000')
        return s.getReceivedMessages()

    # Register client in the serverIndex
    def registerMe(self):
        sIndex = xmlrpc.client.ServerProxy('http://' + self.indexIP + ':8000')
        sIndex.register(self.clientIP, self.name)

    def getNumbersList(self):
        s = xmlrpc.client.ServerProxy('http://' + self.clientIP + ':8000')
        self.number = s.getNumbers()
        print("number list: " + str(self.number))

    #----------------------------------------------------------------------------

    # Method for unique and repeated
    def encontrar_unicos_y_repetidos(self, number):
        conteo = np.unique(number, return_counts=True)
        unicos = []
        repetidos_list = []

        for val, count in zip(conteo[0], conteo[1]):
            if count == 1:  # Conteo[1] se asigno a count y verifica si solo existe una vez
                unicos.append(val)  # Agrega el numero a unicos
            elif count > 1:  # Si ese numero existe más de una vez
                unicos.append(val)
                repetidos_list.extend([val] * (count - 1))  # Añade los valores repetidos

        print("Repetidos metodo" + str(repetidos_list))
        print("unicos metodo" + str(unicos))
        return unicos, repetidos_list

    # Method swap-------------------------------------------------------------------------------
    def swap(self):
        self.getClientsList() #updated ClientList
        for key in self.clientsList: #Scooch the Clients
            IPClient = self.clientsList.get(key) #asigned ip of clientList other clients
            if self.clientIP != IPClient: #When the ip is not the same of the client now
                s = xmlrpc.client.ServerProxy('http://' + str(IPClient) + ':8000') #Bring conection
                self.repeatedT = np.array(s.getRepeatedList(), dtype=np.int64) #Past numpy64 of getRepeatedList from serverClient of the other container
                print("Dato del servidor: " + str(self.repeatedT)) #Print the repeated numbers of clientList

                # Asegúrate de que 'unique' sea una lista, no un array de numpy
                self.unique = list(self.unique)  # Convert to list

                elementos_a_eliminar = [] # list for index to numbers to eliminate

                for index,repeat in enumerate(self.repeatedT): #evaluate the number(repeat) and assign index
                    if repeat not in self.unique: #When number(repeat) is not in unique number of actual client
                        self.unique.append(repeat) #add to unique from repeatedList of other client
                        elementos_a_eliminar.append(index) #add index to eliminate number repeated

                # Eliminar los elementos repetidos fuera del bucle
                indices_a_eliminar = np.array(elementos_a_eliminar) #convert np index to eliminate
                self.repeatedT = np.delete(self.repeatedT,indices_a_eliminar.astype(int)) #delete numbers with index of the numbers to eliminate

                # Convertir de nuevo a numpy array si es necesario, para ordenar
                self.unique = np.array(self.unique) #convert to np
                self.unique = np.sort(self.unique) #sort to np 

                print("Nuevos datos únicos: " + str(self.unique)) #print updated
                print("Nuevos datos repetidos sobrante: " + str(self.repeatedT))#print update

                self.repeatedT = [int(num) for num in self.repeatedT]  # Convert list
                s.updateRepeatedCopy(self.repeatedT) #send new repeatedList from container to update the repeatedList 

    #send repeatedNumbers to this numbersRepeated since serverClient
    def sendRepeated(self, selfIP, repeated):
        self.repeated = [int(num) for num in repeated] #convert to list
        s = xmlrpc.client.ServerProxy('http://' + str(selfIP) + ':8000') #Bring conection
        s.updateRepeatedCopy(self.repeated) #send to serverClient
        return 0
 
    #updated repeatedList this CLIENT(NO OTHERS) :)
    def updateRepeated(self, selfIP):
        s = xmlrpc.client.ServerProxy('http://' + str(selfIP) + ':8000') #Bring conection
        print("repeated before: " + str(self.repeated)) #repeatedList beafore update
        return s.getRepeatedList() #return new repeatedList to client.repeatedList
        # print("repeated after: " + str(self.repeated))
        return self.repeated
     

# Terminal----------------------------------------------------------------------------------
client = Client(input("Client name: "), input("Index Server IP (172.17.0.2): "))
client.registerMe()
while(True):
    # client1.showReceivedMessages()
    command = input(client.name + "::. ")
    if (command == "bye"):
        break
    elif (command == "send message"):
        client.sendMessage(input("message>>"))
    elif (command == "show received messages"):
        print(client.showReceivedMessages())
    elif (command == "get clients list"):
        client.getClientsList()
        print(client.clientsList)
    elif (command == "get numbers list"):
        # Define command for bring numbers list
        client.getNumbersList()
        # print(client.number)
    elif (command == "get ru"):
        client.unique, client.repeated = client.encontrar_unicos_y_repetidos(client.number)
    elif (command == "send repeatedList client"):
        #Send repatedList this serverClient THSI CONTAINER(SELF) , no others
        client.sendRepeated(client.clientIP, client.repeated)
    elif (command == "swap"):
        #Activate swap method (for communication between container to origin container)
        client.swap()
    elif (command == "updated repeated list(after swap)"):
        client.repeated = client.updateRepeated(client.clientIP) #update my repeatedList change after swap from container origin 
        print("valor de repeat(client) after"+ str(client.repeated))
    elif (command == "help"):
        print("send message: send a message to all clients")
        print("get clients list: show the clients list")
        print("bye: exit")
        print("help: show commands and its explanation")
    else:
        print("command not found")
# ----------------------------------------------------------------------------
