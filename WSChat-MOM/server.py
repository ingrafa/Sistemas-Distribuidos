import CosNaming, Server, Server__POA
import pika
import sys
import threading

from omniORB import CORBA, PortableServer
from SOAPpy import SOAPServer
from utils import *


name_server = 'Server'

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
ws_server = SOAPServer(('localhost', 8081))

def create_queue(username):
    channel.queue_declare(queue=username)

ws_server.registerFunction(create_queue)

def server_run():
    global ws_server
    ws_server.serve_forever()

# Executa o WS
start_ws = threading.Thread(target=server_run)
start_ws.daemon = True
start_ws.start()

class CentralServer(Server__POA.CentralServer):
    users_list = {}

    def connect_user(self, username):
        if username in self.users_list:
            del self.users_list[username]
        self.users_list[username] = STATUS_ON
        return STATUS_ON

    def change_user_status(self, username, status):
        self.users_list[username] = status

    def get_user_status(self, username):
        return self.users_list[username] if username in self.users_list else ERROR

    def list_users_by_status(self, status):
        return [username for username in self.users_list if self.users_list[username] == status]

    def get_username_list(self):
        return [username for username in self.users_list]


# Initialize the ORB service and find the root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Create an instance of CentralServer and an CentralServer object reference
ei = CentralServer()
eo = ei._this()

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print("Failed to narrow the root naming context")
    sys.exit(1)


# Bind context to the root context
try:
    name = [CosNaming.NameComponent(name_server, "context")]
    context = rootContext.bind_new_context(name)
    print("New context bounded: {}").format(name_server)

except CosNaming.NamingContext.AlreadyBound as ex:
    obj = rootContext.resolve(name)
    context = obj._narrow(CosNaming.NamingContext)
    
    if context is None:
        print("context exists but is not a NamingContext")
        sys.exit(1)
    
# Bind the object to the context
try:
    name = [CosNaming.NameComponent(name_server, "Object")]
    context.bind(name, eo)

except CosNaming.NamingContext.AlreadyBound:
    context.rebind(name, eo)

# Activate the POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Block for ever (or until the ORB is shut down)
orb.run()
